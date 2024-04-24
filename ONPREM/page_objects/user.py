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
    USERNAME = "#user_name" # "input.form-control[name='user[name]']"
    EMPLOYEE_CODE = "input.form-control[name='user[employee_code]']"
    USERNAME = "input.form-control[name='user[username]']"
    PASSWORD = "input.form-control[name='user[password]']"
    PIN = "input.form-control[name='user[pin]']"
    OPERATIONAL_ROLE = "input.form-control[name='user[operational_role]']"
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