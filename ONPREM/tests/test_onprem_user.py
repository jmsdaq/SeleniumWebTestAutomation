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

    # >>>>>>>>>>>>>>>>>>>>> NAVIGATION TO ONPREM USER WITHIN USER MENU <<<<<<<<<<<<<<<<<<<<<<<<
    def test_warehouse_user(self):
        self.onprem_user_nav()
    
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ADD ONPREM USER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # def test_other(self):
        # CLICK CLOSE ICON
        # self.wait_for_element(self.ADD_BTN)

        wait = WebDriverWait(self.driver, 10)
        add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ADD_BTN)))
        add_btn.click()
        self.wait_for_element(self.CARD_TITLE)
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

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>> SEARCH <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # CHECK NO MATCHING RECORD FOUND
        wait = WebDriverWait(self.driver, 10)
        search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ON_SEARCH)))

        search_input.send_keys("Hefefhsocnciasfhosd")
        self.sleep(2)
        empty_message = self.find_element(self.EMPTY_TABLE)
        self.assertTrue(empty_message.is_displayed(), "No matching records message is not displayed")
        self.sleep(3)

        # TEST MATCH
        # Wait for the search input to be visible and interactable
        wait = WebDriverWait(self.driver, 10)
        search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ON_SEARCH)))
        self.driver.execute_script("arguments[0].scrollIntoView();", search_input)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ON_SEARCH)))

        search_input.clear()
        search_input.send_keys(username)

        # Wait for the table rows to update based on the search query (wait for presence of table rows)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.ON_TABLE_ROWS)))

        # Get all table rows within the table body
        table_rows = self.driver.find_elements(By.XPATH, '//*[@id="nadmin-users"]/tbody/tr')

        # Assert that the table has more than 0 rows after search
        self.assertGreater(len(table_rows), 0, "Table does not contain any rows after search.")
        self.sleep(3)

        search_input = self.find_element(self.ON_SEARCH)
        search_input.send_keys(Keys.CONTROL + 'a')  # Select all text in the input field
        self.sleep(1)
        search_input.send_keys(Keys.BACKSPACE)       # Delete the selected text
        self.sleep(1)


        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SHOWING A SPECIFIC NUMBER OF ENTRIES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        select_element = self.find_element(self.ON_SHOW)
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
            self.wait_for_element("#nadmin-users tbody tr")

            # Find all table rows within the table body
            table_rows = self.find_elements("#nadmin-users tbody tr")

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

            # Get the text of the element indicating the number of entries shown
            entries_info = self.find_element("#nadmin-users_info").text

            # Extract the numbers indicating the range of entries shown
            shown_entries = [int(s) for s in entries_info.split() if s.isdigit()]

            # Extract the expected upper limit of the range based on the selected option value
            expected_upper_limit = min(expected_row_count, actual_row_count)

            # Check if the displayed range matches the selected option value
            assert shown_entries[:2] == [1, expected_upper_limit], (
                f"Expected to show 1 to {expected_upper_limit} entries, "
                f"but found {entries_info}"
            )

            # Scroll back up to the top of the page for the next iteration
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.sleep(1)  # Add a short delay to ensure scrolling is complete
        self.sleep(3)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SORTING TABLE COLUMN <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # def test_sorting_table_column(self):
    #     self.warehouse_nav()

        # Click the column header to trigger sorting
        name_column_header = self.find_element(By.XPATH, '//th[contains(text(), "Username")]')
        name_column_header.click()

        # Wait for the table content to reload after sorting (adjust timeout as needed)
        wait = WebDriverWait(self.driver, 3)  # Adjust timeout as needed
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nadmin-users tbody tr")))

        # Find all visible rows in the table
        visible_rows = self.find_elements("#nadmin-users tbody tr")

            # Refresh the list of visible rows after sorting
        try:
            visible_rows = self.find_elements("#nadmin-users tbody tr")
        except StaleElementReferenceException:
            pass

        # Scroll to the last visible row to observe the sorting result
        if visible_rows:
            last_visible_row = visible_rows[-1]
            self.driver.execute_script("arguments[0].scrollIntoView();", last_visible_row)
            # self.sleep(1)  # Add a short delay to allow scrolling to complete

            # Extract the necessary data for comparison
            first_row_name = visible_rows[0].find_element(By.XPATH, "./td[1]").text
            last_row_name = last_visible_row.find_element(By.XPATH, "./td[1]").text

            # Assert that the first row's name is less than or equal to the last row's name
            assert first_row_name <= last_row_name, "Sorting order is incorrect"

        else:
            # Ha    ndle case where no rows are visible after sorting
            raise AssertionError("No visible rows found after sorting")
        
        self.sleep(3)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> EDIT TABLE ROW <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # def test_edit(self):
        # self.test_warehouse_users()

        self.scroll_up_header()
        # Locate the dropdown toggle button
        # Use WebDriverWait to wait for the element to be present and visible
        wait = WebDriverWait(self.driver, 10)  # Adjust timeout as needed
        dropdown_toggle = wait.until(EC.visibility_of_element_located((By.XPATH, self.ON_TR1)))

        # Click the dropdown toggle button to open the dropdown menu    
        self.click(self.ON_TR1)
        self.sleep(2)

        # Wait for the dropdown menu to appear
        dropdown_menu_xpath = f'//*[@id="nadmin-users"]/tbody/tr[1]/td[6]/div/div'
        dropdown_menu = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, dropdown_menu_xpath)))

        # Locate the "Edit" and "Delete" links within the dropdown menu
        # edit_link = self.element(f'{dropdown_menu} a.dropdown-item[text()="Edit"]')
        edit_link = dropdown_menu.find_element(By.XPATH, './/a[contains(@class, "dropdown-item") and contains(text(), "Edit")]')

        # Click the "Edit" link
        edit_link.click()
        # self.wait_for_element(self.CARD _TITLE)
        # self.scroll_up()
        self.assert_text("Edit OnPrem User", "h5")
        self.select_option_by_text(self.ON_ROLE, onprem_data['role'])
        self.click(self.UPDATE_BTN)
        self.assert_text("User updated!", self.POPUP)
        self.sleep(3)


    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DELETE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # def test_delete(self):
    #     self.warehouse_nav()
        # Perform assertions 
        self.scroll_to(self.ON_TR1)
        dropdown_toggle_xpath = self.ON_TR1

        # Use WebDriverWait to wait for the element to be present and visible
        wait = WebDriverWait(self.driver, 10)  # Adjust timeout as needed
        dropdown_toggle = wait.until(EC.visibility_of_element_located((By.XPATH, self.ON_TR1)))

        # Click the dropdown toggle button to open the dropdown menu    
        dropdown_toggle.click()

        # Wait for the dropdown menu to appear
        dropdown_menu_xpath = f'//*[@id="nadmin-users"]/tbody/tr[1]/td[6]/div/div'
        dropdown_menu = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, dropdown_menu_xpath)))

        # Locate the "Edit" and "Delete" links within the dropdown menu
        delete_link = dropdown_menu.find_element(By.XPATH, './/a[contains(@class, "dropdown-item") and contains(text(), "Delete")]')
        delete_link.click()
        
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert     # Switch to the alert dialog
        dialog_text = alert.text    # Retrieve the text of the confirmation dialog
    
        # Assert or check the text of the confirmation dialog
        expected_text = "Delete user?"
        assert expected_text in dialog_text

        alert.accept()
        self.assert_element_visible(self.POPUP)
        self.sleep(3)

        #>>>>>>>>>>>>>>>>>>>>> ONPREM: USER ABILITIES <<<<<<<<<<<<<<<<<<<
        self.click(self.ABILITIES)
        self.assert_text("Onprem Abilities", "h5")