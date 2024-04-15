from seleniumbase import BaseCase
from page_objects.partner_accs import PartnersPage
from page_objects.home_page import HomePage
from faker import Faker
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import random
import string
import csv

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


    def test_entry_list(self):
        select_element = self.find_element(self.SHOW)

        # Iterate over each option value and perform actions
        for option_value in ["10", "50", "100", "-1"]:  # Include "-1" for the "All" option
            # Click the dropdown to open the options
            select_element.click()

            # Click the <option> corresponding to the specified value
            self.click(f"option[value='{option_value}']")

            # Wait for the table content to load (adjust timeout as needed)
            self.wait_for_element("#partner-account-table tbody tr")

            # Perform actions and assertions based on the displayed entries
            self.verify_displayed_entries(option_value)

             q

    def test_create_partners(self):
        self.click('a.btn.btn-success[href="/nadmin/partner/accounts/new"]')
        self.assert_url(self.REGISTER_PARTNER_URL) # Assert current URL matches PARTNER_URL
        current_url = self.get_current_url() # Get current URL
        self.assert_equal(current_url, self.REGISTER_PARTNER_URL) # Assert current URL matches PARTNER_URL
        self.assert_true("partner/accounts" in current_url) # Assert current URL contains "partner/accounts"


    def test_register_partner(self): # Test Generate 
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