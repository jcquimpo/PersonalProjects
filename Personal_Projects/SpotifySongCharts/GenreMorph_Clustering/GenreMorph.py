import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# 1. Setup Credentials
CLIENT_ID = ''
CLIENT_SECRET = ''

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def print_top_charts(playlist_id, count=25):
    # Fetch only the number of tracks requested (max 50 for this call)
    results = sp.playlist_items(playlist_id, limit=count)
    tracks = results['items']
    
    print(f"{'Rank':<5} | {'Artist':<20} | {'Track Name'}")
    print("-" * 60)
    
    for idx, item in enumerate(tracks):
        track = item['track']
        artist_name = track['artists'][0]['name']
        track_name = track['name']
        
        # Using f-strings to align the columns neatly in the terminal
        print(f"{idx + 1:<5} | {artist_name[:20]:<20} | {track_name}")

# Global Top 50 ID
CHART_ID = '37i9dQZEVXbMDoJ6U7CjYI'

# Change 'count' to any number between 1 and 50
print_top_charts(CHART_ID, count=25)