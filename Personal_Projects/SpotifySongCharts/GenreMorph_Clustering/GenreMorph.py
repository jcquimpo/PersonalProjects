import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Setup Credentials
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_chart_data(playlist_id):
    # 2. Fetch the Playlist (e.g., Global Top 50)
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    
    rows = []
    
    for idx, item in enumerate(tracks):
        track = item['track']
        track_id = track['id']
        artist_id = track['artists'][0]['id']
        
        # 3. Fetch Artist Info for Genres
        # (Note: API changes in 2026 require individual fetches for some objects)
        artist_info = sp.artist(artist_id)
        genres = ", ".join(artist_info['genres'])
        
        # 4. Fetch Audio Statistics (The "ML" Data)
        audio_features = sp.audio_features(track_id)[0]
        
        # Combine into a dictionary
        song_data = {
            'position': idx + 1,
            'title': track['name'],
            'artist': track['artists'][0]['name'],
            'genres': genres,
            'popularity': track['popularity'],
            'duration_ms': track['duration_ms'],
            'danceability': audio_features['danceability'],
            'energy': audio_features['energy'],
            'valence': audio_features['valence'],
            'tempo': audio_features['tempo']
        }
        rows.append(song_data)
    
    return pd.DataFrame(rows)

# The ID for "Global Top 50" is 37i9dQZEVXbMDoJ6U7CjYI
df = get_chart_data('37i9dQZEVXbMDoJ6U7CjYI')

# 5. Export to CSV
df.to_csv('spotify_top_50_data.csv', index=False)
print("Data exported successfully to spotify_top_50_data.csv")