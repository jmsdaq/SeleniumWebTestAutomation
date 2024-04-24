from seleniumbase import BaseCase
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from faker import Faker

class UserPage(BaseCase):

    # WAREHOUSE LOCATORS
    SIDEBAR_ACTIVE = ".app-sidebar"
    USER_MENU = "//a[contains(text(), 'Users')]"
    WAREHOUSE_MENU = "a[data-sidebars-target='menu'][href='/nadmin/app_users']"

    # ADD FORM LOCALTORS
    MODAL = "#appModalContent"
    ADD_BTN = ".btn.btn-success"
    NAME = '#user_name.form-control'
    EMPLOYEE_CODE = 'input#user_employee_code.form-control'
    USERNAME = 'input#user_username.form-control'
    PASSWORD = 'input#user_password.form-control'
    PIN = 'input#user_pin.form-control'
    OPERATIONAL_ROLE = 'select#user_operation_role.form-select'
    SUBMIT = 'input[type="submit"]'
    CLOSE_ICON = ".btn-close"
    CLOSE_BTN = 'button.btn-warning[data-bs-dismiss="modal"]'
    ERRORS = "#errors"


    # ONPREM LOCATORS
    ONPREM_MENU = 'a[data-sidebars-target="menu"][href="/nadmin/users"]'

    def scroll_with_actions(self, element):
        # Scroll down to the specified element using ActionChains
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.perform()

    def scroll_up(self):
        header_element = self.find_element(".modal-header")
        self.scroll_with_actions(header_element)

    def scroll_down(self):
        footer_element = self.find_element(".modal-footer")
        self.scroll_with_actions(footer_element)

    def generate_fake_user_data(self):
        faker = Faker()
        user_data = {
            'name': faker.name(),
            'employee_code': faker.random_number(digits=6),
            'username': faker.user_name(),
            'password': faker.password(length=10, special_chars=True, digits=True),
            'pin': faker.random_number(digits=4),
            'operation_role': faker.random_element(elements=["cashier", "picker", "packer", "checker", "supervisor", "dispatcher"])
        }
        return user_data