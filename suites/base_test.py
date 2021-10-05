import os
from unittest import TestCase

from dotenv import load_dotenv
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from webdriver_manager.chrome import ChromeDriverManager

from helpers import utils
from css_selectors import Auth as auth_css
from css_selectors import General as gen_css


class BaseTest(TestCase):

    def setUp(self) -> None:
        options = Options()
        options.headless = True
        os.environ['WDM_LOG_LEVEL'] = '0'
        os.environ['WDM_PRINT_FIRST_LINE'] = 'False'
        self.driver = Chrome(executable_path=ChromeDriverManager().install(),
                             options=options)
        self.driver.set_window_size(1920, 1080)
        self.driver.maximize_window()
        self.driver.get('https://overview.tribe.xyz/')
        WdWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, gen_css.main_page)))

    def tearDown(self) -> None:
        # TODO - customize the name of the test_screenshot so it is instead the name of the test that called it + time
        try:
            self.driver.save_screenshot('test_screenshot1.png')
        except UnexpectedAlertPresentException:
            # TODO - save at least the text of the alert if it can't be screenshot
            self.driver.save_screenshot('test_screenshot2.png')

        self.driver.quit()

    def login(self):
        main_page_cond = ec.visibility_of_element_located((By.CSS_SELECTOR, gen_css.main_header))

        dot_env = utils.get_dot_env()
        load_dotenv(dot_env)
        email = os.environ.get('tribe_regular_email')
        password = os.environ.get('tribe_regular_password')

        self.driver.find_element(by=By.CSS_SELECTOR, value=auth_css.email_input).send_keys(email)
        self.driver.find_element(by=By.CSS_SELECTOR, value=auth_css.password_input).send_keys(password)
        self.driver.find_element(by=By.CSS_SELECTOR, value=auth_css.login_button).click()
        WdWait(self.driver, 10).until(main_page_cond)

