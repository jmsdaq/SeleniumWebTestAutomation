from page_objects.home_page import HomePage
import time

class LoginTest(HomePage):

    # def setUp():
    #     # Call the parent BaseCase class setup method 
    #     super().setUp()
    #     print("RUNNING BEFORE")
        
    #     # Open the login page
    #     self.open("https://review.7.tindahang-tapat.nweca.com/nadmin")
    #     self.maximize_window()

    # def tearDown():
    #     time.sleep(10)

    # def test_login_page(self):

    #     # Find the username and password input fields and enter credentials
    #     self.type("#session_username", "admin")
    #     self.type("#session_password", "admin")

    #     # # Click on the login button
    #     self.click('input[type="submit"]')

    #     # Validate that we are at the correct URL (optional)
    #     self.assert_title("Tindahang Tapat Nadmin Console")

    #     # Wait for the login process to complete
    #     self.wait_for_element("",".breadcrumb-item", timeout=50)
        
        

   
    # def test_invalid_login(self):

    #     # Verify the outcome
    #     if self.is_element_present(".breadcrumb-item"):
    #         login_successful = True
    #     else:
    #         login_successful = False

    #     # Assert the result
    #     self.assertFalse(login_successful, "Login with invalid credentials should fail")

    #     time.sleep(10)

    def setUp(self):
        # Call the parent BaseCase class setup method 
        super().setUp()
        print("RUNNING BEFORE")
        
        # Open the login page
        self.login()

    def tearDown(self):
        time.sleep(10)

   
    def test_invalid_login(self):

        # Verify the outcome
        if self.is_element_present(HomePage.HOME):
            login_successful = True
        else:
            login_successful = False

        # Assert the result
        self.assertFalse(login_successful, "Login with invalid credentials should fail")

        time.sleep(10)

        

if __name__ == "__main__":
    LoginTest().run()
