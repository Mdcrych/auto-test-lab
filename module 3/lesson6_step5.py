import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

import time
import math


@pytest.fixture()
def browser():
    print("\nstart browser for test..")
    driver = webdriver.Chrome()
    yield driver
    print("\nquit browser..")
    driver.quit()


@pytest.mark.parametrize('links', ["https://stepik.org/lesson/236895/step/1",
                                   "https://stepik.org/lesson/236896/step/1",
                                   "https://stepik.org/lesson/236897/step/1",
                                   "https://stepik.org/lesson/236898/step/1",
                                   "https://stepik.org/lesson/236899/step/1",
                                   "https://stepik.org/lesson/236903/step/1",
                                   "https://stepik.org/lesson/236904/step/1",
                                   "https://stepik.org/lesson/236905/step/1"])
class TestAliens:
    def test_aliens_task(self, browser, links):
        link = links
        browser.get(link)
        browser.implicitly_wait(30)

        button_enter = browser.find_element(By.ID, "ember33")
        button_enter.click()

        input_email = browser.find_element(By.ID, "id_login_email")
        input_email.send_keys("sosal@ya.ru")

        input_password = browser.find_element(By.ID, "id_login_password")
        input_password.send_keys("fdgdfgdfgdfg")

        button_login = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
        button_login.click()
        time.sleep(10)
        try:
            browser.implicitly_wait(10)
            button_again = browser.find_element(By.CSS_SELECTOR, "button.again-btn")
            button_again.click()

        except NoSuchElementException:
            print('Кнопка "Решить снова" отсутствует')

        finally:
            time.sleep(20)
            input_answer = browser.find_element(By.TAG_NAME, 'textarea')
            input_answer.clear()

            answer = math.log(int(time.time()) - 0.034)
            answer_text = str(answer)

            input_answer.send_keys(answer_text)
            time.sleep(5)
            button_send = browser.find_element(By.CLASS_NAME, "submit-submission")
            button_send.click()

            browser.implicitly_wait(10)
            answer_feedback = browser.find_element(By.CLASS_NAME, 'smart-hints__hint')
            assert answer_feedback.text == "Correct!", "Wrong answer!"