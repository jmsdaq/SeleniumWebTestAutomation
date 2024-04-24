from seleniumbase import BaseCase
from selenium.webdriver.support.ui import Select
from faker import Faker

class UserPage(BaseCase):

    # WAREHOUSE LOCATORS
    SIDEBAR_ACTIVE = ".app-sidebar"
    USER_MENU = "//a[contains(text(), 'Users')]"
    WAREHOUSE_MENU = "a[data-sidebars-target='menu'][href='/nadmin/app_users']"


    # ADD FORM LOCALTORS
    ADD_BTN = ".btn.btn-success"
    NAME = '#user_name.form-control'
    EMPLOYEE_CODE = 'input#user_employee_code.form-control'
    USERNAME = 'input#user_username.form-control'
    PASSWORD = 'input#user_password.form-control'
    PIN = 'input#user_pin.form-control'
    OPERATIONAL_ROLE = 'select#user_operation_role.form-select'
    SUBMIT = 'input[type="submit"]'


    # ONPREM LOCATORS
    ONPREM_MENU = 'a[data-sidebars-target="menu"][href="/nadmin/users"]'

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