from selenium.webdriver.common.by import By

from HomePage.FinvizHomePage import FinvizHomePage


class LoginPage():

    driver = None
    user = None
    password = None

    
    def __init__(self,driver):
        self.driver = driver
        self.email = (By.XPATH, '//input[@name="email"]')
        self.password = (By.XPATH, '//input[@name="password"]')
        self.login = (By.XPATH, '//button[@type="submit"]')
        self.driver.find_element(*self.email).send_keys("kennethlucia@gmail.com")
        self.driver.find_element(*self.password).send_keys("Kalu2704!")
        self.driver.find_element(*self.login).click()

