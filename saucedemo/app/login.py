from selenium import webdriver
from selenium.webdriver.common.by import By


class Login:
    def __init__(self):
        self.url = "https://www.saucedemo.com/"
        self.correct_username = "standard_user"
        self.correct_password = "secret_sauce"
        self.wrong_username = "demo_user"
        self.wrong_password = "123456"

    @staticmethod
    def config_driver():
        driver = webdriver.Edge()
        driver.maximize_window()
        return driver

    def login(self, driver, username, password):
        driver.get(self.url)
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
