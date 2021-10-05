import os

from unittest import TestCase

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

from suites.base_test import BaseTest


class TestLoginPage(BaseTest):
    """
    Basic authentication suite
    """
    main_page_cond = ec.visibility_of_element_located((By.CSS_SELECTOR, 'div#main_header'))

    def setUp(self) -> None:
        super(TestLoginPage, self).setUp()
        load_dotenv('../.env')
        email = os.environ.get('tribe_regular_email')
        password = os.environ.get('tribe_regular_password')
        self.driver.find_element(by=By.ID, value='email').send_keys(email)
        self.driver.find_element(by=By.ID, value='password').send_keys(password)
        self.driver.find_element(by=By.CSS_SELECTOR, value='button.Button').click()

    def tearDown(self) -> None:
        super(TestLoginPage, self).tearDown()

    def test_page_load(self):
        WdWait(self.driver, 10).until(self.main_page_cond)

    def test_add_job_popup(self):
        pass
