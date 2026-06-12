from selenium import webdriver
from selenium.webdriver.common.by import By


class Inventory:
    def __init__(self):
        self.url = "https://www.saucedemo.com/inventory.html"
        self.page_product_count = 6

    @staticmethod
    def config_driver():
        driver = webdriver.Edge()
        driver.maximize_window()
        return driver

    def _products_count(self, driver):
        driver.get(self.url)
        products = driver.find_elements(By.XPATH, '//div[@class="inventory_item"]')
        return len(products)
