import unittest
from unittest.mock import patch, MagicMock
from services.scraper import Scraper
from services.spotify_operations.spotify_playlist_maker import SpotifyPlaylistMaker
from services.playlist_manager import PlaylistManager
from services.gpt_operations import GPTOperations
from config import Config
from model.song import Song
from model.songs import Songs

class TestPlaylistManager(unittest.TestCase):
    @patch('services.playlist_manager.Scraper')
    @patch('services.playlist_manager.SpotifyPlaylistMaker')
    def test_create_playlist(self, mock_spotify_maker, mock_scraper):
        # Mock the scraper
        mock_scraper.return_value.get_latest_chart.return_value = Songs([Song("Test Song", "Test Artist")])

        # Mock the Spotify maker
        mock_spotify_maker.return_value.sp.current_user.return_value = {'id': 'test_user'}
        mock_spotify_maker.return_value.create_playlist.return_value = 'test_playlist_id'
        mock_spotify_maker.return_value.search_song.return_value = 'spotify:track:test_uri'

        playlist_manager = PlaylistManager()
        result = playlist_manager.create_playlist("billboard_hot_100")

        self.assertEqual(result['status'], 'success')
        self.assertIn('Created playlist with', result['message'])