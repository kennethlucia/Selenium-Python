from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from BasePage import BasePage



class FinvizHomePage(BasePage):

    driver = None
    SEARCH_INPUT = '«r1»'

    def __init__(self, driver_param,config_file='config.ini'):
        super().__init__(config_file)
        driver_param = self.create_firefox_driver()
        self.driver = driver_param

    def get_url(self):
        return "https://www.finviz.com"

    def open(self):
        self.driver.get(self.get_url())

    def quit(self):
        self.driver.quit()

    def close(self):
        self.driver.close()

    def close_tab(self,tab_number):
        window_handles = self.driver.window_handles

        # point driver at extra tab window handle (Adobe Adblock Installed Tab) and close it.
        self.driver.switch_to.window(window_handles[tab_number])
        print("Tab with Label: " + str("'"+self.driver.title+"'") + " Has Been Closed")
        self.close()

        # get the windows handles again and point driver at the remaining tab handle - there's only
        # one in the window_handles array. This is the Finviz webpage.
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[0])

    def maximize_window(self):
        self.driver.maximize_window()

    def enter_value(self,value):
        self.driver.find_element(By.CSS_SELECTOR,'#«r1»').send_keys(value+Keys.ENTER)


if __name__ == "__main__":
    factory = FinvizHomePage('config.ini')
    factory.open()
    factory.maximize_window()
    factory.close_tab(1)
    factory.enter_value("AAPL")
    factory.quit()

