from app.login import Login
from app.cart import Cart


def test_add_to_cart():
    login_page = Login()
    driver = login_page.config_driver()

    try:
        login_page.login(driver, login_page.correct_username, login_page.correct_password)

        cart_page = Cart()
        cart_page.add_item(driver, "add-to-cart-sauce-labs-backpack")

        count = cart_page.get_cart_count(driver)

        assert count == "1"
    finally:
        driver.quit()