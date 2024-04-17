from seleniumbase import BaseCase
from selenium.webdriver.support.ui import Select
from faker import Faker
import random
import string

class PartnersPage(BaseCase):
    SIDEBAR_ACTIVE = ".app-sidebar"
    PARTNER_URL = "https://review.7.tindahang-tapat.nweca.com/nadmin/partner/accounts"
    PARTNER_MENU = 'a[data-sidebars-target="menu"][href="/nadmin/partner/accounts"]'
    PARTNER_ACCOUNT_TITLE = "h5.card-title"
    REGISTER_PARTNER_URL = "https://review.7.tindahang-tapat.nweca.com/nadmin/partner/accounts/new"

    # Locators for Partners Account Table
    PARTNER_ACCOUNT_TABLE = "#partner-account-table"
    TABLE_ROWS = "#partner-account-table tbody tr"
    SHOW_TITLE = "#partner-account-table_length label"
    SHOW = "select[name='partner-account-table_length']"
    SEARCH_LABEL = "#partner-account-table_filter label"
    SEARCH_INPUT = "#partner-account-table_filter input[type='search']"
    
    # Locators for Partners Account Table Header
    NUM_COL = "#partner-account-table th[aria-label='#']"
    NAME_COL = "#partner-account-table th[aria-label='Name: activate to sort column ascending']"
    COMPANY_COL = "#partner-account-table th[aria-label='Company: activate to sort column ascending']"
    STATUS_COL = "#partner-account-table th[aria-label='Status: activate to sort column ascending']"
    CREATED_ON_COL = "#partner-account-table th[aria-label='Created On: activate to sort column ascending']"

    # Locators for Partners Account Table Dropdown
    TR1_DROPDOWN = '//*[@id="partner-account-table"]/tbody/tr[1]/td[7]/div/a'
    EDIT_ACC = '//*[@id="partner-account-table"]/tbody/tr[1]/td[7]/div/div/a[1]'

    # Locators for Partners Account Registration
    FULL_NAME = "#nadmin_partner_register_form_name"
    GMAIL = "#nadmin_partner_register_form_email"
    PASSWORD = "#nadmin_partner_register_form_password"
    PASSWORD_CONF = "#nadmin_partner_register_form_password_confirmation"
    COMPANY = "#nadmin_partner_register_form_company"
    ACCOUNT_ID = "#nadmin_partner_register_form_account_name"

    def partners(self):
        self.assert_element(".app-sidebar")  # Verify if the sidebar is active (from PartnersPage)
        self.click('a[data-sidebars-target="menu"][href="/nadmin/partner/accounts"]')  # Click on the Partner Accounts menu (from PartnersPage)


    def verify_displayed_entries(self, option_value):
        table_rows = self.find_elements("#partner-account-table tbody tr") # Get the table rows (if any)

        # Determine the expected maximum number of rows based on the selected option
        if option_value == "-1":  # "All" option
            expected_max_rows = len(table_rows)  # Display all rows
        else:
            expected_max_rows = int(option_value) if option_value.isdigit() else 0

    def generate_random_full_name(self):
        fake = Faker()
        return fake.name()

    def generate_random_password(self, length=10):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return f"<{password}>"  # Enclose the password in angle brackets

    def generate_unique_gmail_account(self, full_name):
        username = ''.join(char for char in full_name if char.isalnum()).lower()
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        gmail_account = f"{username}.{suffix}@gmail.com"
        return gmail_account
    
    def generate_dummy_company_name(self):
        fake = Faker()
        return fake.company()

    def generate_dummy_account_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def select_random_timezone(self):
        # Find the select element for time zones
        timezone_select = self.get_element("select#nadmin_partner_register_form_timezone")
        select = Select(timezone_select) # Create a Select object
        options = select.options # Get all the options from the dropdown
        
        # Select a random option
        random_index = random.randint(1, len(options) - 1)  # Exclude the first option ("Select...")
        select.select_by_index(random_index)

    def wait_for_element_value_to_be_populated(self, locator, timeout=10):
        """
        Custom method to wait until an input field's value is populated (not empty).
        """
        self.wait_for_element(locator)  # Wait for the element to be present
        value = self.get_attribute(locator, "value")
        if not value:
            self.wait_for_element_value_to_be_populated(locator, timeout=timeout) 
