from spotify_auth import SpotifyAuth
import logging

class SpotifyPlaylistMaker:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.auth = SpotifyAuth()
        self.sp = self.auth.get_spotify_client()

    def create_playlist(self, user_id: str, playlist_name: str, description: str) -> str:
        """
        Create a Spotify playlist and return its ID.
        """
        try:
            self.auth.refresh_token_if_expired()
            playlist = self.sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=description)
            self.logger.info(f"Created playlist '{playlist_name}' with ID {playlist['id']}")
            return playlist['id']
        except Exception as e:
            self.logger.error(f"Failed to create playlist '{playlist_name}': {str(e)}")
            raise

    def add_tracks_to_playlist(self, playlist_id: str, track_uris: list):
        """
        Add a list of tracks Spotify URIs to the playlist.
        """
        try:
            self.auth.refresh_token_if_expired()
            self.sp.playlist_add_items(playlist_id, track_uris)
            self.logger.info(f"Added {len(track_uris)} tracks to the playlist with ID {playlist_id}.")
        except Exception as e:
            self.logger.error(f"Failed to add tracks to playlist {playlist_id}: {str(e)}")
            raise

    def search_song(self, artist: str, track: str) -> str:
        """
        Search Spotify for a track by its artist and title.
        Returns the Spotify URI for the first match found.
        """
        try:
            self.auth.refresh_token_if_expired()
            query = f"artist:{artist} track:{track}"
            result = self.sp.search(q=query, type='track', limit=1)
            if result['tracks']['items']:
                self.logger.info(f"Found match for '{track}' by {artist}")
                return result['tracks']['items'][0]['uri']
            self.logger.warning(f"No match found for {artist} - {track}")
            return None
        except Exception as e:
            self.logger.error(f"Error searching for track '{track}' by artist '{artist}': {str(e)}")
            raise