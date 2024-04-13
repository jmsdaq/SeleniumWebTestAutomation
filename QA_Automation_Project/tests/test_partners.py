from seleniumbase import BaseCase
from page_objects.partner_accs import PartnersPage
from page_objects.home_page import HomePage
from faker import Faker
import random
import string
import csv
from selenium.common.exceptions import NoSuchElementException

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

    # @pytest.mark.run(order=1)
    def test_partners_account(self):
        self.assert_element(self.SIDEBAR_ACTIVE)  # Verify if the sidebar is active (from PartnersPage)
        self.click(self.PARTNER_MENU)  # Click on the Partner Accounts menu (from PartnersPage)
        self.assert_url(self.PARTNER_URL) # Assert current URL matches PARTNER_URL
        current_url = self.get_current_url() # Get current URL
        self.assert_equal(current_url, self.PARTNER_URL) # Assert current URL matches PARTNER_URL
        self.assert_true("partner/accounts" in current_url) # Assert current URL contains "partner/accounts"

    # @pytest.mark.run(order=2)
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

    # @pytest.mark.run(order=3)
    def test_create_partners(self):
        self.click('a.btn.btn-success[href="/nadmin/partner/accounts/new"]')

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

    # @pytest.mark.run(order=4)
    def test_random_fields(self): # Test Generate 
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

            # Fill out the registration form with generated data
            self.type("#nadmin_partner_register_form_name", full_name)
            self.type("#nadmin_partner_register_form_email", gmail_account)
            self.type("#nadmin_partner_register_form_password", password)
            self.type("#nadmin_partner_register_form_password_confirmation", password)
            self.select_random_timezone()
            self.type("#nadmin_partner_register_form_company", company_name)
            self.type("#nadmin_partner_register_form_account_name", account_id)


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

            # # Optionally, perform assertions or other actions after form submission
            # self.assert_element("#success_message")  # Assuming there's a success message

    def test_search_input(self):
        try:
            # Find the search input element
            search_input = self.find_element('input[aria-controls="partner-account-table"]')

            # Perform some actions with the input (e.g., typing)
            search_input.send_keys("Your search query")

            # Optionally, you can assert something about the input
            self.assertTrue(search_input.is_displayed(), "Search input is not displayed")

        except NoSuchElementException as e:
            # Handle NoSuchElementException (element not found)
            self.fail("Search input element not found: {}".format(e))

        except Exception as e:
            # Handle other exceptions
            self.fail("An unexpected error occurred: {}".format(e))

    ##########################################################################################################




    # # def generate_random_full_name(self):
    # #     fake = Faker()
    # #     return fake.name()

    # def generate_random_password(self, length=10):
    #     characters = string.ascii_letters + string.digits + string.punctuation
    #     return ''.join(random.choice(characters) for _ in range(length))

    # def generate_unique_gmail_account(self, full_name):
    #     username = ''.join(char for char in full_name if char.isalnum()).lower()
    #     suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    #     gmail_account = f"{username}.{suffix}@gmail.com"
    #     return gmail_account

    # def generate_dummy_company_name(self):
    #     fake = Faker()
    #     return fake.company()

    # def generate_dummy_account_id(self):
    #     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # def test_create_multiple_partner_accounts(self):
    #     num_accounts = 5  # Define the number of partner accounts to create

    #     for _ in range(num_accounts):
    #         try:
    #             # Navigate to the create partners page
    #             self.test_create_partners()

    #             # Generate random data for each partner account
    #             full_name = self.generate_random_full_name()
    #             gmail_account = self.generate_unique_gmail_account(full_name)
    #             password = self.generate_random_password()
    #             company_name = self.generate_dummy_company_name()
    #             account_id = self.generate_dummy_account_id()

    #             # Fill out the registration form with generated data
    #             self.type("#nadmin_partner_register_form_name", full_name)
    #             self.type("#nadmin_partner_register_form_email", gmail_account)
    #             self.type("#nadmin_partner_register_form_password", password)
    #             self.type("#nadmin_partner_register_form_password_confirmation", password)
    #             self.select_random_timezone()
    #             self.type("#nadmin_partner_register_form_company", company_name)
    #             self.type("#nadmin_partner_register_form_account_name", account_id)

    #             # Submit the form by clicking the "Register" button
    #             self.click('input[type="submit"]')

    #             # Check for the presence of a success message (or any other verification)
    #             self.wait_for_element_visible("div.alert-success", timeout=10)

    #             # Save the entered information to a CSV file
    #             data = {
    #                 'Name': full_name,
    #                 'Email': gmail_account,
    #                 'Password': password,
    #                 'Company': company_name,
    #                 'Account ID': account_id
    #             }
    #             csv_file = 'partner_accounts.csv'
    #             with open(csv_file, 'a', newline='') as file:
    #                 writer = csv.DictWriter(file, fieldnames=['Name', 'Email', 'Password', 'Company', 'Account ID'])
    #                 if file.tell() == 0:
    #                     writer.writeheader()  # Write header only if the file is empty
    #                 writer.writerow(data)

    #         except NoSuchElementException:
    #             print("Warning: No success message detected after account creation.")

    #         except Exception as e:
    #             print(f"Error creating partner account: {str(e)}")


# Usage:
# Run this test class using SeleniumBase:
# seleniumbase my_test_module.py
    





    # def test_registration_with_random_timezone(self):     
    #     # Call the function to select a random time zone
        

        

    # #     # Add assertions or continue with further test steps
    #     self.assert_element("#success_message")

    #     # Example of using the generated values in subsequent steps:
    #     # self.verify_email_received(gmail_account)

    # def verify_email_received(self, gmail_account):
    #     # Perform actions to verify email received on the generated Gmail account
    #     # Example: Using external email API or checking inbox using IMAP/POP3
    #     pass  # Placeholder for actual verification logic
