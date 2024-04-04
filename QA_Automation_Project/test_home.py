from seleniumbase import BaseCase

class LoginTest(BaseCase):
    def test_login_page(self):
        # Open the login page
        self.open("https://review.7.tindahang-tapat.nweca.com/nadmin")

        # Find the username and password input fields and enter credentials
        self.type("#session_username", "intern")
        self.type("#session_password", "intern")

        # Click on the login button
        self.click('button[type="submit"]')

        # Wait for the login process to complete
        self.wait_for_element("#dashboard")

        # Check if the login was successful by verifying the presence of dashboard element
        self.assert_element("#dashboard")

if __name__ == "__main__":
    LoginTest().run()
