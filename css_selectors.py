# NOTE - For a particular element use div#job_group > div.GroupItem:nth-child(1)
# NOTE - nth-child for the above is increasing in increments of 2
general = {
    'main_header': 'div#main_header'
}

project_setup = {
    'company_search': 'input[placeholder="Search a company"]',
    'add_company': 'div[title="Add / Edit Client"]',
    'add_job': 'button#job_add',
    'show_archived': 'select#archived_select',
    'archive': 'div#job_group > div.GroupItem button[title="Archive this job"]',
    'job_sequence': 'div#job_group > div.GroupItem div:nth-child(8) a',
    'recruiter': 'div#job_group > div.GroupItem div:nth-child(5) > select',
    'manager': 'div#job_group > div.GroupItem div:nth-child(6) > select',
    'edit_job': 'div#job_group > div.GroupItem div:nth-child(4) button',
    'job_title': 'div#job_group > div.GroupItem div:nth-child(4) a'
}
