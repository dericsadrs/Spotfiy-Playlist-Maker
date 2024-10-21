import unittest
from unittest.mock import patch, MagicMock
from services.scraper import Scraper
from services.spotify_operations.spotify_playlist_maker import SpotifyPlaylistMaker
from services.playlist_manager import PlaylistManager
from services.gpt_operations import GPTOperations
from config import Config
from model.song import Song
from model.songs import Songs

class TestSpotifyPlaylistMaker(unittest.TestCase):
    @patch('services.spotify_operations.spotify_playlist_maker.spotipy.Spotify')
    def test_create_playlist(self, mock_spotify):
        mock_spotify.return_value.user_playlist_create.return_value = {'id': 'test_playlist_id'}
        
        playlist_maker = SpotifyPlaylistMaker()
        playlist_id = playlist_maker.create_playlist('test_user', 'Test Playlist', 'Test Description')

        self.assertEqual(playlist_id, 'test_playlist_id')
        mock_spotify.return_value.user_playlist_create.assert_called_once_with(
            user='test_user', name='Test Playlist', public=True, description='Test Description'
        )