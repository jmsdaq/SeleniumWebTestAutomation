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

    # -------GENERAL LOCATORS--------
    # Printers
    PRINTER_NAME = "#printer_config_name"
    PRINTER_IP = "#printer_config_ip_address"
    PRINTER_PORT = "#printer_config_port"
    PRINTER_COPIES = "#printer_config_default_copies"
    PRINTER_DESC = "#printer_config_description"

    # Checkbox
    PRINTER_CONF = "#printer_config_enabled"
    IMAGE_CONF = "#config_request_image_locally"
    PENDING_CONF = "#config_enable_pending_store"
    NOTIF_CONF = "#config_new_order_notification"
    QR_CONF = "#config_qrcode_in_pdf"

    # ------------- MACPOS SETTING LOCATORS -------------
    ALLOW_LABEL = 'label.form-check-label[for="macpos_setting_incomplete_checkout_allow"]'
    ALLOW_WITH_APPROVAL_LABEL = 'label.form-check-label[for="macpos_setting_incomplete_checkout_allow_with_approval"]'
    APP_ID = ".img-responsive"


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