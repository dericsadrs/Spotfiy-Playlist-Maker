import pytest
from unittest.mock import Mock, patch, MagicMock
from services.playlist_manager import PlaylistManager

class TestPlaylistManager:
    """Test suite for PlaylistManager service"""
    
    @pytest.fixture
    def mock_spotify_maker(self):
        with patch('services.spotify_operations.spotify_playlist_maker.SpotifyPlaylistMaker') as mock:
            mock.return_value.sp.current_user.return_value = {'id': 'test_user'}
            mock.return_value.create_playlist.return_value = 'test_playlist_id'
            yield mock
            
    @pytest.fixture
    def playlist_manager(self, mock_spotify_maker):
        return PlaylistManager()
        
    def test_create_playlist_success(self, playlist_manager, mock_spotify_maker):
        """Test successful playlist creation"""
        with patch('services.scraper.Scraper') as mock_scraper:
            mock_scraper.return_value.get_latest_chart.return_value = Songs([
                Song("Test Song", "Test Artist")
            ])
            
            mock_spotify_maker.return_value.search_song.return_value = "spotify:track:test123"
            
            result = playlist_manager.create_playlist("billboard_hot_100")
            assert result["status"] == "success"
            assert "Created playlist" in result["message"]
            
    def test_create_playlist_no_songs(self, playlist_manager):
        """Test playlist creation with no songs found"""
        with patch('services.scraper.Scraper') as mock_scraper:
            mock_scraper.return_value.get_latest_chart.return_value = Songs([])
            
            result = playlist_manager.create_playlist("billboard_hot_100")
            assert result["status"] == "error"
            assert "No songs found" in result["message"]
            
    def test_create_playlist_spotify_error(self, playlist_manager, mock_spotify_maker):
        """Test handling of Spotify API errors"""
        with patch('services.scraper.Scraper') as mock_scraper:
            mock_scraper.return_value.get_latest_chart.return_value = Songs([
                Song("Test Song", "Test Artist")
            ])
            
            # Simulate Spotify API error
            mock_spotify_maker.return_value.create_playlist.side_effect = Exception("Spotify API Error")
            
            result = playlist_manager.create_playlist("billboard_hot_100")
            assert result["status"] == "error"
            assert "error occurred" in result["message"].lower()