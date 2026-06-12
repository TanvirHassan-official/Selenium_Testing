# Selenium + Pytest Exam Survival Guide

This guide is built around the SauceDemo site (`https://www.saucedemo.com/`) since your project already targets it, but every pattern here works for *any* website your faculty gives you. The trick to a Selenium exam is recognizing that almost every scenario is the same loop:

**open browser → find element(s) → do something → wait → check the result (assert)**

---

## 1. Project Structure (Page Object Model)

Your project uses a simple two-folder structure — no `pages/` folder, no `conftest.py`, no extra config files:

```
Practice/
├── app/
│   ├── __init__.py
│   ├── login.py         # Login class: credentials, config_driver(), login()
│   ├── inventory.py      # Inventory class: product count, names, prices, sorting
│   └── cart.py           # Cart class: add to cart, read cart badge
├── tests/
│   ├── __init__.py
│   ├── test_login.py
│   ├── test_inventory.py
│   └── test_cart.py
├── requirements.txt
└── README.md
```

This is still the **Page Object Model (POM)** idea — "what's on the page" lives in `app/`, "what the test checks" lives in `tests/`. Each class in `app/` represents one page (or one feature area) of the site:

- A section of attributes = locators / page data (URL, expected values, credentials)
- A section of methods = actions (`login()`, `sort_by()`, `get_product_names()`, `add_item()`)
- The `test_*` functions just create the page object, call those actions, and `assert`

### No `conftest.py` — driver is created per test

Instead of a shared pytest fixture, each page class has its own `config_driver()` **static method**:

```python
class Login:
    def __init__(self):
        self.url = "https://www.saucedemo.com/"
        self.correct_username = "standard_user"
        self.correct_password = "secret_sauce"

    @staticmethod
    def config_driver():
        driver = webdriver.Edge()
        driver.maximize_window()
        return driver
```

`@staticmethod` means this method doesn't need `self` — it doesn't depend on any particular instance's data, it just builds and returns a browser. That's why it can be called either as `login_page.config_driver()` or directly as `Login.config_driver()`.

Every test follows the same shape:

```python
def test_example():
    page = SomeClass()
    driver = page.config_driver()

    try:
        # ... do something with driver ...
        assert ...
    finally:
        driver.quit()
```

Run with:
```bash
pytest -v
pytest -v tests/test_login.py
pytest -v -k "login"      # run tests whose name contains "login"
```

---

## 2. Finding Elements (Locators) — Your Most Used Skill

```python
from selenium.webdriver.common.by import By

driver.find_element(By.ID, "user-name")
driver.find_element(By.NAME, "username")
driver.find_element(By.CLASS_NAME, "inventory_item_price")
driver.find_element(By.CSS_SELECTOR, "button#login-button")
driver.find_element(By.XPATH, "//button[@id='login-button']")
driver.find_element(By.LINK_TEXT, "Sauce Labs Backpack")
driver.find_element(By.PARTIAL_LINK_TEXT, "Backpack")
driver.find_element(By.TAG_NAME, "h1")
```

**Multiple elements** (returns a list — essential for "how many products" or "check sorting"):
```python
products = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
print(len(products))          # count
for p in products:
    print(p.text)             # loop through text
```

### How to find a locator on the exam site
1. Right-click the element → **Inspect**
2. Look for `id`, `name`, or a unique `class`
3. If nothing unique exists, build an XPath/CSS selector using nearby text or structure
4. Prefer short, meaningful locators (`By.ID`, `By.CLASS_NAME`) over long auto-generated XPaths — they break easily if the page changes even slightly

---

## 3. Waits — `time.sleep()` vs Explicit Waits

Your current code doesn't use `time.sleep()` much, which is good — but if a page needs a moment to update (e.g. after changing a sort dropdown), a short `time.sleep(1)` is an acceptable quick fix under exam time pressure.

The "better" way is an **explicit wait**:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "login-button")))
element.click()
```

If you're short on time, `time.sleep(1-2)` is fine — just know explicit waits exist and why they're better (they wait *only as long as needed*, up to a max).

---

## 4. Login (`app/login.py` + `tests/test_login.py`)

Pattern: **enter credentials → click login → check the result (success page OR error message)**.

```python
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
```

```python
def test_login_success():
    login_page = Login()
    driver = login_page.config_driver()

    try:
        login_page.login(driver, login_page.correct_username, login_page.correct_password)
        assert "inventory.html" in driver.current_url
    finally:
        driver.quit()


