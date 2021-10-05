import os

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as WdWait

from helpers import utils
from suites.base_test import BaseTest


class TestProjectSetupSystem(BaseTest):
    """
    Basic authentication suite
    """

    def setUp(self) -> None:
        super(TestProjectSetupSystem, self).setUp()
        super(TestProjectSetupSystem, self).login()

    def tearDown(self) -> None:
        super(TestProjectSetupSystem, self).tearDown()

