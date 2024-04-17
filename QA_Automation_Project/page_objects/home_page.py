from seleniumbase import BaseCase

class HomePage(BaseCase):
    # USERNAME_INPUT = "#session_username"
    # PASSWORD_INPUT = "#session_password"
    # LOGIN_BUTTON = 'input[type="submit"]'
    # HOME = ".breadcrumb-item"
    
    def login(self):
        # Open the login page
        self.open("https://review.7.tindahang-tapat.nweca.com/nadmin")
        self.maximize_window()
        self.type("#session_username", "user")
        self.type("#session_password", "pass")
        self.click('input[type="submit"]')
        self.assert_title("Tindahang Tapat Nadmin Console")
        self.wait_for_element("", ".breadcrumb-item", timeout=50)

        
