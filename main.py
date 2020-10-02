from functions import *
from analysis import*
import sys
import os

arguments = sys.argv

if len(arguments) > 1:
    playlist_id = arguments[1] 
    print(f'Recieved Playlist ID: {playlist_id}')
else:
    raise ValueError('Incorrect number of inputs')

# #data extraction: Step 1
playlist_name, tracks, user, local_tracks = get_playlist(playlist_id)
song_dict, head, names = song_information(playlist_name, tracks, user)
to_csv(song_dict,head,names)
data_dir = os.path.join(os.getcwd(), names[1],names[0]+'.csv')

#data prep: Step 2
df = read_df(data_dir)
print(df.head())

