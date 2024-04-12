from seleniumbase import BaseCase

class PartnersPage(BaseCase):
    SIDEBAR_ACTIVE = ".app-sidebar"
    PARTNER_URL = "https://review.7.tindahang-tapat.nweca.com/nadmin/partner/accounts"
    PARTNER_MENU = 'a[data-sidebars-target="menu"][href="/nadmin/partner/accounts"]'

    def partners(self):
        self.assert_element(".app-sidebar")  # Verify if the sidebar is active (from PartnersPage)
        self.click('a[data-sidebars-target="menu"][href="/nadmin/partner/accounts"]')  # Click on the Partner Accounts menu (from PartnersPage)
