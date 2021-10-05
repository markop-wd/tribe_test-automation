import os

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait

from helpers import utils
from suites.base_test import BaseTest
from css_selectors import ProjectSetup as proj_css


class TestProjectSetupUnit(BaseTest):
    """
    Basic authentication suite
    """

    def setUp(self) -> None:
        super(TestProjectSetupUnit, self).setUp()
        super(TestProjectSetupUnit, self).login()

    def tearDown(self) -> None:
        super(TestProjectSetupUnit, self).tearDown()

    def test_page_load(self):
        proj_row_first = ec.visibility_of_element_located((By.CSS_SELECTOR, proj_css.job_row_nth(1)))
        WdWait(self.driver, 10).until(proj_row_first)

    def test_job_add_popup(self):
        job_popup = ec.visibility_of_element_located((By.CSS_SELECTOR, proj_css.job_add_popup))
        self.driver.find_element(by=By.CSS_SELECTOR, value=proj_css.job_add_button).click()
        WdWait(self.driver, 10).until(job_popup)

    def test_company_add_popup(self):
        company_popup = ec.visibility_of_element_located((By.CSS_SELECTOR, proj_css.company_add_popup))
        self.driver.find_element(by=By.CSS_SELECTOR, value=proj_css.company_add_button).click()
        WdWait(self.driver, 10).until(company_popup)

    def test_job_edit_popup(self):
        edit_job_button_ec = ec.visibility_of_element_located((By.CSS_SELECTOR, proj_css.edit_job_nth(1)))
        edit_popup_ec = ec.visibility_of_element_located((By.CSS_SELECTOR, proj_css.job_edit_popup))

        edit_job_button = WdWait(self.driver, 10).until(edit_job_button_ec)
        edit_job_button.click()
        WdWait(self.driver, 10).until(edit_popup_ec)
