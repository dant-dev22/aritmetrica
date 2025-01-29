from fastapi import APIRouter, HTTPException
from app.services.spotify_service import SpotifyAPI
from app.services.database_service import DatabaseService
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

# Initialize SpotifyAPI
spotify_client = SpotifyAPI(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
)

# Initialize DatabaseService (No se usa directamente, ya que vamos a conectar directamente a la base de datos)
db_service = DatabaseService(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# configurar esto
db_service.connect()

router = APIRouter(prefix="/artists", tags=["artists"])

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        unix_socket="/var/run/mysqld/mysqld.sock"  # 🔹 Agrega esto
    )

@router.get("/{artist_id}")
def get_artist_info(artist_id: str):
    """
    Endpoint to fetch detailed information about an artist by their Spotify ID.
    """
    artist_data = spotify_client.get_artist(artist_id)
    if not artist_data:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist_data

@router.post("/update")
def update_artist(name: str, id: str, platform: str):
    """
    Endpoint to insert or update an artist in the database.

    Args:
        name (str): Name of the artist.
        id (str): ID of the artist on the specified platform.
        platform (str): Platform to which the ID belongs (e.g., "spotify", "youtube").

    Returns:
        dict: A message indicating success or failure.
    """
    # Validate platform
    valid_platforms = ["spotify", "youtube", "am", "itunes", "genius"]
    if platform not in valid_platforms:
        raise HTTPException(status_code=400, detail=f"Invalid platform. Valid platforms are: {valid_platforms}")

    # Establish a database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the artist already exists
        query = "SELECT id FROM artists WHERE name = %s"
        cursor.execute(query, (name,))
        artist = cursor.fetchone()

        if artist:
            # Update existing artist
            artist_id = artist[0]
            update_query = f"UPDATE artists SET {platform}_id = %s WHERE id = %s"
            cursor.execute(update_query, (id, artist_id))
            conn.commit()
            return {"message": f"Updated {platform}_id for artist '{name}'"}
        else:
            # Insert new artist
            insert_query = f"INSERT INTO artists (name, {platform}_id) VALUES (%s, %s)"
            cursor.execute(insert_query, (name, id))
            conn.commit()
            return {"message": f"Added new artist '{name}' with {platform}_id"}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()