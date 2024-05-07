from page_objects.login import LoginPage
from page_objects.user import UserPage
from page_objects.setting import SettingPage
from selenium.webdriver.support import expected_conditions as EC

class WarehouseUserTest(LoginPage, UserPage, SettingPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.login()

    def tearDown(self):
        self.sleep(10) 
        super().tearDown()

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
        self.assert_text("Settings has been updated", self.POPUP)
        self.sleep(3)

        self.click(self.PENDING_CONF)
        self.click(self.PENDING_UPDATE)
        self.assert_text("Settings has been updated", self.POPUP)
        self.sleep(5)

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
        self.click(self.SUBMIT)
        self.assert_text("MacPOS settings successfully updated", "h2")
        self.sleep(5)


        # --------- WAREHOUSE DISPLAY -----------
        self.click(self.WAREHOUSE_DISPLAY)
        self.assert_element(self.POPUP)
        self.assert_text("Welcome back!", "h2")
        self.sleep(5)
