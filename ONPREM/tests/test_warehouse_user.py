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

        # Click the Add New User Button
        self.click(self.ADD_BTN)
        

        # Generate fake user data using the helper method
        user_data = self.generate_fake_user_data()

        # Fill in the form fields with generated fake data
        self.type(self.NAME, user_data['name'])
        self.type(self.EMPLOYEE_CODE, str(user_data['employee_code']))
        self.type(self.USERNAME, user_data['username'])
        self.type(self.PASSWORD, user_data['password'])
        self.type(self.PIN, str(user_data['pin']))
        self.select_option_by_text(self.OPERATIONAL_ROLE, user_data['operation_role'])


        # Assert Valid Input
        # self.click

        # Assert Invalid Input


        # Assert Duplicate Input
        self.click(self.SUBMIT)