import configparser
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from pathlib import Path
import json
from colorama import Fore, Back, Style, init


class BasePage:
    user = None
    password = None


    def __init__(self, config_file='config.ini'):
        script_dir = Path(__file__).parent
        config_file_path = script_dir.parent / 'config.ini'

        self.config = configparser.ConfigParser()
        self.config.read(config_file_path)
        self.api_key = self.config.get('api', 'key')
        self.csv_file = script_dir.parent / 'export.csv'
        self.api_url = 'https://elite.finviz.com/export.ashx?'
        self.driver = None

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

        if self.config.getboolean('browsers', 'ad_block'):
            extension_path = self.config.get('driver', 'adblock_extension_path')
            driver.install_addon(extension_path, temporary=False)

        self.driver = driver
        return driver

    def get_user_login(self):
        self.user = self.config.get('user', 'username')
        self.password = self.config.get('password', 'password')

    def load_json_data_into_memory(self):
        with open("page_objects_mappings.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    def click_element(self,locator):
        if self.get_locator(locator) is None:
            raise ValueError
        else:
            locator_tuple = (By.XPATH, self.get_locator(locator))
            self.driver.find_element(*locator_tuple).click()
            return locator_tuple

    def get_locator(self, search_for_attribute):
        # 1. Read and parse the JSON file directly into a Python structure
        # with open("page_objects_mappings.json", "r", encoding="utf-8") as file:
        # data = json.load(file)

        # 2. Extract the main list of items from the "pages" key
        pages_list = self.json["pages"]

        # 3. Initialize an empty dictionary to hold our structured, parsed results
        parsed_pages = {}
        current_page_name = None
        found_xpath = None

        # 4. Iterate through the elements to map out the layout
        for element in pages_list:
            # If the element is a string, it represents the name of a new page block
            if isinstance(element, str):
                current_page_name = element
                parsed_pages[current_page_name] = []

            # If the element is a list, it contains the interactive components for the current page
            elif isinstance(element, list) and current_page_name is not None:

                # Step-processing the elements inside the sub-array
                idx = 0
                while idx < len(element):
                    item = element[idx]

                    # Scenario A: Component with an explicit label name string (e.g., "Home", followed by its config)
                    if isinstance(item, str):
                        attribute = item
                        config = element[idx + 1]  # The matching dict dictionary always follows the string label

                        parsed_pages[current_page_name].append({
                            "label": attribute,
                            "python_attribute": config.get("python-attribute"),
                            "xpath": config.get("xpath")
                        })

                        idx += 2  # Advance past both the string and the dict

                    # Scenario B: Component defined directly as a standalone dict object
                    elif isinstance(item, dict):
                        parsed_pages[current_page_name].append({
                            "label": "Generic Element",  # Default label since a string title wasn't provided
                            "python_attribute": item.get("python-attribute"),
                            "xpath": item.get("xpath")
                        })
                        self_attribute = config.get("python-attribute")
                        if (self_attribute == search_for_attribute):
                            found_xpath = config.get("xpath")
                            return found_xpath

                        idx += 1  # Advance past the dict
        if found_xpath is None:
           init(autoreset=True)
           temp_string = json.dumps(parsed_pages, indent=4)
           temp_string.replace(search_for_attribute,Fore.RED + search_for_attribute)
           print(temp_string)
        else:
           # 5. Output the neatly parsed structural dictionary
           print(json.dumps(parsed_pages, indent=4))
