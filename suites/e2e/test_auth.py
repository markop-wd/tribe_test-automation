"""
Current Test Suite For Authentication
"""
import datetime
import os
from time import sleep

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait

from helpers import utils
from helpers.email_handler import MailParser
from suites.base_test import BaseTest


class TestLoginPage(BaseTest):
    """
    Basic authentication suite
    """
    main_page_cond = ec.visibility_of_element_located((By.CSS_SELECTOR, 'div#main_header'))

    def setUp(self) -> None:
        super(TestLoginPage, self).setUp()

    def tearDown(self) -> None:
        super(TestLoginPage, self).tearDown()

    def test_forgot_pass(self):
        """
        Testing forgot/reset password functionality
        :return:
        """
        dot_env = utils.get_dot_env()
        load_dotenv(dot_env)
        forgot_email = os.environ.get('gmail_username')
        run_start_time = datetime.datetime.now(tz=datetime.timezone.utc)

        self.driver.find_element(by=By.ID, value="forgot_password").click()
        email_input = WdWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                      'div.Popup input[type="email"]')))
        email_input.send_keys(forgot_email)
        self.driver.find_element(by=By.CSS_SELECTOR, value='div.Popup > div:nth-child(3) button').click()
        WdWait(self.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div#popup_forgot_sent')))
        email_sent_text = self.driver.find_element(by=By.CSS_SELECTOR,
                                                   value='div#popup_forgot_sent div.content').text
        assert email_sent_text == 'Email sent successfully.'
        sleep(3)
        link_to_go_to = MailParser().run(run_start_time)
        self.driver.get(link_to_go_to)
        WdWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'password_reset_box')))
        self.driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="New password"]').send_keys('testTEST1')
        self.driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Confirmation"]').send_keys('testTEST1')
        self.driver.find_element(by=By.ID, value='password_change_btn').click()
        WdWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div#main_header')))
