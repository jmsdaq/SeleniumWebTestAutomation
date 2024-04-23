from seleniumbase import BaseCase
from page_objects.user import UserPage

class LoginPage(BaseCase):

    def login(self):
        # Open the login page
        self.open("https://review.onprem.nweca.com/nadmin/sign_in")
        self.maximize_window()
        self.type("input[type='username']", "intern_james")
        self.type("input[type='password']", "intern_james")
        self.click('input[type="submit"]')
