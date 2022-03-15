import unittest

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

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
        # Accept cookies
        accept_cookies_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "onetrust-accept-btn-handler")
            )
        )
        # Wait until cookies banner is not visible
        accept_cookies_button.click()
        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located(
                (By.ID, "onetrust-banner-sdk")
            )
        )
        # Load the main page
        self.main_page = page.MainPage(self.driver)

    # def test_voice_changer_for_pc(self):
    #     # Search Voice Changer for PC link
    #     changer_link = self.main_page.search_by_title('Voice Changer for PC')
    #     changer_link.click()
    #     # Delete previous files
    #     self.file_utils.delete_files(config['system']['downloads_folder'], 'VoicemodSetup*.exe')
    #     # Click to download button
    #     download_button = self.main_page.search_by_class('download-button')
    #     download_button.click()
    #     self.main_page.discord_login()
    #     self.main_page.download_wait(config['system']['downloads_folder'], 30, 1)
    #     file_exists = self.file_utils.file_exists(config['system']['downloads_folder'], 'VoicemodSetup*.exe')
    #     assert file_exists, "Error downloading Voicemod installer"
    #
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
        # Search free sounds
        free_sounds = self.main_page.search_by_title('Free Sounds')
        free_sounds.click()
        # Put a donkey in search field
        search_input = self.main_page.get_element_by_id('search-form')
        search_input.click()
        search_input.send_keys('cow')
        search_input.send_keys(Keys.RETURN)
        # Wait until search list appears
        self.main_page.get_element_by_attribute_value('label', 'filters')
        play_first_cow = self.main_page.get_element_by_attribute_value('aria-label', 'Play')
        assert play_first_cow, "almost a play button exists"
        play_first_cow.click()
        pause_first_cow = self.main_page.get_element_by_attribute_value('aria-label', 'Pause')
        assert play_first_cow, "pause button exists"
        pause_first_cow.click()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
