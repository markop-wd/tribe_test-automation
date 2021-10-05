from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from unittest import TestCase


class BaseTest(TestCase):

    def setUp(self) -> None:
        options = Options()
        options.headless = True
        self.driver = Chrome(executable_path=ChromeDriverManager(log_level=0, print_first_line=False).install(),
                             options=options)
        self.driver.set_window_size(1920, 1080)
        self.driver.maximize_window()
        self.driver.get('https://overview.tribe.xyz/')
        WdWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.main-page')))

    def tearDown(self) -> None:
        # TODO - customize the name of the test_screenshot so it is instead the name of the test that called it + time
        try:
            self.driver.save_screenshot('test_screenshot1.png')
        except UnexpectedAlertPresentException:
            # TODO - save at least the text of the alert if it can't be screenshot
            self.driver.save_screenshot('test_screenshot2.png')

        self.driver.quit()
