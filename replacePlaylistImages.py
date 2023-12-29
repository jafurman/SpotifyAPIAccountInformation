import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

client_id = 'YOUR KEY'
client_secret = 'YOUR KEY'
redirect_uri = 'http://localhost:8080/callback'

scope = 'user-read-private user-read-email user-library-read user-library-modify playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-follow-read user-follow-modify user-top-read ugc-image-upload'
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
)

sp = spotipy.Spotify(auth_manager=sp_oauth)

# Get user's playlists
playlists = sp.current_user_playlists()

playlist_ids = []
for playlist in playlists['items']:
    print(f"Playlist Name: {playlist['name']}")
    print(f"Playlist ID: {playlist['id']}")
    print(f"Playlist Image: {playlist['images'][0]['url']}" if playlist['images'] else "No Image")
    print("\n")
    playlist_ids.append(playlist['id'])


def get_cat_image():
    cat_api_url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(cat_api_url)
    cat_data = response.json()
    cat_image_url = cat_data[0]['url']
    return cat_image_url


cat_image = get_cat_image()


# Function to upload cover image to a playlist
def upload_cover_image(playlist_id, image_url):
    headers = {
        "Authorization": f"Bearer {sp_oauth.get_cached_token()['access_token']}",
        "Content-Type": "application/json"
    }

    image_data = requests.get(image_url).content

    data = {
        "image": image_data
    }

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/images"
    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"Playlist {playlist_id} cover image updated successfully!")
    else:
        print(
            f"Error updating cover image for playlist {playlist_id}. Status code: {response.status_code}, Response: {response.text}")


playlist_id_to_update = "2Jk2YNlTCQ7kw07M9bSIup"
upload_cover_image(playlist_id_to_update, cat_image)
