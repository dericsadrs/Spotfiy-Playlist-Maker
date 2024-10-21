import unittest
from unittest.mock import patch, MagicMock
from services.scraper import Scraper
from services.spotify_operations.spotify_playlist_maker import SpotifyPlaylistMaker
from services.playlist_manager import PlaylistManager
from services.gpt_operations import GPTOperations
from config import Config
from model.song import Song
from model.songs import Songs

class TestGPTOperations(unittest.TestCase):
    @patch('services.gpt_operations.SpotifyPlaylistMaker')
    def test_fetch_songs(self, mock_spotify_maker):
        mock_spotify_maker.return_value.sp.search.return_value = {
            'tracks': {'items': [{'name': 'Test Song'}]}
        }

        gpt_ops = GPTOperations()
        result = gpt_ops.fetch_songs("Give me songs by Test Artist")

        self.assertIn("Test Song", result)
        self.assertIn("Test Artist", result)