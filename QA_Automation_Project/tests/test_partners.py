from page_objects.partner_accs import PartnersPage
from page_objects.home_page import HomePage
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import random
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class PartnersTest(HomePage, PartnersPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.login()
        self.partners()

    def tearDown(self):
        self.sleep(5) 
        super().tearDown()

    
    def test_partners_account(self):
        self.assert_element(self.SIDEBAR_ACTIVE)  # Verify if the sidebar is active (from PartnersPage)
        self.click(self.PARTNER_MENU)  # Click on the Partner Accounts menu (from PartnersPage)
        self.assert_url(self.PARTNER_URL) # Assert current URL matches PARTNER_URL
        current_url = self.get_current_url() # Get current URL
        self.assert_equal(current_url, self.PARTNER_URL) # Assert current URL matches PARTNER_URL
        self.assert_true("partner/accounts" in current_url) # Assert current URL contains "partner/accounts"
        self.assert_text("Partner Accounts", self.PARTNER_ACCOUNT_TITLE)
        self.assert_text("Show", self.SHOW_TITLE) 
        self.assert_text("Search:", self.SEARCH_LABEL)
        self.assert_element(self.SEARCH_INPUT)
        self.assert_element_visible(self.PARTNER_ACCOUNT_TABLE, timeout=10)

        # Assert the presence of table headers
        self.assert_text("#", self.NUM_COL)
        self.assert_text("Name", self.NAME_COL) 
        self.assert_text("Company", self.COMPANY_COL)
        self.assert_text("Status", self.STATUS_COL)
        self.assert_text("Created On", self.CREATED_ON_COL)


    def test_th_sorting(self):
        # Define the column headers to sort and their expected sorting behavior
        # Define the column headers to sort and their expected sorting behavior
        columns_to_sort = [
            {"index": 3, "name": "Account ID", "expected_sort": "ascending"},
            {"index": 4, "name": "Company", "expected_sort": "ascending"},
            {"index": 5, "name": "Status", "expected_sort": "ascending"},
            {"index": 6, "name": "Created On", "expected_sort": "ascending"}
        ]

        for column in columns_to_sort:
            # Click on the sorting button for the specified column
            column_sort_button = f"//*[@id='partner-account-table']/thead/tr/th[{column['index']}]"
            self.click(column_sort_button)

            # Wait for the table content to refresh after sorting
            self.wait_for_element_present("#partner-account-table tbody tr")
            table_rows = self.find_elements("#partner-account-table tbody tr")

            # Extract the values from the specified column after sorting
            column_values_after_sorting = []
            for row in table_rows:
                try:
                    # Locate the table cell (td) within the current row (tr) using nth-child
                    cell_value = row.find_element(f"td:nth-child({column['index']})").text.strip()
                    column_values_after_sorting.append(cell_value)
                except Exception as e:
                    # Handle any exceptions raised during cell value extraction
                    print(f"Error extracting cell value: {e}")

            # Determine the expected order of values based on sorting type
            if column['expected_sort'] == "ascending":
                expected_sorted_values = sorted(column_values_after_sorting)
            else:
                expected_sorted_values = sorted(column_values_after_sorting, reverse=True)

            # Verify that the values in the column are sorted as expected
            assert column_values_after_sorting == expected_sorted_values, f"Table rows are not sorted correctly by {column['name']}"

    def test_entry_list(self):
        select_element = self.find_element(self.SHOW)   
        # Iterate over each option value and perform actions
        for option_value in ["10", "50", "100", "-1"]:  # Include "-1" for the "All" option
            select_element.click()
            self.click(f"option[value='{option_value}']")

            # Wait for the table content to load (adjust timeout as needed)
            self.wait_for_element("#partner-account-table tbody tr")
            table_rows = self.find_elements("#partner-account-table tbody tr")

            if option_value == "-1":
                expected_row_count = len(table_rows)  # All rows should be displayed
            else:
                expected_row_count = int(option_value)  # Convert to integer

            actual_row_count = len(table_rows)
            assert actual_row_count <= expected_row_count, f"Expected {expected_row_count} rows, but found {actual_row_count} rows for option value '{option_value}'"

    def test_supervision_icon(self):
        self.click(self.TR1_SUPERVISION)
        self.assert_element(self.MODAL, timeout=10)  # Waiting for modal title to appear
        self.assert_text("Impersonate Parter User", self.MODAL)  # Asserting modal title text

    def test_abort_supervision(self):
        self.test_supervision_icon()
        self.assert_element_visible(self.IMPERSONATE_FORM)
        self.click(self.ABORT_BUTTON)
        self.assert_text("Partner Accounts", self.PARTNER_ACCOUNT_TITLE)
        self.assert_text("Partner Accounts", self.PARTNER_ACCOUNT_TITLE)

    def test_impersonate(self):
        self.test_supervision_icon()
        self.click(self.IMPERSONATE_BUTTON)
        self.assert_title("Tindahang Tapat Partner Dashboard")
        current_url = self.get_current_url() # Get current URL
        self.assert_equal(current_url, self.PARTNER_PORTAL) # Assert current URL matches PARTNER_URL
        self.assert_true("/dashboard" in current_url) # Assert current URL contains "partner/accounts"
        self.wait_for_element_visible(self.PARTNER_POPUP, timeout=5)
        self.assert_element_visible(self.PARTNER_POPUP)
        self.assert_text("You are in impersonation mode!", self.POPUP_TXT)

    def test_exit_portal(self):
        self.test_impersonate()

        confirm_button = self.find_element(By.CSS_SELECTOR, self.EXIT_PORTAL)

        if confirm_button:
            # Click the button to trigger the confirmation dialog
            confirm_button.click()
            # Wait for the confirmation dialog to appear
            try:
                WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert     # Switch to the alert dialog
                dialog_text = alert.text    # Retrieve the text of the confirmation dialog
            
                # Assert or check the text of the confirmation dialog
                expected_text = "You are about to exit impersonation. Continue?"
                assert expected_text in dialog_text

                # Handle the confirmation by accepting (OK) or dismissing (Cancel)
                alert.accept()  # This confirms the action (e.g., proceed with exit impersonation)
                self.assert_element_visible(self.DEACTIVATE_IMPR)
                self.assert_text("Impersonation deactivated!", self.DEACTIVATE_TXT)
                self.assert_url(self.PARTNER_URL) # Assert current URL matches PARTNER_URL
            
            except Exception as e:
                self.fail(f"Confirmation dialog not found or handled: {str(e)}")
                # Handle any exceptions or errors if the confirmation dialog is not encountered
        else:
            self.fail("Confirmation button not found on the page")
            # Fail the test if the confirmation button is not found

    def test_search_input(self):
        search_input = self.find_element('input[aria-controls="partner-account-table"]') # Find the search input element
        search_input.send_keys("Harper Baxter") # Perform some actions with the input (e.g., typing)

        # Wait for the table to load after search
        self.wait_for_element_present("#partner-account-table tbody")
        self.assertTrue(search_input.is_displayed(), "Search input is not displayed") # Check if the search input is still displayed

        # Clear the search input
        search_input.clear()

        search_input.send_keys("Hefefhsocnciasfhosd")
        # Check if the "No matching records found" message is displayed
        empty_message = self.find_element("td.dataTables_empty")
        self.assertTrue(empty_message.is_displayed(), "No matching records message is not displayed")



    def scroll_by_pixels(self, vertical_pixels=0, horizontal_pixels=0):
        """
        Scroll the webpage by the specified number of pixels vertically and/or horizontally.

        Args:
            vertical_pixels (int): Number of pixels to scroll vertically (positive for down, negative for up).
            horizontal_pixels (int): Number of pixels to scroll horizontally (positive for right, negative for left).
        """
        # Construct the JavaScript snippet for scrolling by the specified pixels
        script = f"window.scrollBy({horizontal_pixels}, {vertical_pixels});"

    def test_scroll_by_pixels(self):

        # Scroll down by 500 pixels vertically
        self.scroll_by_pixels(vertical_pixels=500)




    def test_dropdown_menu(self):
        # Define the row number where you want to interact with the dropdown button
        row_number = 2  # Adjust this number based on your scenario
        if row_number >= 2:
            self.scroll_by_pixels(vertical_pixels=1000)

        # Construct the XPath for the specified row
        row_xpath = f'//*[@id="partner-account-table"]/tbody/tr[{row_number}]'

        # Append the XPath to locate the dropdown button within the specified row
        dropdown_xpath = f'{row_xpath}/td[7]/div'

        # Perform actions on the dropdown button using the constructed XPath
        dropdown_element = self.find_element(dropdown_xpath)
        dropdown_element.click()

        time.sleep(2)

        # Perform additional assertions or actions as needed after interacting with the dropdown
        # For example, verify that the dropdown menu appears or performs the desired action
        self.assert_element_present(self.DROPDOWN_MENU, timeout=10)  # Adjust selector as needed


        # # Define the row number where you want to interact with the dropdown button
        # row_number = 1  # Adjust this number based on your scenario

        # # Call the function to interact with the dropdown button in the specified row
        # self.interact_with_row_dropdown(row_number)

        # # Perform additional assertions or actions as needed after interacting with the dropdown
        # # For example, verify that the dropdown menu appears or performs the desired action
        # self.assert_element_present(self.DROPDOWN_MENU, timeout=10)  # Adjust selector as needed
        # def construct_row_xpath(row_number):
        #     # Construct the XPath to locate the specific table row by its index
        #     row_xpath = f'//*[@id="partner-account-table"]/tbody/tr[{row_number}]'
        #     return row_xpath

        # def interact_with_row_dropdown(row_number):
        #     # Construct the XPath for the specified row
        #     row_xpath = construct_row_xpath(row_number)

        #     # Append the XPath to locate the dropdown button within the specified row
        #     dropdown_xpath = f'{row_xpath}/td[7]/div'

        #     # Perform actions on the dropdown button using the constructed XPath
        #     dropdown_element = self.find_element_by_xpath(dropdown_xpath)
        #     dropdown_element.click()

        # # Define the row number where you want to interact with the dropdown button
        # row_number = 3  # Adjust this number based on your scenario

        # # Call the function to interact with the dropdown button in the specified row
        # interact_with_row_dropdown(row_number)
        # # Wait for the dropdown menu to fully expand
        # self.wait_for_element_visible('div.dropdown-menu')
        

        # # Define the expected dropdown options (text and corresponding URLs)
        # expected_options = {
        #     "Edit": "/nadmin/partner/accounts/7/edit",
        #     "Branches": "/nadmin/partner/accounts/7/branches",
        #     "Users": "/nadmin/partner/accounts/7/users",
        #     "Customers": "/nadmin/partner/accounts/7/customers"
        # }
        # # Verify that each expected option is present in the dropdown menu
        # dropdown_items = self.find_elements('a.dropdown-item')
        # for item in dropdown_items:
        #     item_text = item.text
        #     item_href = item.get_attribute('href')
        #     if item_text in expected_options:
        #         # Assert the presence of the expected option
        #         self.assert_true(item.is_displayed(), f"Dropdown option '{item_text}' is not displayed")
        #         # Assert that the href attribute matches the expected URL
        #         self.assert_equal(item_href, expected_options[item_text], f"Unexpected href for dropdown option '{item_text}'")

        # # Click the dropdown toggle again to close the menu (optional)
        # self.click(self.DROPDOWN_BTN)  # Close the dropdown menu

    def test_toggle_status(self):
        # self.assert_element(self.STATUS_BTN)  # Ensure toggle element is present
        # current_status = self.get_text(self.STATUS_BTN).strip()
        # target_status = "Inactive" if current_status == "Active" else "Active"

        # self.click(self.STATUS_BTN)  # Click to toggle status
        # self.wait_for_text_visible(self.STATUS_BTN, target_status, timeout=10)  # Wait for new status
        # self.assert_text(target_status, self.STATUS_BTN)  # Verify new status

        # self.click(self.STATUS_BTN)  # Click again to revert status
        # self.wait_for_text_visible(self.STATUS_BTN, current_status, timeout=10)  # Wait for original status
        # self.assert_text(current_status, self.STATUS_BTN)  # Verify original status

        self.assert_element(self.STATUS_BTN)  # Ensure toggle element is present
        current_status = self.get_text(self.STATUS_BTN).strip()

        # Determine target status based on current status
        if current_status == "Active":
            target_status = "Inactive"
        else:
            target_status = "Active"

        # Click to toggle status
        self.click(self.STATUS_BTN)

        # Wait for the new target_status to appear after toggling
        self.wait_for_text_visible(self.STATUS_BTN, target_status, timeout=10)

        # Verify that the toggle button now displays the target_status
        self.assert_text(target_status, self.STATUS_BTN)

        # Click again to revert status
        self.click(self.STATUS_BTN)

        # Wait for the original current_status to appear after toggling back
        self.wait_for_text_visible(self.STATUS_BTN, current_status, timeout=10)

        # Verify that the toggle button now displays the original current_status
        self.assert_text(current_status, self.STATUS_BTN)




    def test_create_partners(self):
        self.click('a.btn.btn-success[href="/nadmin/partner/accounts/new"]')
        self.assert_url(self.REGISTER_PARTNER_URL) # Assert current URL matches PARTNER_URL
        current_url = self.get_current_url() # Get current URL
        self.assert_equal(current_url, self.REGISTER_PARTNER_URL) # Assert current URL matches PARTNER_URL
        self.assert_true("partner/accounts" in current_url) # Assert current URL contains "partner/account

    

    def test_register_partner(self): # Test Generate 
        num_accounts = 1
        # Navigate to the create partners page
        self.test_create_partners()

        for _ in range (num_accounts):
            # Generate random data for each partner account
            full_name = self.generate_random_full_name()
            gmail_account = self.generate_unique_gmail_account(full_name)
            password = self.generate_random_password()
            company_name = self.generate_dummy_company_name()
            account_id = self.generate_dummy_account_id()

            # Fill out the registration form with generated dat
            form_fields = [
                (self.FULL_NAME, full_name),
                (self.GMAIL, gmail_account),
                (self.PASSWORD, password),
                (self.PASSWORD_CONF, password),
                (self.COMPANY, company_name),
                (self.ACCOUNT_ID, account_id)
            ]
            
            for locator, value in form_fields:
                if locator == "#nadmin_partner_register_form_company":
                    # Select timezone before filling out company name
                    self.select_random_timezone()
                self.type(locator, value)
                self.wait_for_element_value_to_be_populated(locator)

            try:
                province_selector = "#nadmin_partner_register_form_branch_province_id"
                self.select_option_by_visible_text(province_selector, "Camarines Sur")

                city_selector = "#nadmin_partner_register_form_branch_city_id"
                self.wait_for_element(city_selector)

                city_options = self.get_select_options(city_selector)
                assert len(city_options) > 1, "Branch city field did not populate with options based on selected province"

            except Exception as e:
                # Log the exception but continue with the script
                print(f"Error occurred during province/city selection: {e}")
                # You can log the error or perform additional handling here

                # Submit the form
                self.click('input[type="submit"]')

                # Save the entered information to a CSV file
                data = {
                    'Name': full_name,
                    'Email': gmail_account,
                    'Password': password,
                    'Company': company_name,
                    'Account ID': account_id
                }
                csv_file = 'partner_accounts.csv'
                with open(csv_file, 'a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['Name', 'Email', 'Password', 'Company', 'Account ID'])
                    if file.tell() == 0:
                        writer.writeheader()  # Write header only if the file is empty
                    writer.writerow(data)
    
    def test_all_fields(self): # Test Generate 
        num_accounts = 2
        # Navigate to the create partners page
        self.test_create_partners()

        for _ in range (num_accounts):
            # Generate random data for each partner account
            full_name = self.generate_random_full_name()
            gmail_account = self.generate_unique_gmail_account(full_name)
            password = self.generate_random_password()
            company_name = self.generate_dummy_company_name()
            account_id = self.generate_dummy_account_id()

            # Fill out the registration form with generated data
            form_fields = [
                (self.FULL_NAME, full_name),
                (self.GMAIL, gmail_account),
                (self.PASSWORD, password),
                (self.PASSWORD_CONF, password),
                (self.COMPANY, company_name),
                (self.ACCOUNT_ID, account_id)
            ]

            for locator, value in form_fields:
                if locator == "#nadmin_partner_register_form_company":
                    # Select timezone before filling out company name
                    self.select_random_timezone()
                self.type(locator, value)
                self.wait_for_element_value_to_be_populated(locator)

            # Select the province "Camarines Sur"
            province_selector = "#nadmin_partner_register_form_branch_province_id"
            self.select_option_by_visible_text(province_selector, "Camarines Sur")

            # Wait for the city dropdown to populate with options
            city_selector = "#nadmin_partner_register_form_branch_city_id"
            self.wait_for_element(city_selector)

            # Get all the options from the city dropdown
            city_options = self.get_select_options(city_selector)

            # Assert that there are more than 1 city options available
            assert len(city_options) > 1, "Branch city field did not populate with options based on selected province"

            # Select a random branch city
            random_index = random.randint(1, len(city_options) - 1)  # Exclude the first option ("Select...")
            self.select_option_by_index(city_selector, random_index)

            # Continue with other actions or assertions related to selecting a branch city
            selected_city = self.get_selected_option_text("#nadmin_partner_register_form_branch_city_id")
            self.assertIn(selected_city, city_options[1:], "Unexpected branch city selected")  # Check selected city is in the list
            self.click('input[type="submit"]')

            # Assert successful registration or navigate to the next page and perform additional checks
            self.assert_element_present("div.toast-body", timeout=10)  # Check for success message
            self.click('input[type="submit"]') # Submit the form

            # Save the entered information to a CSV file
            data = {
                'Name': full_name,
                'Email': gmail_account,
                'Password': password,
                'Company': company_name,
                'Account ID': account_id
            }
            csv_file = 'partner_accounts.csv'
            with open(csv_file, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Name', 'Email', 'Password', 'Company', 'Account ID'])
                if file.tell() == 0:
                    writer.writeheader()  # Write header only if the file is empty
                writer.writerow(data)

        


    # def test_edit_partner(self):
    #     self.partners()
    #     # Find all dropdown items with class containing 'dropdown-item'
    #     dropdown_items = self.find_elements('//*[contains(@class, "dropdown-item")]')
    #             # Click on specific dropdown options to reach desired state
    #     self.click_dropdown_option("Edit")  # Click 'Edit' in dropdown
    #     # self.click_dropdown_option("Branches")  # Click 'Branches' in dropdown
 
    def setup_initial_state(self):
        # Click on specific dropdown options to reach desired state
        self.click_dropdown_option("Edit")  # Click 'Edit' in dropdown
        self.click_dropdown_option("Branches")  # Click 'Branches' in dropdown

    def click_dropdown_option(self, option_text):
        # Find and click the specified option in the dropdown
        dropdown_xpath = '//*[contains(@class, "dropdown-item")]'
        dropdown_items = self.find_elements(dropdown_xpath)
        for item in dropdown_items:
            if item.text.strip() == option_text:
                self.click(item)
                break

    def test_edit_partner(self):
        # This test starts from the desired initial state set by the fixture
        self.setup_initial_state()
        self.click_dropdown_option()
        edit_page_title = self.get_text("h5")  # Assuming 'h5' is the title element on the edit page
        assert "Edit Account (0MLLVF62)" in edit_page_title  # Assert the title contains 'Edit Partner's