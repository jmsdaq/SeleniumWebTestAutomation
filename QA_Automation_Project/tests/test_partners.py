from seleniumbase import BaseCase
from page_objects.partner_accs import PartnersPage
from page_objects.home_page import HomePage
from faker import Faker
import random
import string

class PartnersTest(HomePage, PartnersPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.login()
        self.partners()

    def tearDown(self):
        self.sleep(5)  # Use self.sleep instead of time.sleep
        super().tearDown()

    def test_partners_account(self):
        self.assert_element(self.SIDEBAR_ACTIVE)  # Verify if the sidebar is active (from PartnersPage)
        self.click(self.PARTNER_MENU)  # Click on the Partner Accounts menu (from PartnersPage)
        self.assert_url(self.PARTNER_URL) # Assert current URL matches PARTNER_URL
        current_url = self.get_current_url() # Get current URL
        self.assert_equal(current_url, self.PARTNER_URL) # Assert current URL matches PARTNER_URL
        self.assert_true("partner/accounts" in current_url) # Assert current URL contains "partner/accounts"

    def test_entry_list(self):
        select_element = self.find_element("select[name='partner-account-table_length']")

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

    def test_create_partners(self):
        self.click('a.btn.btn-success[href="/nadmin/partner/accounts/new"]')

    def generate_unique_gmail_account(self, full_name):
        username = ''.join(char for char in full_name if char.isalnum()).lower()
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        gmail_account = f"{username}.{suffix}@gmail.com"
        return gmail_account

    def test_enter_name_and_email(self):    
        self.test_create_partners()
        # Generate a random full name
        full_name = self.generate_random_full_name()

        # Generate a unique Gmail account based on the full name
        gmail_account = self.generate_unique_gmail_account(full_name)

        # Enter the generated full name into the name field
        self.type("#nadmin_partner_register_form_name", full_name)

        # Enter the generated Gmail account into the email field
        self.type("#nadmin_partner_register_form_email", gmail_account)

        # Submit the form or perform other actions as needed
        self.click('input[type="submit"]')

    # #     # Add assertions or continue with further test steps
    #     self.assert_element("#success_message")

    #     # Example of using the generated values in subsequent steps:
    #     # self.verify_email_received(gmail_account)

    # def verify_email_received(self, gmail_account):
    #     # Perform actions to verify email received on the generated Gmail account
    #     # Example: Using external email API or checking inbox using IMAP/POP3
    #     pass  # Placeholder for actual verification logic
