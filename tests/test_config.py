import unittest
from unittest.mock import patch, MagicMock
from services.scraper import Scraper
from services.spotify_operations.spotify_playlist_maker import SpotifyPlaylistMaker
from services.playlist_manager import PlaylistManager
from services.gpt_operations import GPTOperations
from config import Config
from model.song import Song
from model.songs import Songs

class TestConfig(unittest.TestCase):
    @patch('services.config.load_dotenv')
    @patch('services.config.os.getenv')
    def test_load_env_variables(self, mock_getenv, mock_load_dotenv):
        mock_getenv.side_effect = ['test_client_id', 'test_client_secret', 'test_redirect_uri', 'test_gpt_key']

        config = Config()

        self.assertEqual(config.get_client_id(), 'test_client_id')
        self.assertEqual(config.get_client_secret(), 'test_client_secret')
        self.assertEqual(config.get_redirect_uri(), 'test_redirect_uri')
        self.assertEqual(config.get_gpt_key(), 'test_gpt_key')