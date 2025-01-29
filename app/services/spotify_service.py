import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyAPI:
    """
    A class to interact with the Spotify API.
    Handles authentication and provides methods to fetch artist information.
    """
    def __init__(self, client_id: str, client_secret: str):
        """
        Initializes the SpotifyAPI class with client credentials.

        Args:
            client_id (str): Spotify API client ID.
            client_secret (str): Spotify API client secret.
        """
        self.client = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
        )

    def search_artist(self, artist_name: str, limit: int = 5):
        """
        Searches for artists by name and returns a list of matching artists.

        Args:
            artist_name (str): Name of the artist to search for.
            limit (int): Maximum number of results to return. Default is 5.

        Returns:
            list: A list of dictionaries containing artist information.
                  Returns None if no results are found.
        """
        result = self.client.search(q=f'artist:{artist_name}', type='artist', limit=limit)
        artists = result['artists']['items']

        if not artists:
            return None

        artists_result = []
        for artist in artists:
            artists_result.append({
                'name': artist['name'],
                'genres': artist['genres'],
                'popularity': artist['popularity'],
                'followers': artist['followers']['total'],
                'url': artist['external_urls']['spotify']
            })

        return artists_result

    def get_artist(self, artist_id: str):
        """
        Fetches detailed information about a specific artist by their Spotify ID.

        Args:
            artist_id (str): Spotify ID of the artist.

        Returns:
            dict: A dictionary containing detailed information about the artist.
        """
        artist_data = self.client.artist(artist_id=artist_id)
        return artist_data