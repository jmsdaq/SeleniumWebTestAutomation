from page_objects.login import LoginPage
from page_objects.user import UserPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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
        self.sleep(2)
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
        self.sleep(2)
        self.assert_element(self.ERRORS)  # Ensure errors element is present

        # TEST VALID INPUT
        # Generate fake user data using the helper method
        user_data = self.generate_fake_user_data()

        # Fill in the form fields with generated fake data
        # self.type(self.NAME, user_data['name'])
        self.type(self.NAME, "intern_james")
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

        # CHECK NO MATCHING RECORD FOUND
        wait = WebDriverWait(self.driver, 10)
        search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEARCH)))
        self.driver.execute_script("arguments[0].scrollIntoView();", search_input)

        search_input.send_keys("Hefefhsocnciasfhosd")
        self.sleep(2)
        empty_message = self.find_element(self.EMPTY_TABLE)
        self.assertTrue(empty_message.is_displayed(), "No matching records message is not displayed")
        self.sleep(3)

        # TEST SEARCH
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

        search_input = self.find_element(self.SEARCH)
        search_input.send_keys(Keys.CONTROL + 'a')  # Select all text in the input field
        self.sleep(1)
        search_input.send_keys(Keys.BACKSPACE)       # Delete the selected text

        # TEST SHOW ENTRIES
        select_element = self.find_element(self.SHOW)

        # Define a list of option values to test, including "-1" for "All" option
        option_values = ["10", "50", "100", "-1"]

        for option_value in option_values:
            # Click the 'Show Entries' dropdown and select the current option value
            select_element.click()
            self.click(f"option[value='{option_value}']")

            self.sleep(3)
            # Scroll down to the bottom of the page to load all content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.sleep(2)  # Add a short delay to ensure the content is fully loaded

            # Wait for the table content to load after scrolling (adjust timeout as needed)
            self.wait_for_element("#app-users tbody tr")

            # Find all table rows within the table body
            table_rows = self.find_elements("#app-users tbody tr")

            # Determine the expected number of rows based on the selected option value
            if option_value == "-1":
                expected_row_count = len(table_rows)  # All rows should be displayed
            else:
                expected_row_count = int(option_value)  # Convert to integer

            # Get the actual number of rows displayed on the page
            actual_row_count = len(table_rows)

            # Assert that the actual row count is less than or equal to the expected row count
            assert actual_row_count <= expected_row_count, (
                f"Expected {expected_row_count} rows or fewer, but found {actual_row_count} rows for option value '{option_value}'"
            )

            # Scroll back up to the top of the page for the next iteration
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.sleep(1)  # Add a short delay to ensure scrolling is complete
    
        self.sleep(3)
        # Click the column header to trigger sorting
        name_column_header = self.find_element(By.XPATH, '//th[contains(text(), "Name")]')
        name_column_header.click()

        # Wait for the table content to reload after sorting (adjust timeout as needed)
        self.wait_for_element("#app-users tbody tr")

        # Find all visible rows in the table
        visible_rows = self.find_elements("#app-users tbody tr")

        # Scroll to the last visible row to observe the sorting result
        if visible_rows:
            last_visible_row = visible_rows[-1]
            self.driver.execute_script("arguments[0].scrollIntoView();", last_visible_row)
            self.sleep(1)  # Add a short delay to allow scrolling to complete

            # Extract the necessary data (e.g., names) for comparison
            first_row_name = visible_rows[0].find_element(By.XPATH, "./td[1]").text
            last_row_name = last_visible_row.find_element(By.XPATH, "./td[1]").text

            # Assert that the first row's name is less than or equal to the last row's name
            assert first_row_name <= last_row_name, "Sorting order is incorrect"
        else:
            # Handle case where no rows are visible after sorting
            raise AssertionError("No visible rows found after sorting")