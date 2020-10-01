from functions import *
from analysis import*
import sys
import os

arguments = sys.argv

if len(arguments) > 1:
    playlist_id = arguments[1] 
else:
    raise ValueError('Incorrect number of inputs')

#data extraction: Step 1
# playlist_name, tracks, user = get_playlist(playlist_id)
# song_dict, head, names = song_information(playlist_name, tracks, user)
# to_csv(song_dict,head,names)
# data_dir = os.path.join(os.getcwd(), names[1],names[0]+'.csv')

#data prep
data_dir = '/Users/sidharthsrinath/Documents/VSCode/Projects/spotipy/SidharthSrinath/other.csv'
read_df(data_dir)
