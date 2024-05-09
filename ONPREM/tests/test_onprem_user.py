from page_objects.login import LoginPage
from page_objects.user import UserPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import pytest
import os

class OnpremUserTest(LoginPage, UserPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.login()

    def tearDown(self):
        self.sleep(10) 
        super().tearDown()

    # >>>>>>>>>>>>>>>>>>>>> NAVIGATION TO ONPREM USER WITHIN USER MENU <<<<<<<<<<<<<<<<<<<<<<<<
    @pytest.mark.run(order=2)
    def test_onprem_user(self):
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

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>> ONPREM USER: SEARCH <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # CHECK NO MATCHING RECORD FOUND
        wait = WebDriverWait(self.driver, 10)
        search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ON_SEARCH)))

        search_input.send_keys("#")
        self.sleep(2)
        empty_message = self.find_element(self.EMPTY_TABLE)
        self.assertTrue(empty_message.is_displayed(), "No matching records message is not displayed")
        self.assert_text("No matching records found", "td.dataTables_empty")
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

        table_rows = self.driver.find_elements(By.XPATH, '//*[@id="nadmin-users"]/tbody/tr')
        self.assertGreater(len(table_rows), 0, "Table does not contain any rows after search.")
        self.sleep(3)


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ONPREM USER: EDIT TR1 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
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


    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ONPREM USER: DELETE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # def test_delete(self):
    #     self.warehouse_nav()
        # Perform assertions 
        self.scroll_to(self.ON_TR1)

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

        search_input = self.find_element(self.ON_SEARCH)
        search_input.send_keys(Keys.CONTROL + 'a')  # Select all text in the input field
        self.sleep(1)
        search_input.send_keys(Keys.BACKSPACE)       # Delete the selected text
        self.sleep(1)


        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ONPREM USER: SHOW ENTRIES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.show_entries_helper(self.ON_SHOW, self.ON_TABLE_ROWS)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ONPREM USER: SORTING TABLE COLUMN <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # def test_sorting_table_column(self):
    #     self.warehouse_nav()
        self.sorting_helper("Name", "#nadmin-users tbody tr")
        self.sleep(3)
        self.sorting_helper("Username", "#nadmin-users tbody tr")


    #>>>>>>>>>>>>>>>>>>>>> ONPREM ABILITIES <<<<<<<<<<<<<<<<<<<
        self.click(self.ABILITIES)
        self.assert_text("Onprem Abilities", "h5")
        self.sleep(5)


    # #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ONPREM ROLE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # def test_role(self):
    #     onprem_data = self.generate_fake_onprem_data()
        # self.onprem_user_nav()

        # TEST ERRORS
        self.click(self.ROLE)
        self.assert_text("OnPrem Roles", "h5")
        self.click(self.ADD_BTN)
        self.type(self.ROLE_NAME, "Test")
        self.click(self.SUBMIT)
        self.sleep(3)

        self.assert_element(self.ERRORS)  # Ensure errors element is present

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>> ONPREM ROLE: ADD NEW ROLE <<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # TEST VALID ADD ROLE
        name = onprem_data['name']
        self.type(self.ROLE_NAME, name)
        self.type(self.ROLE_DESC, "Test")

        self.wait_for_element_visible(".form-group")
        # Get all the ability list checkboxes
        ability_checkboxes = self.find_elements("input[type='checkbox'][name='nadmin_role[ability_list][]']")

        # Iterate through each checkbox and click on it
        for checkbox in ability_checkboxes:
            checkbox.click()

        self.click(self.SUBMIT)
        self.assert_text("Role created successfully!", "h2")
        self.sleep(4)

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ONPREM ROLE: SEARCH <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # CHECK NO MATCHING RECORD FOUND
        wait = WebDriverWait(self.driver, 10)
        search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ROLE_SEARCH)))
        # self.driver.execute_script("arguments[0].scrollIntoView();", search_input)

        search_input.send_keys("#")
        self.sleep(2)
        empty_message = self.find_element(self.EMPTY_TABLE)
        self.assertTrue(empty_message.is_displayed(), "No matching records message is not displayed")
        self.assert_text("No matching records found", "td.dataTables_empty")
        self.sleep(3)

        # TEST SEARCH
        # Wait for the search input to be visible and interactable
        search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ROLE_SEARCH)))
        self.driver.execute_script("arguments[0].scrollIntoView();", search_input)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ROLE_SEARCH)))

        search_input.clear()
        search_input.send_keys(name)

        # Wait for the table rows to update based on the search query (wait for presence of table rows)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.ROLE_TABLE_ROWS)))

        # Get all table rows within the table body
        table_rows = self.driver.find_elements(By.XPATH, '//*[@id="nadmin-roles"]/tbody/tr')

        # Assert that the table has more than 0 rows after search
        self.assertGreater(len(table_rows), 0, "Table does not contain any rows after search.")
        self.sleep(3)

        self.click(self.ROLE_ABILITIES)
        self.assert_element(self.MODAL)
        expected_title = name
        actual_title = self.get_text("h1")
        self.assert_equal(actual_title, expected_title)
        self.sleep(2)
        self.click(self.CLOSE_BTN)
        self.sleep(2)


        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ONPREM ROLE: EDIT TR1 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # self.scroll_up_header()
        # Locate the dropdown toggle button
        wait = WebDriverWait(self.driver, 10)  # Adjust timeout as needed
        dropdown_toggle = wait.until(EC.visibility_of_element_located((By.XPATH, self.ROLE_TR1)))

        # Click the dropdown toggle button to open the dropdown menu    
        self.click(self.ROLE_TR1)
        self.sleep(2)

        # Wait for the dropdown menu to appear
        dropdown_menu_xpath = f'//*[@id="nadmin-roles"]/tbody/tr[1]/td[5]/div'
        dropdown_menu = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, dropdown_menu_xpath)))

        edit_link = dropdown_menu.find_element(By.XPATH, './/a[contains(@class, "dropdown-item") and contains(text(), "Edit")]')

        edit_link.click()
        self.assert_text("Edit Role", "h1")
        self.type(self.ROLE_DESC, "Test edit")
        self.click(self.SUBMIT)
        self.assert_text("Role updated successfully!", self.POPUP)
        self.sleep(3)


        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ONPREM ROLE: DELETE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # Perform assertions 
        self.scroll_to(self.ROLE_TR1)

        # Use WebDriverWait to wait for the element to be present and visible
        wait = WebDriverWait(self.driver, 10)  # Adjust timeout as needed
        dropdown_toggle = wait.until(EC.visibility_of_element_located((By.XPATH, self.ROLE_TR1)))

        # Click the dropdown toggle button to open the dropdown menu    
        dropdown_toggle.click()

        # Wait for the dropdown menu to appear
        dropdown_menu_xpath = f'//*[@id="nadmin-roles"]/tbody/tr[1]/td[5]/div'
        dropdown_menu = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, dropdown_menu_xpath)))

        # Locate the "Edit" and "Delete" links within the dropdown menu
        delete_link = dropdown_menu.find_element(By.XPATH, './/a[contains(@class, "dropdown-item") and contains(text(), "Delete")]')
        delete_link.click()
        
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert     # Switch to the alert dialog
        dialog_text = alert.text    # Retrieve the text of the confirmation dialog
    
        # Assert or check the text of the confirmation dialog
        expected_text = "Sure?"
        assert expected_text in dialog_text
        self.sleep(2)

        alert.accept()
        self.assert_element(self.EMPTY_TABLE)
        self.sleep(3)

        search_input = self.find_element(self.ROLE_SEARCH)
        search_input.send_keys(Keys.CONTROL + 'a')  # Select all text in the input field
        self.sleep(1)
        search_input.send_keys(Keys.BACKSPACE)       # Delete the selected text
        self.sleep(1)


        # >>>>>>>>>>>>>>>>>>>>>> ONPREM ROLES: SHOW ENTRIES <<<<<<<<<<<<<<<<<<<<<<<<<
        self.show_entries_helper(self.ROLE_SHOW, self.ROLE_TABLE_ROWS)
        self.sleep(5)

        # >>>>>>>>>>>>>>>> ONPREM ROLE: SORTING TABLE COLUMN <<<<<<<<<<<<<<<<<<<
        self.sorting_helper("Name", "#nadmin-roles tbody tr")