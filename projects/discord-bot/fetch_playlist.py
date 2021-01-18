from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint


client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

lz_uri = 'spotify:artist:6VuMaDnrHyPL1p4EHjYLi7' # Charlie Puth

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

results = sp.artist_top_tracks(lz_uri)

# get top 10 tracks
for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()

#출처 : https://jisun-rea.tistory.com/entry/Spotify-Web-API-%ED%8A%B9%EC%A0%95-artist%EC%9D%98-top-10-playlist-%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0-%ED%8C%8C%EC%9D%B4%EC%8D%AC-spotipy-%EB%9D%BC%EC%9D%B4%EB%B8%8C%EB%9F%AC%EB%A6%AC-%EC%82%AC%EC%9A%A9