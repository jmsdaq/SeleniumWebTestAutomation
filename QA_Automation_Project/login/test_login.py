from seleniumbase import BaseCase
import time

class LoginTest(BaseCase):
    def test_login_page(self):
        # Open the login page
        self.open("https://review.7.tindahang-tapat.nweca.com/nadmin")
        self.maximize_window()

        # Find the username and password input fields and enter credentials
        self.type("#session_username", "username")
        self.type("#session_password", "password")

        # # Click on the login button
        self.click('input[type="submit"]')

        # Validate that we are at the correct URL (optional)
        self.assert_title("Tindahang Tapat Nadmin Console")

        # Wait for the login process to complete
        self.wait_for_element(".breadcrumb-item", timeout=50)
        
        time.sleep(10)

  
    # def test_system_conf_page(self):
        

if __name__ == "__main__":
    LoginTest().run()
