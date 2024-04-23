from seleniumbase import BaseCase
from selenium.webdriver.support.ui import Select

class UserPage(BaseCase):

    # WAREHOUSE LOCATORS
    SIDEBAR_ACTIVE = ".app-sidebar"
    USER_MENU = "//a[contains(text(), 'Users')]"
    WAREHOUSE_MENU = "a[data-sidebars-target='menu'][href='/nadmin/app_users']"

    ADD_BTN = ".btn.btn-success"
    USERNAME = "input.form-control[name='user[name]']"
    E_CODE = "input.form-control[name='user[employee_code]']"
    username = "input.form-control[name='user[username]']"
    password = "input.form-control[name='user[password]']"
    

    # ONPREM LOCATORS
    ONPREM_MENU = 'a[data-sidebars-target="menu"][href="/nadmin/users"]'