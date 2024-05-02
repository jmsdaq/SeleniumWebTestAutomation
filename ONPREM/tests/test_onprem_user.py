from page_objects.login import LoginPage
from page_objects.user import UserPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import os

class WarehouseUserTest(LoginPage, UserPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.login()

    def tearDown(self):
        self.sleep(10) 
        super().tearDown()

    # >>>>>>>>>>>>>>>>>>>>> NAVIGATION TO WAREHOUSE USER WITHIN USER MENU <<<<<<<<<<<<<<<<<<<<<<<<
    def test_warehouse_user(self):
        self.onprem_user_nav()
    
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ADD WAREHOUSE USER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # def test_other(self):
        # CLICK CLOSE ICON
        # self.wait_for_element(self.ADD_BTN)

        wait = WebDriverWait(self.driver, 10)
        add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ADD_BTN)))
        add_btn.click()
        self.wait_for_element(self.ADD_USER_PAGE)
        self.assert_text("New OnPrem User", "h5")
        self.sleep(2)

        # TEST REQUIRED FIELD
        onprem_data = self.generate_fake_onprem_data()
        self.type(self.ON_USERNAME, "intern_james")
        self.type(self.ON_PW, "intern_james")
        self.click(self.SUBMIT)
        self.sleep(2)

        # TEST ALL ERRORS IN ADDING NEW USER
        self.type(self.ON_USERNAME, "intern_james")
        self.type(self.ON_PW, "intern_james")
        self.click(self.ON_ROLE)
        self.select_option_by_text(self.ON_ROLE, onprem_data['role'])
        self.click(self.SUBMIT)

        self.sleep(2)
        self.assert_element(self.DANGER)  # Ensure errors element is present

        # TEST VALID USER DATA
        password = "intern_james"
        username = onprem_data['username']
        self.type(self.ON_USERNAME, username)
        self.type(self.ON_NAME, onprem_data['name'])
        self.type(self.ON_PW, password)
        self.type(self.ON_PW_CONF, password)
        self.select_option_by_text(self.ON_ROLE, onprem_data['role'])
        self.click(self.SUBMIT)
        self.sleep(2)

        # >>>>>>>>>>>>>>>>>>>>> TEST SEARCH <<<<<<<<<<<<<<<
        # Wait for the search input to be visible and interactable
        wait = WebDriverWait(self.driver, 10)
        search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ON_SEARCH)))
        self.driver.execute_script("arguments[0].scrollIntoView();", search_input)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ON_SEARCH)))

        search_input.clear()
        search_input.send_keys(username)

        # Wait for the table rows to update based on the search query (wait for presence of table rows)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.TABLE_ROWS)))

        # Get all table rows within the table body
        table_rows = self.driver.find_elements(By.XPATH, '//*[@id="app-users"]/tbody/tr')

        # Assert that the table has more than 0 rows after search
        self.assertGreater(len(table_rows), 0, "Table does not contain any rows after search.")
        self.sleep(3)

        # # TEST VALID INPUT
        # # Generate fake user data using the helper method
        # user_data = self.generate_fake_user_data()

        # # Fill in the form fields with generated fake data
        # # self.type(self.NAME, user_data['name'])
        # self.type(self.NAME, "intern_james")
        # self.type(self.EMPLOYEE_CODE, str(user_data['employee_code']))
        # username = user_data['username']  # Store the generated username
        # self.type(self.USERNAME, username)
        # self.type(self.PASSWORD, user_data['password'])
        # self.type(self.PIN, str(user_data['pin']))
        # self.select_option_by_text(self.OPERATIONAL_ROLE, user_data['operation_role'])
        # self.click(self.SUBMIT)
        # self.sleep(2)

        # # Print the generated username
        # print("Generated Username:", username)