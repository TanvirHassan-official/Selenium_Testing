import time

from app.login import Login
from app.inventory import Inventory


def test_total_products():
    login_page = Login()
    driver = login_page.config_driver()

    try:
        login_page.login(driver, login_page.correct_username, login_page.correct_password)

        inventory_page = Inventory()
        product_count = inventory_page._products_count(driver)

        assert product_count == inventory_page.page_product_count
    finally:
        driver.quit()


def test_product_exists():
    login_page = Login()
    driver = login_page.config_driver()

    try:
        login_page.login(driver, login_page.correct_username, login_page.correct_password)

        inventory_page = Inventory()
        names = inventory_page.get_product_names(driver)

        assert "Sauce Labs Backpack" in names
        assert "Nonexistent Product" not in names
    finally:
        driver.quit()


def test_sort_price_low_to_high():
    login_page = Login()
    driver = login_page.config_driver()

    try:
        login_page.login(driver, login_page.correct_username, login_page.correct_password)

        inventory_page = Inventory()
        inventory_page.sort_by(driver, "lohi")
        time.sleep(1)  # small wait so prices update before reading

        prices = inventory_page.get_product_prices(driver)

        assert prices == sorted(prices)
    finally:
        driver.quit()


def test_sort_price_high_to_low():
    login_page = Login()
    driver = login_page.config_driver()

    try:
        login_page.login(driver, login_page.correct_username, login_page.correct_password)

        inventory_page = Inventory()
        inventory_page.sort_by(driver, "hilo")
        time.sleep(1)

        prices = inventory_page.get_product_prices(driver)

        assert prices == sorted(prices, reverse=True)
    finally:
        driver.quit()


def test_sort_name_a_to_z():
    login_page = Login()
    driver = login_page.config_driver()

    try:
        login_page.login(driver, login_page.correct_username, login_page.correct_password)

        inventory_page = Inventory()
        inventory_page.sort_by(driver, "az")
        time.sleep(1)

        names = inventory_page.get_product_names(driver)

        assert names == sorted(names)
    finally:
        driver.quit()