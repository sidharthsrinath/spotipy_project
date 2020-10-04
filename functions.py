import spotipy
from spotipy import util
import sys
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
import pandas as pd

scope = 'playlist-modify-private'

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def song_information(playlistname, playlistsongids, playlistuser): #evaluate songs from a list of songs
    #complete for now

    username = playlistuser['display_name'].replace(' ', '')
    headers = []
    songdicts = []

    
    for x,y in enumerate(playlistsongids):
        #song id
        songid = y
        songdata = get_song_data(songid)
        songfeatures = get_song_features(songid)
        songdict = {**songdata, **songfeatures}
        songdicts.append(songdict)
        print(f'Finished {songdata["song_name"]}')
    
    for key in songdicts[0]:
        headers.append(key)

    print(f'Got all info for all songs')
    return songdicts, headers, [playlistname,username]
            
def get_song_genre(artist_id): #getting the genre of a song based on artist id
    #complete for right now
    try:
        artist = spotify.artist(artist_id)#search for artist based on id to get exact result
        genres = artist['genres']
        genrestr = '('
        for a in genres:
            genrestr += (a + ';')
        genrestr = genrestr[:-1]
        genrestr += ')'
        return genrestr
    except(AttributeError):
        pass

def get_song_features(songid): #getting the data of a song (dancability, loudness, etc)
    
    features = spotify.audio_features(songid)
    features = features[0]

    
    song_features = {
    'danceability' : features['danceability'],
    'energy' : features['energy'],
    'key' : features['key'],
    'loudness' : features['loudness'],
    'mode' : features['mode'],
    'speechiness' : features['speechiness'],
    'acousticness' : features['acousticness'],
    'instrumentalness' : features['instrumentalness'],
    'liveness' : features['liveness'],
    'valence' : features['valence'],
    'tempo' : features['tempo'],
    'time_signature' : features['time_signature']
    }

    # print('Recieved Song Data for {}'.format(songid))

    return song_features

def get_song_data(songid):
    data = spotify.track(songid)
    # print(f'Song: {songid} was unable to be found')

    song_data = {
    'song_name' : data['name'],
    'album_name': data['album']['name'],
    'artist_name' : data['artists'][0]['name'],
    'artist_id' : data['artists'][0]['id'],
    'song_release_date' : data['album']['release_date'],
    'song_length' : data['duration_ms'],
    'song_popularity' : data['popularity'],
    'song_id' : songid,
    }
    # song_data['song_genres'] = get_song_genre(song_data['artist_id'])

    print('Recieved Song Data for {}'.format(songid))


    return song_data

def get_playlist(id): #extract and distribute info from a playlist to helper functions
    #complete for right now

    playlist = spotify.playlist(id) #returns a dict

    playlist_name = playlist['name']#playlist name
    user = playlist['owner']#user who owns the playlist
    tracks = playlist['tracks'] #only the first 100 tracks -- is a dict

    all_tracks = tracks['items']
    while tracks['next']: # getting the rest of the tracks from the playlist
        tracks = spotify.next(tracks)
        all_tracks.extend(tracks['items'])
    
    #creating a list of all the songs in the playlist
    local_songs = []
    songs = [x['track'] for x in all_tracks]
    songids = []

    for x,y in enumerate(songs):
        if not y['is_local']:
            songids.append(y['id'])
        else:
            local_songs.append((y['name'],y['id']))

    print(f'Revieved Playlist Info for playlist {id}')
    return playlist_name, songids, user , local_songs 

def make_playlists(df, username):

    scope = 'playlist-modify-private'
    token= util.prompt_for_user_token(username,scope) 
    sp_playlist = spotipy.Spotify(auth=token)

    playlist_1 = df[df['KMeans']==0] #low energy
    playlist_2 = df[df['KMeans']==1] #high energy

    id0 = list(playlist_1['song_id']) #low energy
    id1 = list(playlist_2['song_id']) #high energy

    high_energy = sp_playlist.user_playlist_create(user=username,
                                           name="Radiohead :)")
    low_energy = sp_playlist.user_playlist_create(user=username,
                                            name="Radiohead :(")

    spotify.user_playlist_add_tracks(user = username,playlist_id= low_energy['id'],tracks = id0)
    spotify.user_playlist_add_tracks(user = username,playlist_id= high_energy['id'],tracks = id1)


def to_csv(dictionaries, headers,names):
    #∆ - option+J - special delimiter
    playlist_name = names[0]
    username = names[1]
    try:
        os.mkdir(username)
    except(FileExistsError):
        pass
    filename = username+'/'+playlist_name+'.csv'
    print(f'Writing file {filename}')
    with open(filename, 'w') as data:
        for x in headers:
            data.write(x+'∆')
        data.write('\n')

        for dict in dictionaries:
            for key in dict:
                data.write(f'{dict[key]} ∆')
            data.write('\n')
    print(f'{filename} has been written')

