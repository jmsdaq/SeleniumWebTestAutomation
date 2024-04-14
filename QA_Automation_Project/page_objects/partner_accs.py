from seleniumbase import BaseCase
from selenium.webdriver.support.ui import Select
import random


class PartnersPage(BaseCase):
    SIDEBAR_ACTIVE = ".app-sidebar"
    PARTNER_URL = "https://review.7.tindahang-tapat.nweca.com/nadmin/partner/accounts"
    PARTNER_MENU = 'a[data-sidebars-target="menu"][href="/nadmin/partner/accounts"]'

    def partners(self):
        self.assert_element(".app-sidebar")  # Verify if the sidebar is active (from PartnersPage)
        self.click('a[data-sidebars-target="menu"][href="/nadmin/partner/accounts"]')  # Click on the Partner Accounts menu (from PartnersPage)


    def select_random_timezone(self):
        # Find the select element for time zones
        timezone_select = self.get_element("select#nadmin_partner_register_form_timezone")
        
        # Create a Select object
        select = Select(timezone_select)

        # Get all the options from the dropdown
        options = select.options
        
        # Select a random option
        random_index = random.randint(1, len(options) - 1)  # Exclude the first option ("Select...")
        select.select_by_index(random_index)