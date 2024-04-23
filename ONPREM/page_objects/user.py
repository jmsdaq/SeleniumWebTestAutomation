from seleniumbase import BaseCase
from selenium.webdriver.support.ui import Select
from faker import Faker
import random
import string

class WarehouseUserPage(BaseCase):
    SIDEBAR_ACTIVE = ".app-sidebar"
    USER_MENU = "a[href='#'] > .material-icons-two-tone"
    WH_MENU = 'a[data-sidebars-target="menu"].active'
    ONPREM_MENU = 'a[data-sidebars-target="menu"][href="/nadmin/users"]'