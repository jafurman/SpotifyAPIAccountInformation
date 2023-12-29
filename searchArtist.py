import requests

# Spotify application credentials
client_id = '6f61d716331b4159b2a347c9d43eede7'
client_secret = '4486acbeb22546e08348e511d138baba'

# Step 1: Obtain an access token using the Client Credentials flow
token_url = 'https://accounts.spotify.com/api/token'
data = {
    'grant_type': 'client_credentials',
}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
auth = (client_id, client_secret)

response = requests.post(token_url, data=data, headers=headers, auth=auth)

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data.get('access_token')

    if access_token:
        while True:
            artist_name = input("Enter the artist's name: ")
            search_url = f'https://api.spotify.com/v1/search'
            params = {
                'q': artist_name,
                'type': 'artist',
            }
            headers = {
                'Authorization': f'Bearer {access_token}',
            }

            search_response = requests.get(search_url, params=params, headers=headers)

            if search_response.status_code == 200:
                search_data = search_response.json()
                artists = search_data.get('artists', {}).get('items', [])

                if artists:
                    # Assuming you want the first artist in the search results
                    artist = artists[0]
                    artist_name = artist['name']
                    print(f'Artist Name: {artist_name}')
                    artist_popularity = artist.get("popularity", 'N/A')
                    print(f"Popularity Score: {artist_popularity}")

                    artist_genres = artist.get('genres', [])
                    print(f"Genres: {', '.join(artist_genres)}")

                    artist_followers = artist.get('followers', {}).get('total', 'N/A')
                    print(f"Follower Count: {artist_followers}")

                else:
                    print("No artist found for the given name.")
            else:
                print(f"Error retrieving artist data: {search_response.status_code} - {search_response.text}")

            print()

            check = artist_name.lower()
            if check == "no more":
                break
    else:
        print("Access token not found in the response.")
else:
    print(f"Error obtaining access token: {response.status_code} - {response.text}")
