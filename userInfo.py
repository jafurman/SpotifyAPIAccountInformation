import spotipy
from spotipy.oauth2 import SpotifyOAuth


def checkTopArtists(amt):
    top_artists = sp.current_user_top_artists(limit=amt)
    print("\nYour Top Artists:")
    for idx, artist in enumerate(top_artists['items']):
        print(f"{idx + 1}. {artist['name']}")


def checkTopSongs(amt):
    top_tracks = sp.current_user_top_tracks(limit=amt)
    print("\nYour Top Tracks:")
    for idx, track in enumerate(top_tracks['items']):
        print(f"{idx + 1}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")


def checkLikedSongs():
    numOfSongsToDisplay = input("How many liked songs would you like to display?: ")
    numOfSongsToDisplay = int(numOfSongsToDisplay)

    limit = 25
    offset = 0

    counter = 0
    while True:
        if counter >= numOfSongsToDisplay:
            break
        liked_tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)

        if not liked_tracks['items']:
            break
        for idx, track in enumerate(liked_tracks['items']):
            counter += 1
            print(
                f"{idx + offset + 1}. {track['track']['name']} - {', '.join(artist['name'] for artist in track['track']['artists'])}")

        offset += limit


def checkLikedSongsPopularity():
    limit = 25
    offset = 0
    counter = 0
    popScores = []
    while True:
        liked_tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not liked_tracks['items']:
            break
        for idx, track in enumerate(liked_tracks['items']):
            counter += 1
            first_artist_name = track['track']['artists'][0]['name']
            artist_info = sp.search(q=f'artist:{first_artist_name}', type='artist')
            if artist_info['artists']['items']:
                artist_popularity = artist_info['artists']['items'][0]['popularity']
                popScores.append(int(artist_popularity))
                average = int(sum(popScores) / len(popScores))
                print(f"{average}: current calculated score average with {first_artist_name} : {artist_popularity} on "
                      f"song #{counter}.")
        offset += limit
    average = int(sum(popScores) / len(popScores))
    print(f"Your final average liked songs aritst popularity score is: {average}")
    if average > 80:
        print("Yikes, that's high...")


def removePopularityLevelFromLikedSongs(popLevel):
    if int(popLevel) <= 85:
        print("Bro you aint ready for that...")
        exit()
    limit = 25
    offset = 0
    counter = 0
    while True:
        liked_tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not liked_tracks['items']:
            break
        for idx, track in enumerate(liked_tracks['items']):
            counter += 1
            first_artist_name = track['track']['artists'][0]['name']
            artist_info = sp.search(q=f'artist:{first_artist_name}', type='artist')
            if artist_info['artists']['items']:
                artist_popularity = artist_info['artists']['items'][0]['popularity']
                print(
                    f"{idx + offset + 1}. {track['track']['name']} - {first_artist_name} (Popularity Score: {artist_popularity})"
                )
                if artist_popularity >= int(popLevel):
                    track_id = track['track']['id']
                    sp.current_user_saved_tracks_delete(tracks=[track_id])
                    print("\033[91mELIMINATED {} from liked songs because they're too popular for you.\033[0m".format(track['track']['name']))
            else:
                print(
                    f"{idx + offset + 1}. {track['track']['name']} - {first_artist_name} (Popularity: N/A)"
                )

        offset += limit


# _______________________ MAIN METHOD ___________________________

client_id = '6f61d716331b4159b2a347c9d43eede7'
client_secret = '4486acbeb22546e08348e511d138baba'
redirect_uri = 'http://localhost:8080/callback'

sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                        scope="user-library-read user-top-read")

sp = spotipy.Spotify(auth_manager=sp_oauth)

user_profile = sp.current_user()
display_name = user_profile.get('display_name', 'N/A')
email = user_profile.get('email', 'N/A')
followers = user_profile.get('followers', {}).get('total', 'N/A')

print(f"Display Name: {display_name}")
print(f"Email: {email}")
print(f"Followers Count: {followers}")

while True:
    print()
    # Avaliable Options
    print(f"[1]. See 'x' top artists (max 50)")
    print(f"[2]. See 'x' top songs (max 50)")
    print(f"[3]. See all liked songs")
    print(f"[4]. Display and average 'Popularity Score' in Liked Songs")
    print(f"[5]. Remove popular artist's songs from Liked Songs given 'x' popularity score")
    print(f"[Anything else]. Exit")

    answer = int(input("\nWhat would you like to do?: "))

    if answer == 1:
        amount = int(input("How many artists do you want to see?: "))
        checkTopArtists(amount)
    elif answer == 2:
        amount = int(input("How many songs do you want to see?: "))
        checkTopSongs(amount)
    elif answer == 3:
        checkLikedSongs()
    elif answer == 4:
        checkLikedSongsPopularity()
    elif answer == 5:
        popRemoveLevel = input("What is the popularity score you would like to remove?: ")
        removePopularityLevelFromLikedSongs(popRemoveLevel)
    else:
        exit()
