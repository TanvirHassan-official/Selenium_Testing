# Selenium + Pytest Exam Survival Guide
 
This guide is built around the SauceDemo site (`https://www.saucedemo.com/`) since your project already targets it, but every pattern here works for *any* website your faculty gives you. The trick to a Selenium exam is recognizing that almost every scenario is the same loop:
 
**open browser → find element(s) → do something → wait → check the result (assert)**
 
---
 
## 1. Project Structure (Page Object Model)
 
Your README already describes the right idea — separate "what's on the page" from "what the test checks." This is called the **Page Object Model (POM)**.
 
```
project/
├── pages/
│   ├── login_page.py        # locators + actions for the login page
│   └── inventory_page.py     # locators + actions for the products page
├── tests/
│   ├── test_login.py
│   ├── test_products.py
│   └── conftest.py           # shared pytest fixtures (driver setup/teardown)
├── requirements.txt
└── README.md
```
 
**Why bother with this in an exam?** Even if you write everything in one file because of time pressure, *think* in this structure:
- One section/class = locators (IDs, XPaths, CSS selectors)
- One section/class = actions (login(), sort_by(), get_product_names())
- The actual `test_*` functions just call those actions and `assert`
This keeps your code readable and is exactly what examiners expect to see.
 
### conftest.py — the driver fixture
 
Pytest fixtures avoid repeating setup/teardown in every test. Put this in `conftest.py` so every test file can use it automatically:
 
```python
import pytest
from selenium import webdriver
 
@pytest.fixture
def driver():
    drv = webdriver.Chrome()   # or webdriver.Firefox()
    drv.maximize_window()
    drv.implicitly_wait(5)     # wait up to 5s when finding elements
    yield drv                  # test runs here
    drv.quit()                 # cleanup after test
```
 
Then any test just takes `driver` as a parameter:
 
```python
def test_example(driver):
    driver.get("https://www.saucedemo.com/")
    # ... test code ...
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
4. **Avoid copying long auto-generated XPaths** (like `/html/body/div/div/div[2]/...` from your `app.py`) — they break easily if the page changes even slightly. Prefer short, meaningful ones.
---
 
## 3. Waits — Don't Just Use `time.sleep()`
 
Your `app.py` uses `time.sleep(2)` everywhere. It *works*, but it's slow and unreliable (sometimes 2s isn't enough, sometimes it's wasted time). For an exam, knowing **explicit waits** will impress:
 
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "login-button")))
element.click()
```
 
If you're short on time, `time.sleep(1-2)` is acceptable as a fallback — just know explicit waits exist and why they're better (they wait *only as long as needed*, up to a max).
 
---
 
## 4. Scenario 1: Valid / Invalid Login
 
This is the most common exam scenario. Pattern: **enter credentials → click login → check the result (success page OR error message)**.
 
### Page Object (pages/login_page.py)
```python
from selenium.webdriver.common.by import By
 
class LoginPage:
    URL = "https://www.saucedemo.com/"
 
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
 
    def __init__(self, driver):
        self.driver = driver
 
    def load(self):
        self.driver.get(self.URL)
 
    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
 
    def get_error_text(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text
```
 
### Tests (tests/test_login.py)
```python
from pages.login_page import LoginPage
 
def test_login_success(driver):
    login = LoginPage(driver)
    login.load()
    login.login("standard_user", "secret_sauce")
 
    # successful login redirects to /inventory.html
    assert "inventory" in driver.current_url
 
def test_login_failure(driver):
    login = LoginPage(driver)
    login.load()
    login.login("wrong_user", "wrong_pass")
 
    error_text = login.get_error_text()
    assert "Username and password do not match" in error_text
 
def test_locked_out_user(driver):
    login = LoginPage(driver)
    login.load()
    login.login("locked_out_user", "secret_sauce")
 
    error_text = login.get_error_text()
    assert "locked out" in error_text.lower()
```
 
**Key takeaway:** for "valid" you assert something that proves success (URL changed, a known element appears, page title changed). For "invalid" you assert the **error message text** appears.
 
**General tip:** if the exam site isn't SauceDemo, the same shape applies — just inspect the site to find:
- the username/password field IDs
- the login button
- what changes on success (URL, a welcome message, a logout button appearing)
- what error message appears on failure (and its locator)
---
 
## 5. Scenario 2: Check if a Category/Product Exists
 
Pattern: **get all items of that type as text → check if the target string is in that list**.
 
