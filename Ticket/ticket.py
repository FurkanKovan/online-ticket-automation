import Ticket.constants as const
import os
import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

"""
TO-DO:
    - Implement selection for future months
    - Return a table for cheapest available tickets
    - Additional filters(?), seat availability check(?)
    - New classes for Plane, Hotel, Car, Boat sections
"""

class Ticket(webdriver.Chrome):
    def __init__(self, driver_path=const.DRIVER_PATH, close=False):
        self.driver_path = driver_path
        self.close = close # close browser at finish
        os.environ['PATH'] += self.driver_path
        super(Ticket, self).__init__() # instantiate the WebDriver class
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.close:
            self.quit()

    def getMainPage(self):
        self.get(const.BASE_URL)
        cookies_element = self.find_element(By.CSS_SELECTOR, 'a[aria-label="Cookie Policy"]')
        cookies_element.click()

    def change_currency(self, currency=None):
        currency_element = self.find_element(By.CSS_SELECTOR,
            'button[id="currency-modal-btn"]'
        )
        currency_element.click()

        selected_currency_element = self.find_element(By.CSS_SELECTOR,
            f'a[data-code="{currency}"]'
        )
        selected_currency_element.click()
    
    def select_departure(self, loc_from):
        departure_element = self.find_element(By.ID, 'origin-input')
        departure_element.click()
        departure_element.send_keys(loc_from)
        WebDriverWait(self, timeout=3, poll_frequency=1).until(lambda d: d.find_element(By.CSS_SELECTOR, 'ob-select[class="visible"]'))
        departure_element.send_keys(Keys.ENTER)

    def select_destination(self, loc_to):
        destination_element = self.find_element(By.ID, 'destination-input')
        destination_element.click()
        destination_element.send_keys(loc_to)
        WebDriverWait(self, timeout=3, poll_frequency=1).until(lambda d: d.find_element(By.CSS_SELECTOR, 'ob-select[class="visible"]'))
        destination_element.send_keys(Keys.ENTER)

    def select_departure_date(self, departure_date):
        # Check if the given date has already passed
        dep_date = departure_date.split("-")
        today = date.today()
        if int(dep_date[0]) < int(today.year):
            self.quit()
            raise Exception("Please provide a valid year.")
        elif (int(dep_date[1]) < int(today.month)) and int(dep_date[0] == int(today.year)):
            self.quit()
            raise Exception("Please provide a valid month.")
        elif (int(dep_date[2]) < int(today.day)) \
                and (int(dep_date[1]) == int(today.month)) \
                and (int(dep_date[0]) == int(today.year)):
            self.quit()
            raise Exception("Cannot pick a day that is already passed.")

        date_picker_element = self.find_element(By.TAG_NAME, 'ob-datepicker')
        date_picker_element.click()
        date_element = self.find_element(By.CSS_SELECTOR, f'button[data-date="{departure_date}"]')
        date_element.click()
        
    def search_ticket(self):
        find_ticket_element = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        find_ticket_element.submit()
