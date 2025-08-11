# backend/handlers/spotify_handler.py

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser

# --- 1. Load Environment Variables ---
load_dotenv()

# --- 2. Initialize the Spotify Client ---
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# It's good practice to check if the environment variables were loaded correctly
if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    raise ValueError("SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET is not set in the .env file!")

try:
    # The Client Credentials flow is for server-to-server authentication.
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
    )
    sp_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    print("[Spotify Handler] Spotify client initialized successfully.")
except Exception as e:
    print(f"[Spotify Handler] Error initializing Spotify client: {e}")
    sp_client = None

# --- 3. Define Helper Data ---
# This map helps us create better search queries for moods.
MOOD_TO_GENRE_MAP = {
    'happy': ['happy', 'pop', 'dance', 'upbeat'],
    'sad': ['sad', 'acoustic', 'rainy day', 'chill'],
    'angry': ['angry', 'rock', 'metal', 'workout'],
    'relaxed': ['lo-fi', 'chill', 'ambient', 'focus'],
    'excited': ['party', 'edm', 'dance-pop', 'energetic'],
    'neutral': ['top hits', 'trending', 'pop'],
}

# --- 4. The Main Handler Function ---
def play_music_based_on_entities(entities: dict):
    """
    Builds a search query from entities, finds a playlist on Spotify,
    and opens it in a web browser.

    Args:
        entities (dict): A dictionary of extracted entities from the NLP module.
    """
    if not sp_client:
        print("  [Spotify Handler] Spotify client is not available. Cannot play music.")
        return "Sorry, I can't connect to Spotify right now."

    # --- Build the Search Query ---
    # We prioritize the search in a specific order: Artist > Language > Mood
    query_parts = []
    
    if entities.get("artist"):
        query_parts.append(entities["artist"])
        print(f"  [Spotify Handler] Prioritizing search for artist: {entities['artist']}")
    
    if entities.get("language"):
        query_parts.append(entities["language"])
        print(f"  [Spotify Handler] Adding language to search: {entities['language']}")

    # If no artist or language was found, fall back to mood
    if not query_parts and entities.get("mood"):
        mood = entities["mood"]
        # Get a list of search terms for the mood, or default to 'pop'
        genre_terms = MOOD_TO_GENRE_MAP.get(mood, ['pop'])
        query_parts.extend(genre_terms)
        print(f"  [Spotify Handler] No artist/language found. Searching by mood: {mood} (using terms: {genre_terms})")

    # If there are still no query parts, default to a generic search
    if not query_parts:
        print("  [Spotify Handler] No specific entities found. Defaulting to 'top hits'.")
        query_parts.append("top hits")

    # Join the parts to create the final search query
    search_query = " ".join(query_parts)
    print(f"  [Spotify Handler] Final Spotify search query: '{search_query}'")

    # --- Search Spotify and Open Playlist ---
    try:
        results = sp_client.search(q=search_query, type='playlist', limit=1)
        
        # --- FIX: Added a more robust check for the results object ---
        # First, check if results is not None, then check if it contains items.
        if results and results.get('playlists') and results['playlists'].get('items'):
            playlist = results['playlists']['items'][0]
            playlist_name = playlist['name']
            playlist_url = playlist['external_urls']['spotify']
            
            print(f"  [Spotify Handler] Found playlist: '{playlist_name}'")
            print(f"  [Spotify Handler] Opening URL: {playlist_url}")
            
            # Open the playlist URL in the default web browser
            webbrowser.open(playlist_url)
            
            return f"Playing '{playlist_name}' on Spotify for you."
        else:
            print(f"  [Spotify Handler] No playlists found for query: '{search_query}'")
            return f"Sorry, I couldn't find any playlists for '{search_query}'."

    except Exception as e:
        print(f"  [Spotify Handler] An error occurred during Spotify search: {e}")
        return "Sorry, an error occurred while searching on Spotify."

# --- Testing Block ---
if __name__ == "__main__":
    print("\n--- Testing Spotify Handler ---")

    # Test Case 1: Artist and Language
    print("\nTest Case 1: Artist and Language")
    test_entities_1 = {"artist": "Arijit Singh", "language": "hindi", "mood": "sad"}
    play_music_based_on_entities(test_entities_1)

    # Test Case 2: Just Mood
    print("\nTest Case 2: Just Mood")
    test_entities_2 = {"artist": None, "language": None, "mood": "happy"}
    play_music_based_on_entities(test_entities_2)

    # Test Case 3: No specific entities
    print("\nTest Case 3: No specific entities")
    test_entities_3 = {"artist": None, "language": None, "mood": "neutral"}
    play_music_based_on_entities(test_entities_3)
