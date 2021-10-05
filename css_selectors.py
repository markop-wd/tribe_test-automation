class General:
    main_header = 'div#main_header'
    main_page = 'div.main-page'


class Auth:
    email_input = 'input#email'
    password_input = 'input#password'
    login_button = 'button#login'
    forgot_pw_link = 'div#forgot_password'
    reset_mail_input = 'div.Popup input[type="email"]'
    reset_mail_button = 'div.Popup > div:nth-child(3) button'
    after_reset_popup = 'div#popup_forgot_sent'
    after_reset_popup_text = 'div#popup_forgot_sent div.content'


class PasswordReset:
    change_pw_btn = 'button#password_change_btn'
    first_pw_input = 'input[placeholder="New password"]'
    second_pw_input = 'input[placeholder="Confirmation"]'


class ProjectSetup:
    company_search = 'input[placeholder="Search a company"]'
    company_add_button = 'button#company_add'
    company_add_popup = 'div#company_add_popup'
    job_add_popup = 'div#job_create_popup'
    job_add_button = 'button#job_add'
    job_edit_popup = 'div#job_edit_popup'
    show_archived = 'select#archived_select'

    job_row = 'div#job_group > div.GroupItem'
    archive = 'div#job_group > div.GroupItem button[title="Archive this job"]'
    job_sequence = 'div#job_group > div.GroupItem div:nth-child(8) a'
    recruiter = 'div#job_group > div.GroupItem div:nth-child(5) > select'
    manager = 'div#job_group > div.GroupItem div:nth-child(6) > select'
    edit_job = 'div#job_group > div.GroupItem div:nth-child(4) button'
    job_title = 'div#job_group > div.GroupItem div:nth-child(4) a'

    # NOTE - For a particular element use div#job_group > div.GroupItem:nth-child(X)
    # nth-child for the (X) is increasing in increments of 2 starting from 1 - 1,3,5,7...
    @classmethod
    def job_row_nth(cls, num: int):
        return f'div#job_group > div.GroupItem:nth-child({num})'

    @classmethod
    def archive_nth(cls, num: int):
        return cls.job_row_nth(num) + ' button[title="Archive this job"]'

    @classmethod
    def job_sequence_nth(cls, num: int):
        return cls.job_row_nth(num) + ' div:nth-child(8) a'

    @classmethod
    def recruiter_nth(cls, num: int):
        return cls.job_row_nth(num) + ' div:nth-child(5) > select'

    @classmethod
    def manager_nth(cls, num: int):
        return cls.job_row_nth(num) + ' div:nth-child(6) > select'

    @classmethod
    def edit_job_nth(cls, num: int):
        return cls.job_row_nth(num) + ' div:nth-child(4) button'

    @classmethod
    def job_title_nth(cls, num: int):
        return cls.job_row_nth(num) + ' div:nth-child(4) a'


