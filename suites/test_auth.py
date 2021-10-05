"""
Current Test Suite For Authentication
"""
import datetime
import os

from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from dotenv import load_dotenv

from email_handler import MailParser
from suites.base_test import BaseTest


class TestLoginPage(BaseTest):
    """
    Basic authentication suite
    """
    main_page_cond = ec.visibility_of_element_located((By.CSS_SELECTOR, 'div#main_header'))

    def setUp(self) -> None:
        super(TestLoginPage, self).setUp()
        load_dotenv('../.env')

    def tearDown(self) -> None:
        super(TestLoginPage, self).tearDown()

    def test_positive(self):
        """
        Valid login attempt
        :return:
        """
        email = os.environ.get('tribe_regular_email')
        password = os.environ.get('tribe_regular_password')
        self.driver.find_element(by=By.ID, value='email').send_keys(email)
        self.driver.find_element(by=By.ID, value='password').send_keys(password)
        self.driver.find_element(by=By.CSS_SELECTOR, value='button.Button').click()
        WdWait(self.driver, 10).until(self.main_page_cond)

    def test_negative(self):
        """
        Attempting to login with a correct e-mail and a bad password
        :return:
        """
        self.driver.find_element(by=By.ID, value='email').send_keys('bad@email.com')
        self.driver.find_element(by=By.ID, value='password').send_keys('test')
        self.driver.find_element(by=By.CSS_SELECTOR, value='button.Button').click()
        WdWait(self.driver, 10).until(ec.alert_is_present())
        alert = self.driver.switch_to.alert
        self.assertEqual('We didn’t find an account with those login credentials', alert.text)
        alert.driver
        alert.dismiss()

    def test_empty(self):
        """
        Attempting to login without an e-mail or password
        :return:
        """
        self.driver.find_element(by=By.CSS_SELECTOR, value='button.Button').click()
        WdWait(self.driver, 10).until(ec.alert_is_present())
        alert_text = self.driver.switch_to.alert.text
        self.assertEqual('Please include an email', alert_text)

    # TODO - store the valid password for the account before and after the reset

    def test_forgot_pass(self):
        """
        Testing forgot/reset password functionality
        :return:
        """
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

