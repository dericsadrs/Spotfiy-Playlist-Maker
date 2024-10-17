from services.spotify_operations.spotify_playlist_maker import SpotifyPlaylistMaker
import logging
import json

class UserInfoViewer:
    def __init__(self):
        self.spotify = SpotifyPlaylistMaker()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def get_user_info(self):
        """
        Fetch and return the current user's Spotify information.
        """
        try:
            user_info = self.spotify.sp.current_user()
            self.logger.info(f"Successfully fetched user information")
            return user_info
        except Exception as e:
            self.logger.error(f"Failed to fetch user information: {str(e)}")
            return None

    def display_user_info(self, user_info):
        """
        Display the raw user information response.
        """
        if user_info:
            print("Raw User Information:")
            print(json.dumps(user_info, indent=2))
        else:
            print("No user information available.")

    def view_user_info(self):
        """
        Fetch and display the user's information.
        """
        user_info = self.get_user_info()
        self.display_user_info(user_info)
        return user_info