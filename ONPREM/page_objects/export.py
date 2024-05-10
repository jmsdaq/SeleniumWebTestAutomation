from seleniumbase import BaseCase

class ExportPage(BaseCase):
    EXPORT_MENU = "//a[.='articleExports']"
    EXPORT_FROM = 'input#exported_csv_from'
    EXPORT_TO = 'input#exported_csv_to'
    EXPORT_TYPE = 'select#exported_csv_export_type'
    EXPORT_STATUS = '//*[@id="exported-csvs"]/tbody/tr[1]/td[3]/span'
    TR1_STATS = "//table[@id='exported-csvs']"
    DOWNLOAD = '//*[@id="exported-csvs"]/tbody/tr[1]/td[8]/a'
    PROCESSING = ".badge badge-style-light badge-warning"
    COMPLETED = ".badge badge-style-light badge-success"

    def export_nav(self):
        self.wait_for_element(self.SIDEBAR_ACTIVE)
        self.assert_element(self.SIDEBAR_ACTIVE) 
        self.click(self.EXPORT_MENU)