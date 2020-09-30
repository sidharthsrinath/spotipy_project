from functions import *
import sys

arguments = sys.argv

if len(arguments) > 1:
    playlist_id = arguments[1] 
else:
    raise ValueError('Incorrect number of inputs')

playlist_name, tracks, user = get_playlist(playlist_id)
song_dict, head, names = song_information(playlist_name, tracks, user)

to_csv(song_dict,head,names)
