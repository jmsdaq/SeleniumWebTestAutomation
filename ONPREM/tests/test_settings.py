from page_objects.login import LoginPage
from page_objects.user import UserPage
from page_objects.setting import SettingPage
from selenium.webdriver.common.by import By
import pytest

class SettingTest(LoginPage, UserPage, SettingPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.login()

    def tearDown(self):
        self.sleep(10) 
        super().tearDown()

    @pytest.mark.run(order=3)
    def test_setting(self):
        self.general_setting_nav()

        # >>>>>>>>>>> GENERAL SETTING <<<<<<<<<<<<
        self.type(self.PRINTER_NAME, "test")
        self.type(self.PRINTER_IP, "192.168.31.100")
        self.type(self.PRINTER_PORT, "9101")
        self.type(self.PRINTER_COPIES, "2")
        self.type(self.PRINTER_DESC, "test")
        self.click(self.PRINTER_CONF)
        self.click(self.PRINTER_UPDATE)
        self.assert_text("Printer settings has been updated", self.POPUP)
        self.sleep(3)

        self.scroll_to(self.LOCAL_IMAGE_UPDATE)
        self.sleep(1)
        self.click(self.APP_ID)
        self.click(self.IMAGE_CONF)
        self.click(self.LOCAL_IMAGE_UPDATE)
        self.assert_text("Settings has been updated", "h2")
        self.sleep(3)

        self.click(self.PENDING_CONF)
        self.click(self.PENDING_UPDATE)
        self.assert_text("Settings has been updated", "h2")
        self.sleep(4)


        self.click(self.TRANSACTION)
        self.sleep(2)
        self.wait_for_element(self.ORDER_MENU)
        # self.open_tab(self.ORDER_MENU)
        self.click(self.ORDER_MENU)
        self.sleep(5)
        self.select_date()
        self.click(self.O_TR1)
        self.assert_text("Order is not linked yet", "h2")
        self.sleep(3)
        self.setting_nav()

        # self.click(self.NOTIF_CONF)
        # self.click(self.NOTIF_UPDATE)
        # self.assert_text("Settings has been updated", self.POPUP)
        # self.sleep(3)

        # self.click(self.QR_CONF)
        # self.click(self.QR_UPDATE)
        # self.assert_text("Settings has been updated", self.POPUP)
        # self.sleep(3)

        # --------- MACPOS SETTING -------------
        self.click(self.MACPOS)
        self.assert_text("MacPOS Settings", "h5")
        self.sleep(3)
        self.click(self.ALLOW_LABEL)
        self.sleep(3)
        self.click(self.SUBMIT)
        self.assert_text("MacPOS settings successfully updated", "h2")
        self.sleep(5)


        # --------- WAREHOUSE DISPLAY -----------
        self.click(self.WAREHOUSE_DISPLAY)
        self.assert_text("Welcome back!", "h2")
        # Assertion: Check if URL contains "/nadmin/dashboard" path
        expected_path = "/nadmin/dashboard"
        assert expected_path in self.get_current_url(), f"Actual URL: {self.get_current_url()}"
        self.sleep(5)