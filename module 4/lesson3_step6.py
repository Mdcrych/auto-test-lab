import math
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
# 1. Импортируем TimeoutException
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoAlertPresentException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    def is_disappeared(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException). \
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    # 2. Исправляем обработку исключений
    def solve_quiz_and_get_code(self):
        try:
            alert = WebDriverWait(self.browser, 5).until(EC.alert_is_present())
            x = alert.text.split(" ")[2]
            answer = str(math.log(abs(12 * math.sin(float(x)))))
            alert.send_keys(answer)
            alert.accept()
            try:
                alert = WebDriverWait(self.browser, 5).until(EC.alert_is_present())
                alert_text = alert.text
                print(f"Your code: {alert_text}")
                alert.accept()
            except TimeoutException:
                print("No second alert presented")
        except TimeoutException:
            print("No alert presented for quiz")


class ProductPage(BasePage):
    ADD_TO_BASKET_BUTTON = (By.CSS_SELECTOR, ".btn-add-to-basket")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product_main h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product_main .price_color")
    MESSAGE_PRODUCT_ADDED = (By.CSS_SELECTOR, "div.alert-success .alertinner strong")
    MESSAGE_BASKET_TOTAL = (By.CSS_SELECTOR, ".alert-info .alertinner strong")

    def add_product_to_basket(self):
        self.browser.find_element(*self.ADD_TO_BASKET_BUTTON).click()

    def should_be_correct_product_added_message(self):
        product_name = self.browser.find_element(*self.PRODUCT_NAME).text
        message_product = self.browser.find_element(*self.MESSAGE_PRODUCT_ADDED).text
        assert product_name == message_product, \
            f"Expected product name '{product_name}', but got '{message_product}' in success message."

    def should_be_correct_basket_price(self):
        product_price = self.browser.find_element(*self.PRODUCT_PRICE).text
        basket_total = self.browser.find_element(*self.MESSAGE_BASKET_TOTAL).text
        assert product_price == basket_total, \
            f"Expected basket total '{product_price}', but got '{basket_total}'."

    def should_not_be_success_message(self):
        assert self.is_not_element_present(*self.MESSAGE_PRODUCT_ADDED), \
            "Success message is presented, but should not be"

    def success_message_should_disappear(self):
        assert self.is_disappeared(*self.MESSAGE_PRODUCT_ADDED), \
            "Success message has not disappeared, but it should have"


@pytest.fixture(scope="function")
def browser():
    print("\nstart browser for test..")
    browser = webdriver.Chrome()
    yield browser
    print("\nquit browser..")
    browser.quit()


# --- ПАРАМЕТРИЗОВАННЫЙ ТЕСТ (ТЕПЕРЬ ДОЛЖЕН РАБОТАТЬ) ---
@pytest.mark.parametrize('link', [
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer0",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer1",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer2",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer3",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer4",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer5",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer6",
    pytest.param("http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer7",
                 marks=pytest.mark.xfail),
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer8",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer9"
])
def test_guest_can_add_product_to_basket(browser, link):
    page = ProductPage(browser, link)
    page.open()
    page.add_product_to_basket()
    page.solve_quiz_and_get_code()
    page.should_be_correct_product_added_message()
    page.should_be_correct_basket_price()


# --- НОВЫЕ ОТРИЦАТЕЛЬНЫЕ ТЕСТЫ ---
link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"


@pytest.mark.xfail
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    page = ProductPage(browser, link)
    page.open()
    page.add_product_to_basket()
    page.should_not_be_success_message()


def test_guest_cant_see_success_message(browser):
    page = ProductPage(browser, link)
    page.open()
    page.should_not_be_success_message()


@pytest.mark.xfail
def test_message_disappeared_after_adding_product_to_basket(browser):
    page = ProductPage(browser, link)
    page.open()
    page.add_product_to_basket()
    page.success_message_should_disappear()