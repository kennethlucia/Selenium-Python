from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from BasePage import BasePage
from HomePage.FinvizStockPage import FinvizStockPage, FinvizETFPage


class FinvizHomePage(BasePage):

    driver = None

    def __init__(self, driver_param,config_file='config.ini'):
        super().__init__(config_file)
        self.login = None
        driver_param = self.create_firefox_driver()
        self.driver = driver_param

        # locators
        self.home = (By.XPATH,'//a[@href="/"]')
        self.login = (By.XPATH,'//a[@href="/login"]')
        self.search = (By.ID, '_r_1_')
        self.screener = (By.XPATH, '//a[@href="/screener.ashx"]')

        # This locator only shows up when searching for an ETF equity symbol
        self.etf_label = (By.XPATH, '//a[@title="Exchange Traded Fund"]')

        # temporary xpath to test select dropdown
        self.dividend_yield = (By.XPATH, '//select[@id="fs_fa_div"]')

        self.all_locators = [self.home,self.login,self.search,self.screener]

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

        for a_locator in self.all_locators:
            self.element_exists(a_locator)

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
        from HomePage.LoginPage import LoginPage

        if not self.is_in_account():
            self.driver.find_element(*self.login).click()
            return LoginPage(self.driver)

    def is_etf(self):
        self.driver.implicitly_wait(1)
        if len(self.driver.find_elements(*self.etf_label)) > 0:
            return True
        return False

    def is_in_account(self):
        in_account = self.config.getboolean('browsers', 'logged_in')
        if in_account:
            return True
        return False

    def element_exists(self,web_element):
        try:
            self.driver.find_element(*web_element)
        except NoSuchElementException as e:
            print(e)

    def create_api_url(self):
        url = self.driver.current_url
        filter = url.split('?')[1]
        return self.api_url + filter + '&auth=' + self.api_key


if __name__ == "__main__":
    finviz_home_page = FinvizHomePage('config.ini')
    finviz_home_page.open()
    finviz_home_page.maximize_window()
    finviz_home_page.close_tab(1)
    finviz_home_page.click_login()

    finviz_home_page.click_screener()

    url_str = finviz_home_page.create_api_url()



    equities_list = ["GOOG","PGR"]

    for equity in equities_list:

        finviz_equity_page = finviz_home_page.enter_value(equity)
        stock_ticker = finviz_equity_page.ticker
        print("")
        print(f"Stock Ticker: {stock_ticker}")

        fundamentals_table = finviz_equity_page.get_table()

        price = fundamentals_table.get_parameter("Price")
        print(f"Price: {price}")

        equity_name = fundamentals_table.get_equity_name()
        print(f"The Stock's Company Name is: {equity_name}")

        price_to_earnings = fundamentals_table.get_parameter("P/E")
        print(f"Price to Earnings: {price_to_earnings}")

        earnings = fundamentals_table.get_earnings_date()
        print(f"{earnings}")

        print(f"{equity_name} is in sector: {finviz_equity_page.get_sector()}")
        print(f"{equity_name} is in industry: {finviz_equity_page.get_industry()}")
        print("")

    fundamentals_table.quit()

