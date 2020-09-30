import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def get_artist(name):
    results = spotify.search(q='artist:' + name, type='artist')

    dict = results['artists']['items'][0]


    for key in dict:
        print(f'\n{key}: {dict[key]} \n')

def get_song(name):
    results = spotify.search(q = 'song: ' + name, type='song')

    print(results)


def get_album(id):
    album = spotify.album(id)
    
    artist_name = album['artists'][0]['name']
    genre = album['genres']
    album_name = album['name']

    print(album_name)
    print(artist_name)
    
    # for key in album:
    #     print(key)

    #return album_name, artist_name, artist_id

def get_playlist(id):
    playlist = spotify.playlist(id)

    # for key in playlist:
    #     print(key)

    playlist_name = playlist['name']
    tracks = playlist['tracks']

    # for key in tracks:
    #     print(key)

    with open('tracks.txt', 'w') as tracktext:
        tracktext.write(f'Playlist: {playlist_name} \n')
        for x,y in enumerate((tracks['items'])):
            thistrack = y['track']
            thisname = thistrack['name']
            artist_name = thistrack['artists'][0]['name']
            tracktext.write(f'{x+1}. {thisname} , {artist_name} \n')

    # trackdict = tracks['items'][0]['track']['available_markets']
    # print(trackdict)
    # for key in trackdict:
    #    print(key)

            


playlist_id = 'spotify:playlist:6q3k05ivbimSgEWvWnSStd'
playlist = get_playlist(playlist_id)