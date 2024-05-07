from page_objects.login import LoginPage
from page_objects.user import UserPage
from page_objects.export import ExportPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import os

class ExportTest(LoginPage, UserPage, ExportPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.login()

    def tearDown(self):
        self.sleep(10) 
        super().tearDown()

    def test_export(self):
        self.export_nav()
        