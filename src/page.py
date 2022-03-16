import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from src.config import config


class BasePage(object):
    """Base class to initialize the base page that will be called from all
    pages"""

    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):

    def is_title_matches(self):
        """Verifies that the hardcoded text "Voicemod" appears in page title"""

        return "Voicemod" in self.driver.title

    def search_by_title(self, title):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, f"//a[@title='{title}']")
            )
        )
        return element

    def search_by_text(self, text):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_located_to_be_selected(
                (By.XPATH, f"//*[contains(text(), '{text}')]")
            )
        )
        return element

    def search_by_link_text(self, text):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.LINK_TEXT, text)
            )
        )
        return element

    def is_not_visible_by_class(self, class_name):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element(
                (By.CLASS_NAME, class_name)
            )
        )
        return element

    def get_element_by_id(self, identifier):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, identifier)
            )
        )
        return element

    def get_element_visible_by_id(self, identifier):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                (By.ID, identifier)
            )
        )
        return element

    def is_invisible_by_id(self, identifier):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located(
                (By.ID, identifier)
            )
        )

    def is_invisible_by_class(self, identifier):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located(
                (By.CLASS_NAME, identifier)
            )
        )

    def get_element_by_attribute_value(self, attribute, value):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, f"//*[@{attribute}='{value}']")
            )
        )
        return element

    def get_element_by_class(self, class_name):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.CLASS_NAME, class_name)
            )
        )
        return element

    @staticmethod
    def print_html(element):
        html = element.get_attribute('innerHTML')
        print(html)

    @staticmethod
    def download_wait(directory, timeout, number_of_files=None):
        seconds = 0
        download_wait = True
        while download_wait and seconds < timeout:
            time.sleep(1)
            download_wait = False
            files = os.listdir(directory)
            if number_of_files and len(files) != number_of_files:
                download_wait = True

            for file_name in files:
                if file_name.endswith('.crdownload'):
                    download_wait = True

            seconds += 1
        return seconds

    def discord_login(self):
        discord_button = self.get_element_by_attribute_value('data-testid', 'Discord')
        discord_button.click()
        email_input = self.get_element_by_attribute_value('name', 'email')
        email_input.clear()
        email_input.send_keys(config['credentials']['email'])
        password_input = self.get_element_by_attribute_value('name', 'password')
        password_input.clear()
        password_input.send_keys(config['credentials']['password'])
        submit_button = self.get_element_by_attribute_value('type', 'submit')
        submit_button.click()
        self.get_element_by_id('oauth2-authorize-header-id')
        authorize_div = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Autorizar')]")
        authorize_button = authorize_div.find_element(By.XPATH, '..')
        authorize_button.click()

    @staticmethod
    def search_card_button(card, button_type):
        element = None
        buttons = card.find_elements(By.TAG_NAME, 'button')
        for button in buttons:
            aria_label = button.get_attribute("aria-label")
            if aria_label == button_type:
                element = button
                break
        return element

    def accept_cookies(self):
        accept_all_cookies_button = self.get_element_by_attribute_value('aria-label', 'Accept all cookies')
        accept_all_cookies_button.click()
        self.is_not_visible_by_class('cookie-consent')

    def wait_title(self, text):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.title_is(text)
        )
