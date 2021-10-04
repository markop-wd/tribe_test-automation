"""
A way to wait for the e-mail with the given subject to arrive and then parse it for the reset link
"""
import imaplib
import os
from time import sleep
from datetime import datetime
from email.header import decode_header
from email.message import Message
import email

from bs4 import BeautifulSoup
from dotenv import load_dotenv


class MailParser:
    """
    Main functions of the e-mail parsing and waiting
    """
    
    def __init__(self):
        load_dotenv('.env')
    
        self.href_identifier = 'sendgrid.net'
        self.mail_subject = 'Your password reset request'
        self.mail_from = 'support@tribe.xyz'
    
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap.login(os.environ.get('gmail_username'), os.environ.get('gmail_password'))

    def run(self, call_date: datetime):
        """
        Main business logic of the class
        :param call_date: datetime when the forgot password was clicked
        :type call_date: datetime
        :return: the href within the reset e-mail where the reset is initiated
        :rtype: str
        """

        # Get the total number of messages in the inbox
        _, messages = self.imap.select("INBOX", readonly=True)
        message_total = int(messages[0])

        # Get the first/latest message from the inbox and check if it matches
        latest_msg = self.get_mail(message_total)

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
                except ValueError as exc:
                    raise DateParseError from exc

        # Check if the time when we called the function is later than the latest email date
        if call_date > date_dtm:
            return self.waiter(message_total)

        # If the latest e-mail is after the call date loop over
        for email_id in reversed(range(1, message_total + 1)):
            msg = self.get_mail(email_id)
            return_date = self.header_parse(msg)
            if not return_date:
                continue
            # If a fitting message was found (via header_parse)
            # Make sure it's after the call date
            if return_date and (call_date > return_date):
                return self.waiter(message_total)
            # If there is a proper header and the date is after the call date return the message
            return self.message_parse(msg)

    def get_mail(self, mail_id: int):
        """
        Returns the email with the corresponding email_id ID
        :param mail_id: ID of the e-mail, usually in the int form
        :type mail_id: int
        :return: the Message that corresponds to the mail_id ID
        :rtype: Message
        """
        _, message_list = self.imap.fetch(str(mail_id), "(RFC822)")
        response = message_list[0]
        # noinspection PyUnresolvedReferences
        msg = email.message_from_bytes(response[1])
        return msg

    def waiter(self, message_total: int):
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
            new_messages = self.reselect()
            # If a new message arrived check it
            if new_messages > message_total:
                # If only one new message arrived new_messages will equal to the ID of the newest
                if message_total + 1 == new_messages:
                    msg = self.get_mail(new_messages)
                    if not self.header_parse(msg):
                        message_total = new_messages
                        continue

                    return self.message_parse(msg)

                # If multiple messages arrived parse through all of their headers
                for new_email in reversed(range(message_total, new_messages + 1)):
                    msg = self.get_mail(new_email)

                    if not self.header_parse(msg):
                        continue

                    return self.message_parse(msg)

                message_total = new_messages

        loop_count += 1

    def reselect(self):
        """
        Just a quick way to check the message total in the inbox
        :return:
        """
        _, messages = self.imap.select("INBOX", readonly=True)
        message_total = int(messages[0])
        return message_total

    def message_parse(self, msg: Message):
        """
        Parse the message for the reset message URL
        :param msg:
        :return:
        """
        for part in msg.walk():
            # extract content type of email
            content_type = part.get_content_type()
            # get the email body
            try:
                body = part.get_payload(decode=True).decode()
            except AttributeError:
                continue
            else:
                if content_type == "text/plain":
                    continue

                if content_type == "text/html":
                    mail_soup = BeautifulSoup(body, 'html.parser')
                    all_a_els = mail_soup.find_all('a')
                    for a_el in all_a_els:
                        a_href = a_el.get('href')
                        if self.href_identifier in a_href:
                            return a_href

                    raise MailParseException
        return None

    def header_parse(self, msg: Message):
        """
        Parsing the header and checking/exiting if the header subject does not match or sender or date. In that order
        :param msg: message upon which to perform header_parse upon
        :return: date when the message was received
        """
        # decode the email subject
        subject, subject_enc = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            # if it's a bytes, decode to str
            subject = subject.decode(subject_enc)
        if subject != self.mail_subject:
            return False

        # decode email sender
        msg_from, from_enc = decode_header(msg.get("From"))[0]
        if isinstance(msg_from, bytes):
            msg_from = msg_from.decode(from_enc)
        if msg_from != self.mail_from:
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

        return date_dtm


class MailParseException(Exception):
    """
    Exception raised when there is no appropriate href url in the e-mail
    """

    def __init__(self, message="sendgrid.net not found as a link in the e-mail"):
        self.message = message
        super().__init__(self.message)


class MultipartException(Exception):
    """
    Exception when the message is not multi-part, as the logic for that is not implemented/needed
    """

    def __init__(self, message="Message is not multi-part, this has not been implemented"):
        self.message = message
        super().__init__(self.message)


class EmailTimeout(Exception):
    """
    Custom exception to raise after 10 minutes of attempts to find the e-mail
    """

    def __init__(self, message="Reset password e-mail has not arrived after 10 minutes"):
        self.message = message
        super().__init__(self.message)


class DateParseError(Exception):
    """
    Date formatting in e-mails can take on many forms and I don't think I implemented them all - hence this
    """

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


if __name__ == '__main__':
    mp = MailParser()
    test = datetime.strptime('2021, 10, 04, 20, 50, 30', '%Y, %d, %m, %H, %M, %S')
    print(mp.run(test))
