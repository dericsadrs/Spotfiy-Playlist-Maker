import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config
import logging

class SpotifyAuth:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.config = Config()
        self.sp = None
        self.authenticate()

    def authenticate(self):
        """
        Authenticate with Spotify using OAuth 2.0
        """
        try:
            self.logger.info("Attempting to authenticate with Spotify...")
            self.sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=self.config.get_client_id(),
                    client_secret=self.config.get_client_secret(),
                    redirect_uri=self.config.get_redirect_uri(),
                    scope='playlist-modify-public user-read-private user-read-email'
                )
            )
            self.logger.info("Successfully authenticated with Spotify")
        except Exception as e:
            self.logger.error(f"Failed to authenticate with Spotify: {str(e)}")
            raise

    def get_spotify_client(self):
        """
        Return the authenticated Spotify client
        """
        if not self.sp:
            self.logger.warning("Spotify client not initialized. Attempting to authenticate...")
            self.authenticate()
        return self.sp

    def refresh_token_if_expired(self):
        """
        Check if the current token is expired and refresh if necessary
        """
        try:
            if self.sp.auth_manager.is_token_expired(self.sp.auth_manager.get_cached_token()):
                self.logger.info("Token expired. Refreshing...")
                self.sp.auth_manager.refresh_access_token(self.sp.auth_manager.get_cached_token()['refresh_token'])
                self.logger.info("Token refreshed successfully")
            else:
                self.logger.info("Token is still valid")
        except Exception as e:
            self.logger.error(f"Error checking/refreshing token: {str(e)}")
            raise