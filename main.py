import datetime
import os

from mail_test import MailParser

import unittest
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from dotenv import load_dotenv


class TestLoginPage(unittest.TestCase):

    main_page_cond = ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search by name"]'))

    def setUp(self) -> None:
        load_dotenv('.env')
        self.email = os.environ.get('email')
        self.password = os.environ.get('password')
        self.email = os.environ.get('reset_pass')

        self.driver = Chrome(executable_path=ChromeDriverManager().install())
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get('https://overview.tribe.xyz/')
        WdWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.main-page')))

    def tearDown(self) -> None:
        self.driver.quit()

    # TODO - Validate the time it took to login
    def test_positive(self):
        self.driver.find_element(by=By.ID, value='email').send_keys(self.email)
        self.driver.find_element(by=By.ID, value='password').send_keys(self.password)
        self.driver.find_element(by=By.CSS_SELECTOR, value='button.Button').click()
        WdWait(self.driver, 10).until(self.main_page_cond)

    def test_negative(self):
        self.driver.find_element(by=By.ID, value='email').send_keys(self.email)
        self.driver.find_element(by=By.ID, value='password').send_keys('test')
        self.driver.find_element(by=By.CSS_SELECTOR, value='button.Button').click()
        WdWait(self.driver, 10).until(ec.alert_is_present())
        alert_text = self.driver.switch_to.alert.text
        self.assertEqual('We didn’t find an account with those login credentials', alert_text)

    def test_empty(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value='button.Button').click()
        WdWait(self.driver, 10).until(ec.alert_is_present())
        alert_text = self.driver.switch_to.alert.text
        self.assertEqual('Please include an email', alert_text)

    # TODO - store the valid password for the account before and after the reset
    def test_forgot_pass(self):
        run_start_time = datetime.datetime.now()
        self.driver.find_element(by=By.ID, value="forgot_password").click()
        email_input = WdWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                      'div.Popup input[type="email"]')))
        email_input.send_keys('marko.pom94@gmail.com')
        self.driver.find_element(by=By.CSS_SELECTOR, value='div.Popup > div:nth-child(3) button').click()
        email_sent_text = self.driver.find_element(by=By.CSS_SELECTOR,
                                                   value='body > div:nth-child(9) > '
                                                         'div:nth-child(1) > div > div > div').text
        assert email_sent_text == 'Email sent successfully.'
        sleep(3)
        # main_handle = self.driver.current_window_handle
        link_to_go_to = MailParser.run(run_start_time)
        self.driver.execute_script(f"window.open({link_to_go_to});")
        input('hello')


if __name__ == '__main__':
    unittest.main()
