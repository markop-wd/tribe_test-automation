"""
Current Test Suite For Authentication
"""
import os

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait

from suites.base_test import BaseTest
from helpers import utils


class TestLoginPage(BaseTest):
    """
    Basic authentication suite
    """
    main_page_cond = ec.visibility_of_element_located((By.CSS_SELECTOR, 'div#main_header'))

    def setUp(self) -> None:
        super(TestLoginPage, self).setUp()

    def tearDown(self) -> None:
        super(TestLoginPage, self).tearDown()

    def test_positive(self):
        """
        Valid login attempt
        :return:
        """
        dot_env = utils.get_dot_env()
        load_dotenv(dot_env)
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
