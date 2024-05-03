from seleniumbase import BaseCase

class LoginPage(BaseCase):

    def login(self):
        # Open the login page
        self.open("https://review.onpremg.nweca.com")
        self.maximize_window()
        self.type("input[type='username']", "jms")
        self.type("input[type='password']", "jms")
        self.click('input[type="submit"]')
