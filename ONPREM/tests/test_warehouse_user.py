from page_objects.warehouse_user import WarehouseUserPage
from page_objects.login import LoginPage
from page_objects.onprem_user import OnPremUserPage
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import random
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class WarehouseUserTest(LoginPage, WarehouseUserPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.user()

    def tearDown(self):
        self.sleep(5) 
        super().tearDown()

    def test_warehouse_users(self):
        self.assert_element(self.SIDEBAR_ACTIVE)  # Verify if the sidebar is active (from PartnersPage)
        self.click(self.USER_MENU)  # Click on the Partner Accounts menu (from PartnersPage)
        # self.assert_url(self.PARTNER_URL) # Assert current URL matches PARTNER_URL