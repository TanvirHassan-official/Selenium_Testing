from selenium import webdriver
from selenium.webdriver.common.by import By


class Cart:
    def __init__(self):
        self.url = "https://www.saucedemo.com/inventory.html"

    @staticmethod
    def config_driver():
        driver = webdriver.Edge()
        driver.maximize_window()
        return driver

    def add_item(self, driver, button_id):
        driver.get(self.url)
        driver.find_element(By.ID, button_id).click()

    def get_cart_count(self, driver):
        return driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text