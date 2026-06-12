from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


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

    def get_product_names(self, driver):
        driver.get(self.url)
        names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        return [n.text for n in names]

    def get_product_prices(self, driver):
        driver.get(self.url)
        prices = driver.find_elements(By.CLASS_NAME, "inventory-item-price")
        return [float(p.text.replace("$", "")) for p in prices]

    def sort_by(self, driver, value):
        # value options: "az", "za", "lohi", "hilo"
        driver.get(self.url)
        dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
        dropdown.select_by_value(value)