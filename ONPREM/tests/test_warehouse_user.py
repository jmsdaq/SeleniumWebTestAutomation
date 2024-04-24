from page_objects.user import UserPage
from page_objects.login import LoginPage
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



class WarehouseUserTest(LoginPage, UserPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.login()

    def tearDown(self):
        self.sleep(10) 
        super().tearDown()

    def test_warehouse_users(self):
        self.assert_element(self.SIDEBAR_ACTIVE)  # Verify if the sidebar is active (from PartnersPage)
        self.click(self.USER_MENU)  # Click on the Partner Accounts menu (from PartnersPage)
        self.click(self.WAREHOUSE_MENU) 
        self.wait_for_element(self.WAREHOUSE_MENU)

        # wait

        # Click the Close Icon for the Modal2
        self.click(self.ADD_BTN)
        self.wait_for_element(self.MODAL)
        self.click(self.CLOSE_ICON)

        # Click the Close Button for the Modal
        self.click(self.ADD_BTN)
        self.wait_for_element(self.MODAL)
        # Find an element towards the bottom of the page (e.g., footer)
        # Call the scroll function to scroll down using ActionChains
        bottom_element = self.find_element(self.FOOTER)
        self.scroll_with_actions(bottom_element)
        self.wait_for_element(self.CLOSE_BTN)
        self.click(self.CLOSE_BTN)
        

        self.click(self.ADD_BTN)
        self.wait_for_element(self.MODAL)
        self.type(self.EMPLOYEE_CODE, "test")
        bottom_element = self.find_element(self.FOOTER)
        self.scroll_with_actions(bottom_element)
        self.click(self.SUBMIT)
        
        header_element = self.find_element(self.HEADER)
        self.scroll_with_actions(header_element)
        self.assert_element(self.ERRORS)  # Ensure errors element is present

        # # Generate fake user data using the helper method
        # user_data = self.generate_fake_usesr_data()

        # # Fill in the form fields with generated fake data
        # self.type(self.NAME, user_data['name'])
        # self.type(self.EMPLOYEE_CODE, str(user_data['employee_code']))
        # self.type(self.USERNAME, user_data['username'])
        # self.type(self.PASSWORD, user_data['password'])
        # self.type(self.PIN, str(user_data['pin']))
        # self.select_option_by_text(self.OPERATIONAL_ROLE, user_data['operation_role'])


        # Assert Valid Input
        # self.click

        # Assert Invalid Input


        # Assert Duplicate Input
        # self.click(self.SUBMIT)