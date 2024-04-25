from page_objects.login import LoginPage
from page_objects.user import UserPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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

    # def perform_search(self, username):
    #     self.wait_for_element(self.SEARCH)
    #     search_input = self.find_element(self.SEARCH)
    #     search_input.clear()
    #     search_input.send_keys(username)
    #     search_input.submit()

    def test_warehouse_users(self):
        
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE)  # Verify if the sidebar is active (from PartnersPage)
        self.click(self.USER_MENU)  # Click on the Partner Accounts menu (from PartnersPage)
        self.wait_for_element(self.WAREHOUSE_MENU)
        self.click(self.WAREHOUSE_MENU) 
        

        # CLICK CLOSE ICON
        self.wait_for_element(self.ADD_BTN)
        self.click(self.ADD_BTN)
        self.wait_for_element(self.MODAL)
        self.click(self.CLOSE_ICON)

        # CLICK THE CLOSE BUTTON
        self.click(self.ADD_BTN)
        self.wait_for_element(self.MODAL)
        self.scroll_down() # scroll down method
        self.wait_for_element(self.CLOSE_BTN)
        self.click(self.CLOSE_BTN)
        
        # TEST ERRORS IN ADDING NEW USER
        self.click(self.ADD_BTN)
        self.wait_for_element(self.MODAL)
        self.type(self.EMPLOYEE_CODE, "test")
        self.scroll_down() # scroll down method
        self.click(self.SUBMIT)
        self.scroll_up()
        self.assert_element(self.ERRORS)  # Ensure errors element is present

        # TEST VALID INPUT
        # Generate fake user data using the helper method
        user_data = self.generate_fake_user_data()

        # Fill in the form fields with generated fake data
        self.type(self.NAME, user_data['name'])
        self.type(self.EMPLOYEE_CODE, str(user_data['employee_code']))
        username = user_data['username']  # Store the generated username
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, user_data['password'])
        self.type(self.PIN, str(user_data['pin']))
        self.select_option_by_text(self.OPERATIONAL_ROLE, user_data['operation_role'])
        self.click(self.SUBMIT)
        self.sleep(2)

        # Print the generated username
        print("Generated Username:", username)
        # Now you can use the generated username for interaction with the search input
        # Wait for the search input to be visible and interactable
        wait = WebDriverWait(self.driver, 10)
        search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEARCH)))
        self.driver.execute_script("arguments[0].scrollIntoView();", search_input)

        search_input.clear()
        search_input.send_keys(username)

        self.wait_for_element_present("#app-users_wrapper")
        # Check if the search input is displayed
        self.assertTrue(search_input.is_displayed())
        # Wait for the user list table to load
        self.wait_for_element_present(self.TABLE)

        # Verify that the expected user row is visible in the table
        user_row_xpath = f'//tr[contains(.//td, "{username}")]'
        self.assertTrue(self.is_element_present(user_row_xpath), f"User with username '{search_query}' not found in the table")
        
        # Clear the search input
        search_input.clear()

        search_input.send_keys("Hefefhsocnciasfhosd")
        # Check if the "No matching records found" message is displayed
        empty_message = self.find_element(".dataTables_empty")
        self.assertTrue(empty_message.is_displayed(), "No matching records message is not displayed")