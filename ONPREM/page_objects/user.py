from seleniumbase import BaseCase
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from faker import Faker
from datetime import datetime
import random

class UserPage(BaseCase):

    # WAREHOUSE LOCATORS
    SIDEBAR_ACTIVE = ".app-sidebar"
    USER_MENU = "//a[contains(text(), 'Users')]"
    WAREHOUSE_MENU = "a[data-sidebars-target='menu'][href='/nadmin/app_users']"
    
    # ADD FORM LOCALTORS
    MODAL = "#appModalContent"
    ADD_BTN = ".btn.btn-success"
    NAME = 'input#user_name.form-control'
    EMPLOYEE_CODE = 'input#user_employee_code.form-control'
    USERNAME = 'input#user_username'
    PASSWORD = 'input#user_password.form-control'
    PASSWORD_CONF = 'input#user_password_confirmation.form-control'
    PIN = 'input#user_pin.form-control'
    OPERATIONAL_ROLE = 'select#user_operation_role.form-select'
    SUBMIT = 'input[type="submit"]'
    CLOSE_ICON = ".btn-close"
    CLOSE_BTN = 'button.btn-warning[data-bs-dismiss="modal"]'
    ERRORS = "#errors"
    FOOTER = ".modal-footer"
    HEADER = ".modal-header"
    CREATED = "td:nth-child(6)"
    UPDATED = "td:nth-child(7)"

    # SEARCH LOCATORS
    SEARCH = 'input[type="search"][aria-controls="app-users"]'
    TABLE = ".dataTables_wrapper no-footer"
    S_TRS = '#app-users tbody tr'
    TR_XPATH = '//*[@id="app-users"]/tbody/tr'
    EMPTY_TABLE = ".dataTables_empty"
    AVATAR = '//*[@id="app-users"]/tbody/tr/td[2]'
    CHOOSE_IMG = "#user_image_url"
    POPUP = "#swal2-title"

    # SHOW ENTRIES LOCATORS
    SHOW = "select[name='app-users_length']"
    TR1 = '//*[@id="app-users"]/tbody/tr[1]/td[8]/div'

    # EDIT LOCATORS
    EDIT_MODAL_TITLE = ".modal-title fs-5"
    UPDATE_BTN = 'input[type="submit"][value="Update User"]'


    # ----------------ONPREM: USER LOCATORS --------------------
    ONPREM_MENU = 'a[data-sidebars-target="menu"][href="/nadmin/users"]'
    CARD_TITLE = '.card-title'
    DANGER = 'div.text-danger'
    ON_USERNAME = 'input#nadmin_user_username.form-control'
    ON_NAME = 'input#nadmin_user_name.form-control'
    ON_PW = 'input#nadmin_user_password.form-control'
    ON_PW_CONF = 'input#nadmin_user_password_confirmation.form-control'
    ON_ROLE = '#nadmin_user_role_id'
    ON_SEARCH = 'input[type="search"][aria-controls="nadmin-users"]'
    ON_SHOW = "select[name='nadmin-users_length']"
    S_ON_TRS = '#nadmin-users tbody tr'
    ON_TR_XPATH = '//*[@id="nadmin-users"]/tbody/tr'
    ON_TR1 = '//*[@id="nadmin-users"]/tbody/tr[1]/td[6]/div'
    ON_TABLE = "//*[@id='nadmin-users']/tbody"
    ON_CREATED = "td:nth-child(5)"

    # ONPREM: ABILITIES LOCATORS
    ABILITIES = "#user-abilities"

    # ONPREM: ROLE
    ROLE = "#user-roles"
    ROLE_NAME = "#nadmin_role_name"
    ROLE_DESC = "#nadmin_role_description"
    ROLE_SEARCH = 'input[type="search"][aria-controls="nadmin-roles"]'
    S_ROLE_TRS = '#nadmin-roles tbody tr'
    ROLE_TR_XPATH = '//*[@id="nadmin-roles"]/tbody/tr'
    ROLE_ABILITIES = '//*[@id="nadmin-roles"]/tbody/tr[1]/td[4]/a'
    ROLE_TR1 = '//*[@id="nadmin-roles"]/tbody/tr[1]/td[5]/div'
    ROLE_SHOW = "select[name='nadmin-roles_length']"
    ROLE_TR1_ABILITIES = '//*[@id="nadmin-roles"]/tbody/tr[1]/td[4]/a'
    ROLE_TABLE = "//*[@id='nadmin-roles']/tbody"

    def user_nav(self):
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE) 
        self.click(self.USER_MENU) 

    def warehouse_nav(self):
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE)  # Verify if the sidebar is active (from PartnersPage)
        self.sleep(2)
        self.click(self.USER_MENU)  # Click on the Partner Accounts menu (from PartnersPage)
        self.sleep(2)
        self.click(self.WAREHOUSE_MENU)

    def onprem_user_nav(self):
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE)  # Verify if the sidebar is active (from PartnersPage)
        self.sleep(2)
        self.click(self.USER_MENU)  # Click on the Partner Accounts menu (from PartnersPage)
        self.sleep(2)
        self.click(self.ONPREM_MENU)

    def scroll_with_actions(self, element):
        # Scroll down to the specified element using ActionChains
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.perform()

    def scroll_up(self):
        header_element = self.find_element(".modal-header")
        self.scroll_with_actions(header_element)
    
    def scroll_up_header(self):
        header_element = self.find_element(".table-light")
        self.scroll_with_actions(header_element)

    def scroll_down(self):
        footer_element = self.find_element(".modal-footer")
        self.scroll_with_actions(footer_element)

    def scroll_bottom(self):
        bottom_element = self.find_element(".navbar fixed-bottom text-end text-muted")
        self.scroll_with_actions(bottom_element)

    def clear_search(self, css_selector):
        search_input = self.find_element(css_selector)
        search_input.send_keys(Keys.CONTROL + 'a')  # Select all text in the input field
        self.sleep(1)
        search_input.send_keys(Keys.BACKSPACE)       # Delete the selected text
        self.sleep(2)

    def generate_fake_warehouse_data(self):
        faker = Faker()
        wh_data = {
            'name': faker.name(),
            'employee_code': faker.random_number(digits=6),
            'username': faker.user_name(),
            'password': faker.password(length=10, special_chars=True, digits=True),
            'pin': faker.random_number(digits=4),
            'operation_role': faker.random_element(elements=["cashier", "picker", "packer", "checker", "supervisor", "dispatcher"])
        }
        return wh_data
    
    def generate_fake_onprem_data(self):
        faker = Faker()
        onprem_data = {
            'name': faker.name(),
            'username': faker.user_name(),
            'password': faker.password(length=10, special_chars=True, digits=True),
            'role': faker.random_element(elements=["admin", "warehouse", "Assistant Admin", "test role", "TestRaj", "Intern"])
        }
        return onprem_data
    
    def search_helper(self, search, sn, trs, trx):
        # CHECK NO MATCHING RECORD FOUND
        wait = WebDriverWait(self.driver, 10)
        search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, search)))

        search_input.send_keys("#")
        self.sleep(2)
        empty_message = self.find_element(self.EMPTY_TABLE)
        self.assertTrue(empty_message.is_displayed(), "No matching records message is not displayed")
        self.assert_text("No matching records found", "td.dataTables_empty")
        self.sleep(3)

        # >>>>>>>>>>>>>> TEST MATCH <<<<<<<<<<<<<<<<<<<
        # Wait for the search input to be visible and interactable
        wait = WebDriverWait(self.driver, 10)
        search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, search)))
        self.driver.execute_script("arguments[0].scrollIntoView();", search_input)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, search)))

        search_input.clear()
        search_input.send_keys(sn)
        # # Wait for the table rows to update based on the search query (wait for presence of table rows)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, trs)))

        table_rows = self.driver.find_elements(By.XPATH, trx)
        self.assertGreater(len(table_rows), 0, "Table does not contain any rows after search.")
        self.sleep(3)
        
    def show_entries_helper(self, tr_selector, css_selector):
        # >>>>>>>>>>>>>>>>> SHOWING A SPECIFIC NUMBER OF ENTRIES <<<<<<<<<<<<<<<<<<<<<<<<<<<
        select_element = self.find_element(tr_selector)
        # Define a list of option values to test, including "-1" for "All" option
        option_values = ["10", "50", "100", "-1"]
        for option_value in option_values:
            # Click the 'Show Entries' dropdown and select the current option value
            select_element.click()
            self.click(f"option[value='{option_value}']")
            self.sleep(2)

            # Scroll down to the bottom of the page to load all content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.sleep(1)  # Add a short delay to ensure the content is fully loaded

            self.wait_for_element(css_selector)
            table_rows = self.find_elements(css_selector)

            # Determine the expected number of rows based on the selected option value
            if option_value == "-1":
                expected_row_count = len(table_rows)  # All rows should be displayed
            else:
                expected_row_count = int(option_value)  # Convert to integer
            actual_row_count = len(table_rows)
            
            assert actual_row_count <= expected_row_count, (
                f"Expected {expected_row_count} rows or fewer, but found {actual_row_count} rows for option value '{option_value}'"
            )
            # Scroll back up to the top of the page for the next iteration
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.sleep(1)  # Add a short delay to ensure scrolling is complete
            
    def sorting_helper(self, column_name, css_selector):
        # Click the column header to trigger sorting
        column_header = self.find_element(By.XPATH, f'//th[contains(text(), "{column_name}")]')
        column_header.click()

        # Refresh the reference to the column header to avoid staleness
        column_header = self.find_element(By.XPATH, f'//th[contains(text(), "{column_name}")]')

        # Wait for the table content to reload after sorting (adjust timeout as needed)
        wait = WebDriverWait(self.driver, 3)  # Adjust timeout as needed
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

        # Refresh the reference to the table rows to avoid staleness
        try:
            visible_rows = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
        except StaleElementReferenceException:
            # If stale element exception occurs, refresh the reference again
            visible_rows = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

        # Assert the sorting order
        if visible_rows:
            first_row_value = visible_rows[0].find_element(By.XPATH, f"./td[1]").text
            last_row_value = visible_rows[-1].find_element(By.XPATH, f"./td[1]").text
            assert first_row_value <= last_row_value, f"Sorting order for column '{column_name}' is incorrect"
        else:
            raise AssertionError("No visible rows found after sorting")
        

    def _convert_to_datetime(self, date_str):
        # Convert date-time string to a datetime object
        # Adjust the format according to your date-time string (e.g., "04/15/24 04:40:52 PM")
        date_format = "%m/%d/%y %I:%M:%S %p"
        return datetime.strptime(date_str, date_format)
      
    def assert_ordered_at(self, td_selector):
        # Find all date elements using the CSS selector for the specific column
        date_elements = self.find_elements(td_selector)
        # Extract and store the date-time strings from the elements
        date_strings = []
        for element in date_elements:
            date_text = element.text.strip()
            date_strings.append(date_text)  # Store the date-time string
        # Convert date-time strings to datetime objects for comparison
        date_objects = []
        for date_str in date_strings:
            date_obj = self._convert_to_datetime(date_str)
            date_objects.append(date_obj)
        # Check if the date objects are in ascending order
        is_ascending = all(date_objects[i] <= date_objects[i + 1] for i in range(len(date_objects) - 1))
        # Assert that the date objects are in ascending order
        self.assertTrue(is_ascending, "Dates are not in ascending order")

    def sort_date(self, column):
        column_header = self.find_element(By.XPATH, f'//th[contains(text(), "{column}")]')
        column_header.click()

        # Refresh the reference to the column header to avoid staleness
        column_header = self.find_element(By.XPATH, f'//th[contains(text(), "{column}")]')
        self.sleep(2)