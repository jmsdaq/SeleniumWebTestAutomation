from page_objects.login import LoginPage
from page_objects.user import UserPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        self.scroll_to(self.CLOSE_BTN) # scroll down method
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
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEARCH)))

        search_input.clear()
        search_input.send_keys(username)

        # Wait for the table rows to update based on the search query (wait for presence of table rows)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.TABLE_ROWS)))

        # Get all table rows within the table body
        table_rows = self.driver.find_elements(By.XPATH, '//*[@id="app-users"]/tbody/tr')

        # Assert that the table has more than 0 rows after search
        self.assertGreater(len(table_rows), 0, "Table does not contain any rows after search.")
        self.sleep(3)

        #UPDATE USER'S AVATAR
        # Construct the absolute path to the file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.abspath(os.path.join(current_dir, '..', 'data', 'avatar.jpg'))
        self.click(self.AVATAR)
        self.wait_for_element_visible(self.MODAL)
        # Wait for the file upload input to be clickable
        wait = WebDriverWait(self.driver, 10)
        upload_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.CHOOSE_IMG)))
        
        # Upload the file using JavaScript to set the file path directly
        self.driver.execute_script('arguments[0].style = ""; arguments[0].style.display = "block";', upload_input)
        # upload_input.send_keys(file_path)
        upload_input.send_keys(file_path)

        self.click(self.SUBMIT)
        self.assert_text("User picture has been updated successfully!", self.POPUP)