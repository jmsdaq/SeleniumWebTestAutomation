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

class WarehouseUserTest(LoginPage, UserPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.login()

    def tearDown(self):
        self.sleep(10) 
        super().tearDown()

    # >>>>>>>> NAVIGATION TO WAREHOUSE USER WITHIN USER MENU <<<<<<<<<<<<<
    @pytest.mark.run(order=1)
    def test_warehouse_user(self):
        self.warehouse_nav()
    
        # >>>>>>>>>>>>> ADD WAREHOUSE USER <<<<<<<<<<<<<<<<
        wait = WebDriverWait(self.driver, 10)
        add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ADD_BTN)))
        add_btn.click()
        # self.click(self.ADD_BTN)
        self.wait_for_element(self.MODAL)
        self.click(self.CLOSE_ICON)
        self.sleep(1)

        # CLICK THE CLOSE BUTTON
        self.click(self.ADD_BTN)
        self.wait_for_element(self.MODAL)
        self.scroll_to(self.CLOSE_BTN) # scroll down method
        self.wait_for_element(self.CLOSE_BTN)
        self.click(self.CLOSE_BTN)
        self.sleep(1)
        
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
        wh_data = self.generate_fake_warehouse_data()

        # Fill in the form fields with generated fake data
        self.type(self.NAME, "intern_james")
        self.type(self.EMPLOYEE_CODE, str(wh_data['employee_code']))
        username = wh_data['username']  # Store the generated username
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, wh_data['password'])
        self.type(self.PIN, str(wh_data['pin']))
        self.select_option_by_text(self.OPERATIONAL_ROLE, wh_data['operation_role'])
        self.click(self.SUBMIT)
        self.assert_text("Warehouse user created successfully!", "h2")
        self.sleep(2)

        # Print the generated username
        print("Generated Username:", username)

        # >>>>>>>>>>>>>>> SEARCH <<<<<<<<<<<<<<<<<<<
        self.search_helper(self.SEARCH, username, self.S_TRS, self.TR_XPATH)

        # >>>>>>>>>>>>>> UPDATE USER'S AVATAR <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # Construct the absolute path to the file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.abspath(os.path.join(current_dir, '..', 'data', 'avatar.jpg'))
        self.click(self.AVATAR)
        self.wait_for_element_visible(self.MODAL)
        upload_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.CHOOSE_IMG)))
        
        # Upload the file using JavaScript to set the file path directly
        self.driver.execute_script('arguments[0].style = ""; arguments[0].style.display = "block";', upload_input)

        # upload_input.send_keys(file_path)
        upload_input.send_keys(file_path)
        self.click(self.SUBMIT)
        self.assert_text("User picture has been updated successfully!", self.POPUP)

        # >>>>>>>>>>>>>>>> EDIT TABLE ROW <<<<<<<<<<<<<<<<<<<<
        self.scroll_up_header()

        # Locate the dropdown toggle button
        wait = WebDriverWait(self.driver, 10)  # Adjust timeout as needed
        dropdown_toggle = wait.until(EC.visibility_of_element_located((By.XPATH, self.TR1)))

        # Click the dropdown toggle button to open the dropdown menu    
        self.click(self.TR1)
        self.sleep(2)

        # Wait for the dropdown menu to appear
        dropdown_menu_xpath = f'//*[@id="app-users"]/tbody/tr[1]/td[8]/div/div[@class="dropdown-menu show"]'
        dropdown_menu = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, dropdown_menu_xpath)))

        edit_link = dropdown_menu.find_element(By.XPATH, './/a[contains(@class, "dropdown-item") and contains(text(), "Edit")]')

        # Click the "Edit" link
        edit_link.click()
        self.wait_for_element(self.MODAL)
        self.assert_text("Edit Warehouse User", "h1")
        self.scroll_down()
        self.select_option_by_text(self.OPERATIONAL_ROLE, wh_data['operation_role'])
        self.sleep(2)
        self.scroll_to(self.UPDATE_BTN)
        self.click(self.UPDATE_BTN)
        self.assert_text("App user updated successfully!", self.POPUP)
        self.sleep(3)

        #>>>>>>>>>>>>>>>>>>>>> DELETE <<<<<<<<<<<<<<<<<<<<<<<<
        # Perform assertions
        self.scroll_to(self.TR1)
        dropdown_toggle_xpath = self.TR1

        # Use WebDriverWait to wait for the element to be present and visible
        wait = WebDriverWait(self.driver, 10)  # Adjust timeout as needed
        dropdown_toggle = wait.until(EC.visibility_of_element_located((By.XPATH, self.TR1)))

        # Click the dropdown toggle button to open the dropdown menu    
        dropdown_toggle.click()

        # Wait for the dropdown menu to appear
        dropdown_menu_xpath = f'//*[@id="app-users"]/tbody/tr[1]/td[8]/div/div[@class="dropdown-menu show"]'
        dropdown_menu = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, dropdown_menu_xpath)))

        # Locate the "Edit" and "Delete" links within the dropdown menu
        delete_link = dropdown_menu.find_element(By.XPATH, './/a[contains(@class, "dropdown-item") and contains(text(), "Delete")]')
        delete_link.click()
        
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert  
        dialog_text = alert.text
        self.sleep(3)

        # Assert or check the text of the confirmation dialog
        expected_text = "Delete user?"
        assert expected_text in dialog_text

        alert.accept()
        self.assert_element_visible(self.POPUP)
        self.sleep(3)
        self.clear_search(self.SEARCH)
        self.sleep(2)

        # >>>>>>>>>> SHOWING A SPECIFIC NUMBER OF ENTRIES <<<<<<<<<<<<
        self.show_entries_helper(self.SHOW, self.S_TRS)
        self.sleep(5)

        # >>>>>>>>>>> SORTING TABLE COLUMN <<<<<<<<<<<<<<
        self.sorting_helper("Name", self.S_TRS)
        self.sleep(4)
        self.sorting_helper("Username", self.S_TRS)