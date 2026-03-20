from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from BasePage import BasePage
from FinvizStockPage import FinvizStockPage, FinvizETFPage
import requests


def get_url():
    return "https://www.finviz.com"


class FinvizHomePage(BasePage):
    driver = None

    def __init__(self, config_file='config.ini'):
        super().__init__(config_file)
        self.login = None
        self.driver = self.create_firefox_driver()

        # locators
        self.home = (By.XPATH, '//a[@href="/" and text()="Home"]')
        self.login = (By.XPATH, '//a[@href="/login"]')
        self.search = (By.ID, '_r_1_')
        self.screener = (By.XPATH, '//a[@href="/screener.ashx"]')
        self.decriptive = (By.XPATH, "//div[text()='Descriptive']")
        self.fundamental = (By.XPATH, "//div[text()='Fundamental']")
        self.technical = (By.XPATH, "//div[text()='Technical']")
        self.etf = (By.XPATH, "//div[text()='ETF']")

        # This locator only shows up when searching for an ETF equity symbol
        self.etf_label = (By.XPATH, '//a[@title="Exchange Traded Fund"]')

        # temporary xpath to test select dropdown
        self.dividend_yield = (By.XPATH, '//select[@id="fs_fa_div"]')

        self.all_locators = [self.home, self.login, self.search, self.screener]

    def get_driver(self):
        return self.driver

    def open(self):
        self.driver.get(get_url())

    def quit(self):
        self.driver.quit()

    def close(self):
        self.driver.close()

    def close_tab(self, tab_number):
        window_handles = self.driver.window_handles

        # point driver at extra tab window_handle (Adobe Adblock Installed Tab) and close it.
        self.driver.switch_to.window(window_handles[tab_number])
        print("Tab with Label: " + str("'" + self.driver.title + "'") + " Has Been Closed")
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
        self.driver.find_element(*self.search).send_keys(value + Keys.ENTER)
        firefox_driver = self.driver
        if self.is_etf():
            return FinvizETFPage(firefox_driver, value)
        else:
            return FinvizStockPage(firefox_driver, value)

    def click_screener(self):
        self.driver.find_element(*self.screener).click()
        return ScreenerPage(self.driver)
    def click_descriptive(self):
        self.driver.find_element(*self.decriptive).click()
        return DescriptiveScreener(self.driver)
    def click_fundamental(self):
        self.driver.find_element(*self.fundamental).click()
        return FundamentalScreener(self.driver)
    def click_etf(self):
        self.driver.find_element(*self.etf).click()
        return ETFScreener(self.driver)
    def click_technical(self):
        self.driver.find_element(*self.technical).click()
        return TechnicalScreener(self.driver)

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

    def element_exists(self, web_element):
        try:
            self.driver.find_element(*web_element)
        except NoSuchElementException as e:
            print(e)

    def create_api_url(self):
        url = self.self.driver.current_url
        filter = url.split('?')[1]
        return self.api_url + filter + '&auth=' + self.api_key

    def send_api_request(self):
        built_url = self.create_api_url()
        response = requests.get(built_url)
        open(self.csv_file, "wb").write(response.content)


class ScreenerPage:

    def __init__(self, driver):
        self.driver = driver
        self.overview = (By.XPATH, "//a[text()='Overview']")
        self.valuation = (By.XPATH, "//a[text()='Valuation']")
        self.financial = (By.XPATH, "//a[text()='Financial']")
        self.ownership = (By.XPATH, "//a[text()='Ownership']")
        self.performance = (By.XPATH, "//a[text()='Performance']")
        self.technical = (By.XPATH, "//a[text()='Technical']")
        self.etfperf = (By.XPATH, "//a[text()='ETF Perf']")

    def click_overview(self):
        self.driver.find_element(*self.overview).click()

    def click_valuation(self):
        self.driver.find_element(*self.valuation).click()

    def click_financial(self):
        self.driver.find_element(*self.financial).click()

    def click_ownership(self):
        self.driver.find_element(*self.ownership).click()

    def click_performance(self):
        self.driver.find_element(*self.performance).click()

    def click_technical(self):
        self.driver.find_element(*self.technical).click()

    def click_etfperformance(self):
        self.driver.find_element(*self.etfperf).click()

class DescriptiveScreener:

    def __init__(self, driver):
        self.driver = driver

        self.exchange = (By.XPATH, '//select[@id="fs_exch"]')

    def select_exchange(self, value):
        select = Select(self.driver.find_element(*self.exchange))
        select.select_by_visible_text(value)
class FundamentalScreener:

    def __init__(self, driver):
        self.driver = driver

        #locators for Fundamental Screener
        self.price_to_earning = (By.XPATH, '//select[@id="fs_fa_pe"]')

    def select_ptoe(self,value):
        select = Select(self.driver.find_element(*self.price_to_earning))
        select.select_by_visible_text(value)

class TechnicalScreener:

    def __init__(self, driver):
        self.driver = driver

        #locators
        self.performance = (By.XPATH, '//select[@id="fs_ta_perf"]')

    def select_performance(self,value):
        select = Select(self.driver.find_element(*self.performance))
        select.select_by_visible_text(value)

class ETFScreener:

    def __init__(self, driver):
        self.driver = driver

        #locators
        self.single_category = (By.XPATH, '//select[@id="fs_etf_category"]')

    def select_single_category(self,value):
        select = Select(self.driver.find_element(*self.single_category))
        select.select_by_visible_text(value)


if __name__ == "__main__":
    finviz_home_page = FinvizHomePage('config.ini')
    finviz_home_page.open()
    finviz_home_page.maximize_window()
    finviz_home_page.close_tab(1)
    finviz_home_page.click_login()

    screener_page = finviz_home_page.click_screener()
    screener_page.click_valuation()
    screener_page.click_technical()
    screener_page.click_performance()
    screener_page.click_etfperformance()
    screener_page.click_overview()
    screener_page.click_financial()
    screener_page.click_ownership()

    descriptive_screener = finviz_home_page.click_descriptive()
    descriptive_screener.select_exchange("AMEX")

    fundamental_screener = finviz_home_page.click_fundamental()
    fundamental_screener.select_ptoe("Under 25")

    technical_screener = finviz_home_page.click_technical()
    technical_screener.select_performance("Today +15%")

    etf_screener = finviz_home_page.click_etf()
    etf_screener.select_single_category("Bonds - Inflation protected")

    equities_list = ["GOOG", "PGR"]

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
