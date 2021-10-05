general = {
    'main_header': 'div#main_header'
}

auth = {
    'forgot_pw_init_link': 'div#forgot_password',
    'reset_mail_input': 'div.Popup input[type="email"]',
    'reset_mail_button': 'div.Popup > div:nth-child(3) button',
    'after_reset_popup_text': 'div#popup_forgot_sent div.content'
}

reset_pw = {
    'change_pw_btn': 'button#password_change_btn',
    'first_pw_input': 'input[placeholder="New password"]',
    'second_pw_input': 'input[placeholder="Confirmation"]'
}

project_setup = {
    'company_search': 'input[placeholder="Search a company"]',
    'company_add_button': 'button#company_add',
    'company_add_popup': 'div#company_add_popup',
    'job_add_popup': 'div#job_create_popup',
    'job_add_button': 'button#job_add',
    'show_archived': 'select#archived_select',
    # NOTE - For a particular (X) element use div#job_group > div.GroupItem:nth-child(X)
    # nth-child for the above is increasing in increments of 2 starting from 1
    'archive': 'div#job_group > div.GroupItem button[title="Archive this job"]',
    'job_sequence': 'div#job_group > div.GroupItem div:nth-child(8) a',
    'recruiter': 'div#job_group > div.GroupItem div:nth-child(5) > select',
    'manager': 'div#job_group > div.GroupItem div:nth-child(6) > select',
    'edit_job': 'div#job_group > div.GroupItem div:nth-child(4) button',
    'job_title': 'div#job_group > div.GroupItem div:nth-child(4) a'
}
