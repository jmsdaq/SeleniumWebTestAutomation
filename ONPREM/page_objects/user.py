from seleniumbase import BaseCase
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import random

class UserPage(BaseCase):

    # WAREHOUSE LOCATORS
    SIDEBAR_ACTIVE = ".app-sidebar"
    USER_MENU = "//a[contains(text(), 'Users')]"
    WAREHOUSE_MENU = "a[data-sidebars-target='menu'][href='/nadmin/app_users']"

    # ADD FORM LOCALTORS
    MODAL = "#appModalContent"
    ADD_BTN = ".btn.btn-success"
    NAME = 'input#user_name.form-control'
    EMPLOYEE_CODE = 'input#user_employee_code.form-control'
    USERNAME = 'input#user_username'
    PASSWORD = 'input#user_password.form-control'
    PASSWORD_CONF = 'input#user_password_confirmation.form-control'
    PIN = 'input#user_pin.form-control'
    OPERATIONAL_ROLE = 'select#user_operation_role.form-select'
    SUBMIT = 'input[type="submit"]'
    CLOSE_ICON = ".btn-close"
    CLOSE_BTN = 'button.btn-warning[data-bs-dismiss="modal"]'
    ERRORS = "#errors"
    FOOTER = ".modal-footer"
    HEADER = ".modal-header"

    # SEARCH LOCATORS
    SEARCH = 'input[type="search"][aria-controls="app-users"]'
    TABLE = ".dataTables_wrapper no-footer"
    TABLE_ROWS = '#app-users tbody tr'
    EMPTY_TABLE = ".dataTables_empty"
    AVATAR = '//*[@id="app-users"]/tbody/tr/td[2]'
    CHOOSE_IMG = "#user_image_url"
    POPUP = "#swal2-title"

    # SHOW ENTRIES LOCATORS
    SHOW = "select[name='app-users_length']"


    TR1 = '//*[@id="app-users"]/tbody/tr[1]/td[8]/div'

    # EDIT LOCATORS
    EDIT_MODAL_TITLE = ".modal-title fs-5"
    UPDATE_BTN = 'input[type="submit"][value="Update User"]'

    # ONPREM LOCATORS
    ONPREM_MENU = 'a[data-sidebars-target="menu"][href="/nadmin/users"]'
    CARD_TITLE = '.card-title'
    DANGER = 'div.text-danger'
    ON_USERNAME = 'input#nadmin_user_username.form-control'
    ON_NAME = 'input#nadmin_user_name.form-control'
    ON_PW = 'input#nadmin_user_password.form-control'
    ON_PW_CONF = 'input#nadmin_user_password_confirmation.form-control'
    ON_ROLE = '#nadmin_user_role_id'
    ON_SEARCH = 'input[type="search"][aria-controls="nadmin-users"]'
    ON_SHOW = "select[name='nadmin-users_length']"
    ON_TABLE_ROWS = '#nadmin-users tbody tr'
    ON_TR1 = '//*[@id="nadmin-users"]/tbody/tr[1]/td[8]/div'


    def user_nav(self):
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE) 
        self.click(self.USER_MENU) 

    def warehouse_nav(self):
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE)  # Verify if the sidebar is active (from PartnersPage)
        self.sleep(2)
        self.click(self.USER_MENU)  # Click on the Partner Accounts menu (from PartnersPage)
        self.sleep(2)
        self.click(self.WAREHOUSE_MENU)

    def onprem_user_nav(self):
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE)  # Verify if the sidebar is active (from PartnersPage)
        self.sleep(2)
        self.click(self.USER_MENU)  # Click on the Partner Accounts menu (from PartnersPage)
        self.sleep(2)
        self.click(self.ONPREM_MENU)

    def scroll_with_actions(self, element):
        # Scroll down to the specified element using ActionChains
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.perform()

    def scroll_up(self):
        header_element = self.find_element(".modal-header")
        self.scroll_with_actions(header_element)
    
    def scroll_up_header(self):
        header_element = self.find_element(".table-light")
        self.scroll_with_actions(header_element)

    def scroll_down(self):
        footer_element = self.find_element(".modal-footer")
        self.scroll_with_actions(footer_element)

    def generate_fake_warehouse_data(self):
        faker = Faker()
        wh_data = {
            'name': faker.name(),
            'employee_code': faker.random_number(digits=6),
            'username': faker.user_name(),
            'password': faker.password(length=10, special_chars=True, digits=True),
            'pin': faker.random_number(digits=4),
            'operation_role': faker.random_element(elements=["cashier", "picker", "packer", "checker", "supervisor", "dispatcher"])
        }
        return wh_data
    
    def generate_fake_onprem_data(self):
        faker = Faker()
        onprem_data = {
            'name': faker.name(),
            'username': faker.user_name(),
            'password': faker.password(length=10, special_chars=True, digits=True),
            'role': faker.random_element(elements=["admin", "warehouse", "Assistant Admin", "test role", "TestRaj", "Intern"])
        }
        return onprem_data