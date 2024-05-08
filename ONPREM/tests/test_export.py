from page_objects.login import LoginPage
from page_objects.user import UserPage
from page_objects.export import ExportPage

class ExportTest(LoginPage, UserPage, ExportPage):
    def setUp(self):
        super().setUp()
        print("Running setup before test")
        # Perform login using HomePage's login method
        self.login()

    def tearDown(self):
        self.sleep(10) 
        super().tearDown()

    def test_export(self):
        self.export_nav()
        self.sleep(3)

        # >>>>>>>>>> ADD NEW EXPORT <<<<<<<<<<
        self.click(self.ADD_BTN)
        self.sleep(2)
        self.assert_element(self.MODAL)
        self.assert_text("New Export", "h1")
        self.type(self.EXPORT_FROM, "05072024")
        self.type(self.EXPORT_TO, "06072024")

        select_type = self.EXPORT_TYPE
        self.click(select_type)
        # Assuming you want to select the option with the value "order", locate it
        option_value = "order"
        option_locator = f"option[value='{option_value}']"
        
        # Click on the option to select it
        self.click(option_locator)
        self.click(self.SUBMIT)
        self.assert_text("Exporting data. This might take a while...", "h2")
        self.sleep(5)
        self.assert_text("processing", self.EXPORT_STATUS)
        
    
        # >>>>>>>>>> DOWNLOAD <<<<<<<<<<
        self.click(self.DOWNLOAD)