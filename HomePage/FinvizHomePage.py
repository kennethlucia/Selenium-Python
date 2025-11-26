from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from BasePage import BasePage
from SubPages.FinvizStockPage import FinvizStockPage, FinvizETFPage


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
        self.login = (By.XPATH, '//a[@href="/login"]')
        self.etf_label = (By.XPATH, '//a[@title="Exchange Traded Fund"]')

    def get_driver(self):
        return self.driver

    def open(self):
        self.driver.get(self.get_url())


    def get_url(self):
        return "https://www.finviz.com"



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


        if self.is_etf():
            return FinvizETFPage(self.driver, value)
        else:
            return FinvizStockPage(self.driver,value)

    def click_screener(self):
        self.driver.find_element(*self.screener).click()

    def click_home(self):
        self.driver.find_element(*self.home).click()

    def click_login(self):
        from SubPages.LoginPage import LoginPage

        self.driver.find_element(*self.login).click()
        return LoginPage(self.driver)

    def is_etf(self):
        self.driver.implicitly_wait(1)
        if len(self.driver.find_elements(*self.etf_label)) > 0:
            return True
        return False


if __name__ == "__main__":
    finviz_home_page = FinvizHomePage('config.ini')
    finviz_home_page.open()
    finviz_home_page.maximize_window()
    finviz_home_page.close_tab(1)
    finviz_home_page.click_login()

    #finviz_home_page.click_screener()
    #finviz_home_page.quit()

    finviz_equity_page = finviz_home_page.enter_value("AAPL")

    fundamentals_table = finviz_equity_page.get_table()
    fundamentals_table.show_dictionary()

    fundamentals_table.go_back()
    fundamentals_table.quit()

