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



class StockPageFundamentalsTable():
    driver = None
    ticker = ""
    table = None
    web_element_list = None

    def __init__(self, driver, ticker):

            self.driver = driver
            self.ticker = ticker

            self.driver.implicitly_wait(2)
            self.web_element_list = self.driver.find_elements(By.CSS_SELECTOR, '.js-snapshot-table-wrapper')
            self.columns = (By.XPATH, "//td[contains(@class, 'snapshot-td2 w-[8%] ')]")
            self.names = (By.XPATH, "//td[@class='snapshot-td2 cursor-pointer w-[7%]']")
            self.negative_values = (By.XPATH, "//span[@class='color-text is-negative']")

            size = len(self.web_element_list)
            if size > 0:
               self.table = self.web_element_list[0]
            else:
               print("On __init__ No Table Element in List")
               self.quit()


    def inspect_table(self):

       column_names = self.table.find_elements(*self.names)
       column_values = self.table.find_elements(*self.columns)
       column_negative_spans = self.table.find_elements(*self.negative_values)

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

    def quit(self):
        self.driver.quit()

    def go_back(self):
        self.driver.back()


