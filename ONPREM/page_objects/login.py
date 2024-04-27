from seleniumbase import BaseCase
from page_objects.user import UserPage

class LoginPage(BaseCase):

    def login(self):
        # Open the login page
        self.open("https://review.onprem.nweca.com/nadmin/dashboard")
        self.maximize_window()
        self.type("input[type='username']", "jms")
        self.type("input[type='password']", "jms")
        self.click('input[type="submit"]')
