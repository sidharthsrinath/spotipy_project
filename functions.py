import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def get_songs(playlistname, playlistsongs, playlistuser): #evaluate songs from a list of songs
    #complete for now

    filename = 'tracks_'+playlistname+'.txt'
    username = playlistuser['display_name']

    playlist_song_names = []
    playlist_song_album_names = []
    playlist_song_artist_names = []
    playlist_song_ids = []
    playlist_song_genres = []


    with open(filename, 'w') as tracktext:
        tracktext.write(f'Playlist: {playlistname} \n')
        tracktext.write(f'Owner: {username} \n')
        for x,y in enumerate(playlistsongs):
            #song id
            songid = y['id']
            playlist_song_ids.append(songid)
            #song name
            songname = y['name']
            playlist_song_names.append(songname)
            #songs album name
            albumname = y['album']['name']
            playlist_song_album_names.append(albumname)
            #songs artists name
            artistname = y['artists'][0]['name']
            playlist_song_artist_names.append(artistname)
            #songs artist's id
            artistid = y['artists'][0]['id']
            #song's genre
            songgenres = get_song_genre(artistid)
            playlist_song_genres.append(songgenres)
            #f'{x+1}. {song name}, {album name}, {artist name} \n'
            tracktext.write(f'{x+1}. {songname}, {albumname}, {artistname}, {songgenres} \n')
   
    song_info = list(zip(playlist_song_names, playlist_song_album_names, 
        playlist_song_artist_names, playlist_song_ids,playlist_song_genres))
    
    return song_info

def get_song_genre(artist_id):
    try:
        artist = spotify.artist(artist_id)#search for artist based on id to get exact result
        return artist['genres']
    except(AttributeError):
        pass

def get_playlist(id): #extract and distribute info from a playlist to helper functions
    #complete for right now

    
    playlist = spotify.playlist(id)
    
    playlist_name = playlist['name']#playlist name
    user = playlist['owner']#user who owns the playlist
    tracks = playlist['tracks'] #only the first 100 tracks

    all_tracks = tracks['items']
    while tracks['next']: # getting the rest of the tracks from the playlist
        tracks = spotify.next(tracks)
        all_tracks.extend(tracks['items'])
    
    #creating a list of all the songs in the playlist
    songs = [x['track'] for x in all_tracks]

    return playlist_name, songs, user


