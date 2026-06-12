import pytest
from selenium.webdriver.common.by import By
from app.login import Login


def test_login_success():
    login_page = Login()
    driver = login_page.config_driver()

    try:
        login_page.login(
            driver,
            login_page.correct_username,
            login_page.correct_password
        )

        # Assertion: after success, check if redirected to inventory page
        assert "inventory.html" in driver.current_url
    finally:
        driver.quit()


def test_login_failure():
    login_page = Login()
    driver = login_page.config_driver()

    try:
        login_page.login(
            driver,
            login_page.wrong_username,
            login_page.wrong_password
        )

        # Assertion: check error message is displayed
        error_msg = driver.find_element(
            By.XPATH, '//h3[@data-test="error"]'
        ).text

        assert "Username and password do not match" in error_msg
    finally:
        driver.quit()
