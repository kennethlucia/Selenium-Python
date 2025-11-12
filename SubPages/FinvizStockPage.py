
from HomePage.FinvizHomePage import FinvizHomePage

class FinvizStockPage(FinvizHomePage):

    def __init__(self, config_file='config.ini'):
        super().__init__(config_file)

    def go_back(self):
        self.driver.back()