def test_login_failure():
    login_page = Login()
    driver = login_page.config_driver()

    try:
        login_page.login(driver, login_page.wrong_username, login_page.wrong_password)
        error_msg = driver.find_element(By.XPATH, '//h3[@data-test="error"]').text
        assert "Username and password do not match" in error_msg
    finally:
        driver.quit()
```

**Key takeaway:** for "valid" you assert something that proves success (URL changed, a known element appears). For "invalid" you assert the **error message text**.

---

## 5. Inventory (`app/inventory.py` + `tests/test_inventory.py`)

All inventory tests log in first using the `Login` class, since the inventory page requires authentication.

```python
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
        prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        return [float(p.text.replace("$", "")) for p in prices]

    def sort_by(self, driver, value):
        # value options: "az", "za", "lohi", "hilo"
        driver.get(self.url)
        dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
        dropdown.select_by_value(value)
```

### Count products
```python
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
```

### Check a product exists
```python
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
```

### Check sorting works

`Select` is used instead of clicking the dropdown manually — it's built specifically for `<select>` elements and is far more reliable.

```python
def test_sort_price_low_to_high():
    login_page = Login()
    driver = login_page.config_driver()

    try:
        login_page.login(driver, login_page.correct_username, login_page.correct_password)

        inventory_page = Inventory()
        inventory_page.sort_by(driver, "lohi")
        time.sleep(1)  # give the page a moment to re-render

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
```

---

## 6. Cart (`app/cart.py` + `tests/test_cart.py`)

Pattern: **log in → add an item → read the cart badge → assert the count**.

```python
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
```

```python
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
```

Each product's "Add to cart" button has a unique `id` like `add-to-cart-sauce-labs-backpack` — inspect the button on the page to find the right id for the product you want.

---

## 7. Quick Reference — General Toolkit

| Need to... | Use |
|---|---|
| Click something | `.click()` |
| Type text | `.send_keys("text")` |
| Clear a field first | `.clear()` before `.send_keys()` |
| Get visible text | `.text` |
| Get an attribute (href, value, src) | `.get_attribute("href")` |
| Check if element is shown | `.is_displayed()` |
| Check a checkbox/radio state | `.is_selected()` |
| Check if enabled | `.is_enabled()` |
| Handle dropdowns | `Select(element)` |
| Wait for something to appear | `WebDriverWait` + `expected_conditions` |
| Switch between tabs/windows | `driver.window_handles`, `driver.switch_to.window(...)` |
| Handle alerts/popups | `driver.switch_to.alert`, `.accept()`, `.dismiss()` |
| Scroll to an element | `driver.execute_script("arguments[0].scrollIntoView();", element)` |
| Take a screenshot (debugging) | `driver.save_screenshot("debug.png")` |
| Go back/forward | `driver.back()`, `driver.forward()` |

**General debugging tip for the exam:** if `find_element` throws `NoSuchElementException`, print `driver.page_source` or take a screenshot to see what's actually on screen — often the element just hasn't loaded yet (add a wait) or your locator is slightly wrong.

---

## 8. Quick Reference — Assertions

```python
assert actual == expected
assert "text" in some_string
assert element.is_displayed()
assert len(list_of_elements) == 6
assert "inventory" in driver.current_url
```

If an assertion fails, pytest shows you exactly what was expected vs actual — great for debugging mid-exam.

---

## 9. Minimal "Panic Template"

If you blank out and need to write a brand-new page class + test from scratch, adapt this skeleton (matches your project's style — no fixtures, no conftest):

```python
# app/some_page.py
from selenium import webdriver
from selenium.webdriver.common.by import By


class SomePage:
    def __init__(self):
        self.url = "https://example.com/"

    @staticmethod
    def config_driver():
        driver = webdriver.Edge()
        driver.maximize_window()
        return driver

    def do_something(self, driver):
        driver.get(self.url)
        element = driver.find_element(By.ID, "some-id")
        element.click()
```

```python
# tests/test_some_page.py
from app.some_page import SomePage


def test_something():
    page = SomePage()
    driver = page.config_driver()

    try:
        page.do_something(driver)
        assert "expected" in driver.page_source
    finally:
        driver.quit()
```

Good luck tomorrow!