```python
def test_product_exists(driver):
    driver.get("https://www.saucedemo.com/inventory.html")
 
    product_names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    names_text = [el.text for el in product_names]
 
    assert "Sauce Labs Backpack" in names_text
    assert "Nonexistent Product" not in names_text
```
 
For checking a **category** on a different site (e.g. an e-commerce site with a nav menu):
```python
def test_category_exists(driver):
    driver.get("https://example-shop.com/")
 
    categories = driver.find_elements(By.CSS_SELECTOR, "nav.menu a")
    category_names = [c.text.strip() for c in categories]
 
    assert "Electronics" in category_names
```
 
**If you're not sure of the exact class name in the exam**, inspect one item, find a shared class on the *container* (e.g. all product names share `inventory_item_name`), and grab all of them.
 
---
 
## 6. Scenario 3: Check Sorting Works
 
Pattern: **trigger the sort → read the values into a list → compare against a sorted version of that list**.
 
On SauceDemo, the sort dropdown has `data-test="product-sort-container"` with options like `Price (low to high)`.
 
```python
from selenium.webdriver.support.ui import Select
 
def test_sort_price_low_to_high(driver):
    driver.get("https://www.saucedemo.com/inventory.html")
 
    # Use Select for <select> dropdowns -- much more reliable than clicking options
    sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_dropdown.select_by_value("lohi")   # lohi = low to high, hilo = high to low
 
    price_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    prices = [float(p.text.replace("$", "")) for p in price_elements]
 
    assert prices == sorted(prices)   # check ascending order
 
def test_sort_price_high_to_low(driver):
    driver.get("https://www.saucedemo.com/inventory.html")
 
    sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_dropdown.select_by_value("hilo")
 
    price_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    prices = [float(p.text.replace("$", "")) for p in price_elements]
 
    assert prices == sorted(prices, reverse=True)
```
 
**Why `Select` instead of `.click()`?** Your `app.py` clicks the dropdown then clicks an `<option>` by XPath — this is fragile and sometimes doesn't register in headless/CI environments. The `Select` class is built specifically for `<select>` elements and is far more reliable. **This is a great thing to mention/use in your exam.**
 
For sorting by **name** (A-Z / Z-A), same idea but compare strings:
```python
names = [el.text for el in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
assert names == sorted(names)
```
 
---
 
## 7. Scenario 4: Count How Many Products Exist
 
This is the simplest one — just `len()` on a `find_elements()` list.
 
```python
def test_product_count(driver):
    driver.get("https://www.saucedemo.com/inventory.html")
 
    products = driver.find_elements(By.CLASS_NAME, "inventory_item")
    print(f"Number of products: {len(products)}")
 
    assert len(products) == 6   # SauceDemo always has 6 products
```
 
Variation — counting items matching a condition (e.g. products under $20):
```python
prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
cheap_count = sum(1 for p in prices if float(p.text.replace("$", "")) < 20)
print(f"Products under $20: {cheap_count}")
```
 
---
 
## 8. Scenario 5: "Hard" / Unexpected Problems — General Toolkit
 
When you don't know exactly what's coming, fall back on this checklist:
 
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
| Add item to cart, check cart badge | `find_element(...).text` on the cart count element |
 
**Adding to cart & checking cart count** (common SauceDemo-style task):
```python
def test_add_to_cart(driver):
    driver.get("https://www.saucedemo.com/inventory.html")
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
 
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_badge.text == "1"
```
 
**General debugging tip for the exam:** if `find_element` throws `NoSuchElementException`, print the page source (`driver.page_source`) or take a screenshot to see what's actually on screen — often the element just hasn't loaded yet (add a wait) or your locator is slightly wrong.
 
---
 
## 9. Quick Reference — Assertions
 
```python
assert actual == expected
assert "text" in some_string
assert element.is_displayed()
assert len(list_of_elements) == 6
assert "inventory" in driver.current_url
```
 
If an assertion fails, pytest shows you exactly what was expected vs actual — great for debugging mid-exam.
 
---
 
## 10. Minimal "Panic Template"
 
If you blank out, start every test with this skeleton and adapt:
 
```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
 
@pytest.fixture
def driver():
    drv = webdriver.Chrome()
    drv.maximize_window()
    drv.implicitly_wait(5)
    yield drv
    drv.quit()
 
def test_something(driver):
    driver.get("https://example.com/")
 
    # 1. Find element(s)
    element = driver.find_element(By.ID, "some-id")
 
    # 2. Do something
    element.click()
 
    # 3. Assert the result
    assert "expected" in driver.page_source
```
 
Good luck tomorrow!