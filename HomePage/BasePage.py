import configparser
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from pathlib import Path


class BasePage:

    def __init__(self, config_file='config.ini'):
        script_dir = Path(__file__).parent
        config_file_path = script_dir.parent / 'config.ini'
        print(config_file_path)
        self.config = configparser.ConfigParser()
        self.config.read(config_file_path)

    def create_firefox_driver(self):
        # Get GeckoDriver path from INI file
        geckodriver_path = self.config.get('driver', 'gecko_driver_path')

        # Create Firefox service with the driver path
        service = Service(executable_path=geckodriver_path)

        # Create Firefox options
        options = Options()

        if self.config.getboolean('browsers', 'headless'):
            options.add_argument("--headless")

        # Optional: Set Firefox binary path if specified
        if self.config.has_option('driver', 'firefox_binary_path'):
            firefox_binary = self.config.get('driver', 'firefox_binary_path')
            options.binary_location = firefox_binary

        # Create and return the driver
        driver = webdriver.Firefox(service=service, options=options)

        return driver


#if __name__ == "__main__":
    #factory = BasePage('config.ini')
    #driver = factory.create_firefox_driver()

    # Use the driver
    #driver.get(url)
    #print(driver.title)

    # Clean up
    #driver.quit()