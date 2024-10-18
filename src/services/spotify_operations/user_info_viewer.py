from services.spotify_operations.spotify_auth import SpotifyAuth
import logging
import json

class UserInfoViewer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.auth = SpotifyAuth()
        self.sp = self.auth.get_spotify_client()

    def get_user_info(self):
        """
        Fetch and return the current user's Spotify information.
        """
        try:
            self.auth.refresh_token_if_expired()
            user_info = self.sp.current_user()
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
            self.logger.info("Displaying raw user information")
            print("Raw User Information:")
            print(json.dumps(user_info, indent=2))
        else:
            self.logger.warning("No user information available to display")
            print("No user information available.")

    def view_user_info(self):
        """
        Fetch and display the user's information.
        """
        self.logger.info("Fetching and displaying user information")
        user_info = self.get_user_info()
        self.display_user_info(user_info)
        return user_info