from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os


try:
    link = "http://suninjuly.github.io/file_input.html"
    browser = webdriver.Chrome()
    browser.get(link)

    browser.find_element(By.CSS_SELECTOR, "input.form-control[name='firstname']").send_keys("Mdcrch")
    browser.find_element(By.CSS_SELECTOR, "input.form-control[name='lastname']").send_keys("Mediocrycity")
    browser.find_element(By.CSS_SELECTOR, "input.form-control[name='email']").send_keys("mmm@mail.ru")

    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_dir, 'file.txt')
    browser.find_element(By.ID, "file").send_keys(file_path)

    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

finally:
    time.sleep(10)
    browser.quit()