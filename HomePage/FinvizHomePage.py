from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from BasePage import BasePage
from SubPages.FinvizStockPage import FinvizStockPage


class FinvizHomePage(BasePage):

    driver = None

    def __init__(self, driver_param,config_file='config.ini'):
        super().__init__(config_file)
        driver_param = self.create_firefox_driver()
        self.driver = driver_param
        # Map locators
        self.search = (By.CSS_SELECTOR, '#«r1»')
        self.home = (By.XPATH, '//a[@href="/"]')
        self.screener = (By.XPATH, '//a[@href="/screener.ashx"]')

    def get_driver(self):
        return self.driver

    def open(self):
        self.driver.get(self.get_url())

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

        # point driver at extra tab window_handle (Adobe Adblock Installed Tab) and close it.
        self.driver.switch_to.window(window_handles[tab_number])
        print("Tab with Label: " + str("'"+self.driver.title+"'") + " Has Been Closed")
        self.close()

        # get the updated windows_handles array and point driver at the remaining tab handle - there should  only
        # be one in the window_handles array. This is the Finviz webpage.
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[0])

    def maximize_window(self):
        self.driver.maximize_window()

    def enter_value(self, value):
        self.driver.find_element(*self.search).send_keys(value+Keys.ENTER)

        return FinvizStockPage(self.driver,value)

    def click_screener(self):
        self.driver.find_element(*self.screener).click()

    def click_home(self):
        dict = self.locator_dict
        by = dict.get("HOME")
        self.driver.find_element(*self.home).click()

if __name__ == "__main__":
    finviz_home_page = FinvizHomePage('config.ini')
    finviz_home_page.open()
    finviz_home_page.maximize_window()
    finviz_home_page.close_tab(1)
    #finviz_home_page.click_screener()
    #finviz_home_page.quit()

    finviz_stock_page = finviz_home_page.enter_value("AAPL")
    fundamentals_table = finviz_stock_page.get_table()
    fundamentals_table.show_dictionary()

    fundamentals_table.go_back()
    fundamentals_table.quit()

