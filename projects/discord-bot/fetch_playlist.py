from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint
import sys

def fetch() :
    client_id = "YOUR_CLIENT_ID"    #YOUR_CLIENT_ID
    client_secret = "YOUR_CLIENT_SECRET"    #YOUR_CLIENT_SECRET

    import dbQuery as query
    lz_uri = query.RETRIEVE()
    if lz_uri == 'N/A' :
        print("Exiting..")
        sys.exit()

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    results = sp.artist_top_tracks(lz_uri)

    playlist = list()

    # get top 10 tracks
    for track in results['tracks'][:10]:
        # print('track    : ' + track['name'])
        # print('audio    : ' + track['preview_url'])
        # print('cover art: ' + track['album']['images'][0]['url'])
        # print()
        playlist.append(track['name'])
    
    return playlist