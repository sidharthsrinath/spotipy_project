from functions import *
import sys

arguments = sys.argv

if len(arguments) > 1:
    playlist_id = arguments[1] 
else:
    raise ValueError('Incorrect number of inputs')

#'spotify:playlist:6q3k05ivbimSgEWvWnSStd'

playlist_name, tracks, user = get_playlist(playlist_id)
get_songs(playlist_name, tracks, user)