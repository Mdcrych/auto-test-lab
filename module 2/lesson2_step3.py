from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


try:
    link = "https://suninjuly.github.io/selects1.html"
    browser = webdriver.Chrome()
    browser.get(link)

    x_element = browser.find_element(By.ID, "num1")
    x = int(x_element.text)
    y_element = browser.find_element(By.ID, "num2")
    y = int(y_element.text)
    el_sum = x + y

    select = Select(browser.find_element(By.TAG_NAME, "select"))
    select.select_by_value(str(el_sum))

    button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    button.click()


finally:
    time.sleep(10)
    browser.quit()