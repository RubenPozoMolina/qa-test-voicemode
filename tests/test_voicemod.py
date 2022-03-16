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

    # def test_soundboard(self):
    #     # Search Soundboard link
    #     soundboard_link = self.main_page.search_by_title('Soundboard')
    #     soundboard_link.click()
    #     # Delete previous files
    #     self.file_utils.delete_files(config['system']['downloads_folder'], 'VoicemodSetup*.exe')
    #     # Click to download button
    #     download_button = self.main_page.search_by_class('download-button')
    #     download_button.click()
    #     self.main_page.discord_login()
    #     self.main_page.download_wait(config['system']['downloads_folder'], 30, 1)
    #     file_exists = self.file_utils.file_exists(config['system']['downloads_folder'], 'VoicemodSetup*.exe')
    #     assert file_exists, "Error downloading Soundboard installer"
    #
    # def test_voicelab(self):
    #     # Search soundboard link
    #     soundboard_link = self.main_page.search_by_title('Voicelab')
    #     soundboard_link.click()
    #     # Delete previous files
    #     self.file_utils.delete_files(config['system']['downloads_folder'], 'VoicemodSetup*.exe')
    #     # Click to download button
    #     download_button = self.main_page.search_by_class('download-button')
    #     download_button.click()
    #     self.main_page.discord_login()
    #     self.main_page.download_wait(config['system']['downloads_folder'], 30, 1)
    #     file_exists = self.file_utils.file_exists(config['system']['downloads_folder'], 'VoicemodSetup*.exe')
    #     assert file_exists, "Error downloading Voicelab installer"

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

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
