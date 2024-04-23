from page_objects.user import UserPage
from page_objects.login import LoginPage
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import random
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class WarehouseUserTest(LoginPage, UserPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.login()

    def tearDown(self):
        self.sleep(5) 
        super().tearDown()

    def test_warehouse_users(self):
        self.assert_element(self.SIDEBAR_ACTIVE)  # Verify if the sidebar is active (from PartnersPage)
        self.click(self.USER_MENU)  # Click on the Partner Accounts menu (from PartnersPage)
        self.click(self.WAREHOUSE_MENU) 

        # wait

        # Create New User 
        self.click(self.ADD_BTN)