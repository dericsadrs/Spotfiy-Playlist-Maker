import unittest
from unittest.mock import patch, MagicMock
from services.scraper import Scraper
from services.spotify_operations.spotify_playlist_maker import SpotifyPlaylistMaker
from services.playlist_manager import PlaylistManager
from services.gpt_operations import GPTOperations
from config import Config
from model.song import Song
from model.songs import Songs

class TestScraper(unittest.TestCase):
    @patch('services.scraper.sync_playwright')
    def test_get_latest_chart(self, mock_playwright):
        # Mock the playwright and page objects
        mock_page = MagicMock()
        mock_browser = MagicMock()
        mock_browser.new_page.return_value = mock_page
        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser

        # Mock the song elements
        mock_song_element = MagicMock()
        mock_song_element.query_selector().inner_text.return_value = "Test Song"
        mock_page.query_selector_all.return_value = [mock_song_element]

        scraper = Scraper(headless=True, chart_type="billboard_hot_100")
        result = scraper.get_latest_chart()

        self.assertIsInstance(result, Songs)
        self.assertEqual(len(result.songs), 1)
        self.assertEqual(result.songs[0].title, "Test Song")