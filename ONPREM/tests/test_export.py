from page_objects.login import LoginPage
from page_objects.user import UserPage
from page_objects.export import ExportPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

class ExportTest(LoginPage, UserPage, ExportPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.login()

    def tearDown(self):
        self.sleep(10) 
        super().tearDown()

    @pytest.mark.run(order=4)
    def test_export(self):
        self.export_nav()
        self.sleep(3)

        # >>>>>>>>>> ADD NEW EXPORT <<<<<<<<<<
        wait = WebDriverWait(self.driver, 10)
        add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.ADD_BTN)))
        add_btn.click()
        self.sleep(2)
        self.assert_element(self.MODAL)
        self.assert_text("New Export", "h1")
        self.type(self.EXPORT_FROM, "05012024")
        self.type(self.EXPORT_TO, "05022024")

        select_type = self.EXPORT_TYPE
        self.click(select_type)
        # Assuming you want to select the option with the value "order", locate it
        option_value = "order"
        option_locator = f"option[value='{option_value}']"
        
        # Click on the option to select it
        self.click(option_locator)
        self.click(self.SUBMIT)
        self.assert_text("Exporting data. This might take a while...", "h2")

        self.sleep(4)
        self.refresh()
        self.click(self.DOWNLOAD)