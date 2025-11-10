from BasePage import BasePage


class FinvizHomePage(BasePage):

    def __init__(self, config_file='config.ini'):
        super().__init__(config_file)

    def get_url(self):
        return "https://www.finviz.com"


if __name__ == "__main__":
    factory = FinvizHomePage('config.ini')
    driver = factory.create_firefox_driver()

    # Use the driver
    driver.get(factory.get_url())
    print(driver.title)

    # Clean up
    driver.quit()
