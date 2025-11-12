
from HomePage.FinvizHomePage import FinvizHomePage

class FinvizStockPage(FinvizHomePage):

    def __init__(self, driver_param):
        super().__init__(driver_param)
        self.driver = driver_param

    def go_back(self):
        self.driver.back()
