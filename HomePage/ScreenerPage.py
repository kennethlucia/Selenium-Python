from selenium.webdriver.common.by import By

from HomePage.FinvizHomePage import FinvizHomePage


class ScreenerPage(FinvizHomePage):

    def __init__(self):

        # locators of bottom row of Buttons common to all Screener Types
        self.overview = (By.XPATH, "//a[text()='Overview']")
        self.valuation = (By.XPATH, "//a[text()='Valuation']")
        self.financial = (By.XPATH, "//a[text()='Financial']")
        self.ownership = (By.XPATH, "//a[text()='Ownership']")

    def click_overview(self):
        self.driver.find_element(*self.overview).click()
