from seleniumbase import BaseCase
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ExportPage(BaseCase):
    EXPORT_MENU = "//a[.='articleExports']"
    EXPORT_FROM = 'input#exported_csv_from'
    EXPORT_TO = 'input#exported_csv_to'
    EXPORT_TYPE = 'select#exported_csv_export_type'

    def export_nav(self):
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE) 
        self.click(self.EXPORT_MENU)