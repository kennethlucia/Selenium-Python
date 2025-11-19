from selenium.common import InvalidSelectorException
from selenium.webdriver.common.by import By


class FinvizStockPage():

    driver = None
    ticker = None

    def __init__(self, driver, ticker):
        self.driver = driver
        self.ticker = ticker


    def go_back(self):
        self.driver.back()

    def quit(self):
        self.driver.quit()

    def get_table(self):
        return StockPageFundamentalsTable(self.driver, self.ticker)



class StockPageFundamentalsTable(FinvizStockPage):
    driver = None
    ticker = ""
    table = None
    locator_dict = {"FUNDAMENTALS_TABLE": [By.CSS_SELECTOR, '.js-snapshot-table-wrapper']}
    web_element_list = None

    def __init__(self, driver, ticker):
            #super().__init__(driver, ticker)
            self.driver = driver
            self.ticker = ticker
            by = self.locator_dict.get("FUNDAMENTALS_TABLE")[0]
            locate = self.locator_dict.get("FUNDAMENTALS_TABLE")[1]
            self.web_element_list = self.driver.find_elements(by, locate)

            size = len(self.web_element_list)
            if size > 0:
               self.table = self.web_element_list[0]
            else:
               print("On __init__ No Table Element in List")
               self.quit()


    def inspect_table(self):


       column_names = self.table.find_elements(By.XPATH, '//td[@class="snapshot-td2 cursor-pointer w-[7%]"]')
       column_values = self.table.find_elements(By.XPATH, '//td[@class="snapshot-td2 w-[8%] "]')
       column_negative_spans = self.table.find_elements(By.XPATH, '//span[@class="color-text is-negative"]')

       labels_list = []
       values_list = []
       negatives_list = []

       for neg in column_negative_spans:
           negatives_list.append(neg.text)

       for name in column_names:
           labels_list.append(name.text)

       for value in column_values:
           if value.text in negatives_list:
              if '-' in value.text:
                 values_list.append(value.text)
              else:
                 values_list.append("-"+value.text)
           else:
               values_list.append(value.text)


       zipped_pairs = zip(labels_list, values_list)
       fundamentals_dictionary = dict(zipped_pairs)
       print(fundamentals_dictionary)




    def show_dictionary(self):
        self.inspect_table()




