from seleniumbase import BaseCase
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import random

class SettingPage(BaseCase):

    # GENERAL SETTING LOCATORS
    SETTING = '/html/body/div[1]/div[1]/div[2]/ul/li[7]/a'
    GENERAL = 'a[data-sidebars-target="menu"][href="/nadmin/settings"]'
    MACPOS = 'a[data-sidebars-target="menu"][href="/nadmin/macpos/settings"]'
    WAREHOUSE_DISPLAY = 'a[data-sidebars-target="menu"][href="/"]'

    def setting_nav(self):
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE) 
        self.click(self.SETTING)

    def general_setting_nav(self):
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE) 
        self.click(self.SETTING)
        self.click(self.GENERAL)

    def macpos_config_setting_nav(self):
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE) 
        self.click(self.MACPOS)
        
    def warehouse_display(self):
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE) 
        self.click(self.WAREHOUSE_DISPLAY)