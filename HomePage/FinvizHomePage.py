from BasePage import BasePage



class FinvizHomePage(BasePage):

    driver = None

    def __init__(self, driver_param,config_file='config.ini'):
        super().__init__(config_file)
        driver_param = self.create_firefox_driver()
        self.driver = driver_param

    def get_url(self):
        return "https://www.finviz.com"

    def open(self):
        self.driver.get(self.get_url())

    def close(self):
        self.driver.quit()

    def maximize_window(self):
        self.driver.maximize_window()


if __name__ == "__main__":
    factory = FinvizHomePage('config.ini')
    factory.open()
    factory.maximize_window()
    factory.close()

