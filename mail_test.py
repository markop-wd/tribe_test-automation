import imaplib
import email
import os
from email.header import decode_header
from time import sleep

from bs4 import BeautifulSoup
from datetime import datetime
from email.message import Message


class MailParser:
    username = os.environ.get('gmail_username')
    password = os.environ.get('gmail_password')

    href_identifier = 'sendgrid.net'
    mail_subject = 'Your password reset request'
    mail_from = 'support@tribe.xyz'

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)

    @classmethod
    def run(cls, call_date: datetime):
        """
        Main business logic of the class
        :param call_date: datetime when the forgot password was clicked
        :type call_date: datetime
        :return: the href within the reset e-mail where the reset is initiated
        :rtype: str
        """

        # Get the total number of messages in the inbox
        _, messages = cls.imap.select("INBOX", readonly=True)
        message_total = int(messages[0])

        # Get the first/latest message from the inbox and check if it matches
        latest_msg = cls.get_mail(message_total)

        # Get the date of the message
        date, date_enc = decode_header(latest_msg["Date"])[0]
        if isinstance(date, bytes):
            date = date.decode(date_enc)

        # convert from the header date to the datetime format and extract only the date
        try:
            date_dtm = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            try:
                date_dtm = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
            except ValueError:
                try:
                    date_dtm = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z (%Z)")
                except ValueError:
                    raise DateParseError

        date_dtm = date_dtm.replace(tzinfo=None)

        # Check if the time when we called the function is later than the latest email date
        if call_date > date_dtm:
            return cls.waiter(message_total)
        else:
            # If the latest e-mail is after the call date loop over
            for email_id in reversed(range(1, message_total + 1)):
                msg = cls.get_mail(email_id)
                return_date = cls.header_parse(msg)
                if not return_date:
                    continue
                # If a fitting message was found (via header_parse)
                # Make sure it's after the call date
                elif return_date and (call_date > return_date):
                    return cls.waiter(message_total)
                # If there is a proper header and the date is after the call date return the message
                else:
                    return cls.message_parse(msg)

    @classmethod
    def get_mail(cls, mail_id: int):
        """
        Returns the email with the corresponding email_id ID
        :param mail_id: ID of the e-mail, usually in the int form
        :type mail_id: int
        :return: the Message that corresponds to the mail_id ID
        :rtype: Message
        """
        _, message_list = cls.imap.fetch(str(mail_id), "(RFC822)")
        response = message_list[0]
        # noinspection PyUnresolvedReferences
        msg = email.message_from_bytes(response[1])
        return msg

    @classmethod
    def waiter(cls, message_total: int):
        """
        Function that waits for the proper forgot e-mail to arrive if none was detected initially
        :param message_total: current number of messages in the inbox
        :type message_total: int
        :return: Message that arrived after the call date with the corresponding parameters
        :rtype: Message
        """
        loop_count = 0
        # Make sure the loop runs for 10 minutes (600 seconds)
        while True:
            if loop_count >= 60:
                raise EmailTimeout
            sleep(10)
            new_messages = cls.reselect()
            # If a new message arrived check it
            if new_messages > message_total:
                # If only one new message arrived new_messages will equal to the ID of the newest
                if message_total + 1 == new_messages:
                    msg = cls.get_mail(new_messages)
                    if not cls.header_parse(msg):
                        message_total = new_messages
                        continue
                    else:
                        return cls.message_parse(msg)
                else:
                    # If multiple messages arrived parse through all of their headers
                    for new_email in reversed(range(message_total, new_messages + 1)):
                        msg = cls.get_mail(new_email)

                        if not cls.header_parse(msg):
                            continue
                        else:
                            return cls.message_parse(msg)

                    message_total = new_messages

            loop_count += 1

    @classmethod
    def reselect(cls):
        _, messages = cls.imap.select("INBOX", readonly=True)
        message_total = int(messages[0])
        return message_total

    @classmethod
    def message_parse(cls, msg: Message):
        for part in msg.walk():
            # extract content type of email
            content_type = part.get_content_type()
            # get the email body
            try:
                body = part.get_payload(decode=True).decode()
            except AttributeError:
                pass
            else:
                if content_type == "text/plain":
                    continue
                elif content_type == "text/html":
                    mail_soup = BeautifulSoup(body, 'html.parser')
                    all_a = mail_soup.find_all('a')
                    for a in all_a:
                        a_href = a.get('href')
                        if cls.href_identifier in a_href:
                            return a_href
                    else:
                        raise MailParseException

    @classmethod
    def header_parse(cls, msg: Message):
        # decode the email subject
        subject, subject_enc = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            # if it's a bytes, decode to str
            subject = subject.decode(subject_enc)
        if subject != cls.mail_subject:
            return False

        # decode email sender
        msg_from, from_enc = decode_header(msg.get("From"))[0]
        if isinstance(msg_from, bytes):
            msg_from = msg_from.decode(from_enc)
        if msg_from != cls.mail_from:
            return False

        # decode the date
        date, date_enc = decode_header(msg["Date"])[0]
        if isinstance(date, bytes):
            date = date.decode(date_enc)

        # convert from the header to the datetime format and extract only the date
        try:
            date_dtm = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            try:
                date_dtm = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
            except ValueError:
                date_dtm = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z (%Z)")

        date_dtm = date_dtm.replace(tzinfo=None)

        return date_dtm


class MailParseException(Exception):
    def __init__(self, message="sendgrid.net not found as a link in the e-mail"):
        self.message = message
        super(MailParseException, self).__init__(self.message)


class MultipartException(Exception):
    def __init__(self, message="Message is not multi-part, this has not been implemented"):
        self.message = message
        super(MultipartException, self).__init__(self.message)


class EmailTimeout(Exception):
    def __init__(self, message="Reset password e-mail has not arrived after 10 minutes"):
        self.message = message
        super(EmailTimeout, self).__init__(self.message)


class DateParseError(Exception):
    def __init__(self, message=""):
        self.message = message
        super(DateParseError, self).__init__(self.message)


# test = datetime.strptime('2021, 09, 08, 19, 50, 30', '%Y, %d, %m, %H, %M, %S')
# print(MailParser.run(test))

