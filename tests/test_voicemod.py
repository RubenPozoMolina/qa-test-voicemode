import os.path
import unittest

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import page
from config import config
from file_utils import FileUtils


class TestFreeVoiceChangerSoftware(unittest.TestCase):
    """A sample test class to show how page object works"""

    file_utils = FileUtils()
    main_page = None

    def setUp(self):
        options = Options()
        self.driver = webdriver.Firefox(options=options)
        self.driver.get("http://www.voicemod.net")
        # Load the main page
        self.main_page = page.MainPage(self.driver)
        # Accept cookies
        accept_cookies_button = self.main_page.get_element_by_id("onetrust-accept-btn-handler")
        accept_cookies_button.click()
        self.main_page.is_invisible_by_id("onetrust-banner-sdk")

    def test_voice_changer_for_pc(self):
        # Search Voice Changer for PC link
        changer_link = self.main_page.search_by_title('Voice Changer for PC')
        changer_link.click()
        # Delete previous files
        self.file_utils.delete_files(config['system']['downloads_folder'], 'VoicemodSetup*.exe')
        # Click to download button
        download_button = self.main_page.search_by_class('download-button')
        download_button.click()
        self.main_page.discord_login()
        self.main_page.download_wait(config['system']['downloads_folder'], 30, 1)
        file_exists = self.file_utils.file_exists(config['system']['downloads_folder'], 'VoicemodSetup*.exe')
        assert file_exists, "Error downloading Voicemod installer"

    def test_free_sounds(self):
        # Delete previous files
        self.file_utils.delete_files(config['system']['downloads_folder'], 'el-test-ha-fallado-By-Tuna.mp3')
        # Search free sounds
        free_sounds = self.main_page.search_by_title('Free Sounds')
        free_sounds.click()
        # Put a donkey in search field
        search_input = self.main_page.get_element_by_id('search-form')
        search_input.click()
        search_input.send_keys('El test ha fallado')
        self.main_page.accept_cookies()
        search_input.send_keys(Keys.RETURN)
        # Wait until tittle changes
        self.main_page.wait_title('Search result for El test ha fallado. Meme soundboards and SFX Tuna')
        # Get first card
        cards = self.main_page.driver.find_elements(By.CLASS_NAME, 'card__content')
        card_el_test_ha_fallado = cards[0]
        # Test play button
        play_button = self.main_page.search_card_button(card_el_test_ha_fallado, "Play")
        assert play_button, "play button don't found"
        play_button.click()
        # Test pause button
        pause_button = self.main_page.search_card_button(card_el_test_ha_fallado, "Pause")
        assert pause_button, "pause button don't found"
        pause_button.click()
        # Test download button
        download_button = self.main_page.search_card_button(card_el_test_ha_fallado, "Download")
        assert download_button, "download button don't found"
        download_button.click()
        # Verify downloaded file
        file_exists = self.file_utils.file_exists(
            config['system']['downloads_folder'],
            'el-test-ha-fallado-By-Tuna.mp3'
        )
        assert file_exists, "Error downloading sound"
        original_file = os.path.abspath("sounds/el-test-ha-fallado-By-Tuna.mp3")
        downloaded_file = config['system']['downloads_folder'] + os.path.sep + 'el-test-ha-fallado-By-Tuna.mp3'
        equal_files = self.file_utils.are_file_equals(original_file, downloaded_file)
        assert equal_files, "Unexpected file"

    def test_careers(self):
        # Verify careers redirect to jobs.eu.lever.co
        about_us = self.main_page.search_by_title('About Us')
        about_us.click()
        careers = self.main_page.get_element_by_attribute_value('title', 'Careers')
        careers.click()
        self.main_page.wait_title('Careers')
        explore_jobs = self.main_page.search_by_link_text('Explore all jobs')
        explore_jobs.click()
        self.main_page.wait_title('Voicemod')
        assert self.main_page.driver.current_url == 'https://jobs.eu.lever.co/voicemod', "Unexpected jobs url"

    def test_faq(self):
        # Search for login faqs, the first should be "Login Issues: LOGIN ERROR"
        faq = self.main_page.search_by_title('FAQ')
        faq.click()
        # Select second tab
        self.driver.switch_to.window(self.driver.window_handles[1])
        # Search for Login word
        search_input = self.main_page.get_element_by_id('query')
        search_input.send_keys('Login')
        search_input.send_keys(Keys.RETURN)
        self.main_page.wait_title('Search results – Voicemod')
        results_list = self.main_page.get_element_by_class('search-results-list')
        results = results_list.find_elements(By.TAG_NAME, 'li')
        first_title = results[0].find_element(By.CLASS_NAME, 'search-result-title')
        assert first_title.text == 'Login Issues: LOGIN ERROR', 'Unexpected first result text'
        # Close second tab
        self.driver.close()

    def test_my_account(self):
        # Verify user email is right
        my_account = self.main_page.search_by_title('My Account')
        my_account.click()
        # Select second tab
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.main_page.discord_login()
        self.main_page.wait_title('Voicemod User Account')
        email_view = self.main_page.get_element_by_attribute_value('data-testid', 'view')
        email_view.click()
        email_input = self.main_page.get_element_visible_by_id('test')
        email = email_input.get_attribute("value")
        assert email == config['credentials']['email'], "Email unexpected"

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
