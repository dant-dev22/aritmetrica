from fastapi import APIRouter, HTTPException
from app.services.spotify_service import SpotifyAPI
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize SpotifyAPI
spotify_client = SpotifyAPI(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
)

router = APIRouter(prefix="/artists", tags=["artists"])

@router.get("/{artist_id}")
def get_artist_info(artist_id: str):
    """
    Endpoint to fetch detailed information about an artist by their Spotify ID.
    """
    artist_data = spotify_client.get_artist(artist_id)
    if not artist_data:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist_data