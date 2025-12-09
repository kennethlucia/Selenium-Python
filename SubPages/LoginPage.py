from selenium.webdriver.common.by import By

from HomePage.BasePage import BasePage
from HomePage.FinvizHomePage import FinvizHomePage


class LoginPage(BasePage):

    driver = None
    user = None
    password = None

    
    def __init__(self,driver,config_file='config.ini'):
        self.driver = driver
        self.choose_email = (By.XPATH,'//a[@href="/login-email?remember=true"]')
        self.email = (By.XPATH, '//input[@name="email"]')
        self.password_locator = (By.XPATH, '//input[@name="password"]')
        self.login = (By.XPATH, '//button[@type="submit"]')
        super().__init__(config_file)
        self.get_user_login()

        user = self.user
        password = self.password

        self.driver.find_element(*self.choose_email).click()
        self.driver.find_element(*self.email).send_keys(user)
        self.driver.find_element(*self.password_locator).send_keys(password)
        self.driver.find_element(*self.login).click()

