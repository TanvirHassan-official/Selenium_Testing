import time

from app.login import Login
from app.inventory import Inventory


def test_total_products():
    # Initialize login page and driver
    login_page = Login()
    driver = login_page.config_driver()

    try:
        # Log in with correct credentials
        login_page.login(driver, login_page.correct_username, login_page.correct_password)

        # Initialize inventory page and get product count
        inventory_page = Inventory()
        product_count = inventory_page._products_count(driver)

        # Assertion: check if product count matches expected count
        assert product_count == inventory_page.page_product_count

    finally:
        # Ensure driver quits even if test fails
        driver.quit()
