#!/usr/bin/env python
from gmusicapi import Mobileclient
import sys

REMOVE_FLAG = True
def find_and_remove_dups(api, tracks):
    track_set = set()
    delete_count = 0

    for track in tracks:
        trackId = track['trackId']
        entryId = track['id']
        if trackId in track_set:
            print("    found duplicate with trackId: " + trackId + ", deleting")
            if REMOVE_FLAG:
                try:
                    api.remove_entries_from_playlist(entryId)
                except Exception as e:
                    print(e)
            delete_count += 1
        else:
            track_set.add(trackId)
    if delete_count > 0:
        print("Deleted {s} in playlist".format(s=str(delete_count)))
    return delete_count
            

if len(sys.argv) != 1:
    print("USAGE:")
    print("./delete_dups_from_playlists.py")
    print("\n")
    print("     Will delete all duplicate songs within each playlist")
    exit(0)

api = Mobileclient()
username = "emailadress"
password = "your password" # or app-specific password for 2 Factor Authentication
logged_in = api.login(username, password,  Mobileclient.FROM_MAC_ADDRESS)


if logged_in:
    print("Successfully logged in. Finding duplicates in playlists")
    playlists = api.get_all_user_playlist_contents()

    for playlist in playlists:
        print("Checking duplicates from " + playlist['name'] + "...")
        tracks = playlist['tracks']
        find_and_remove_dups(api, tracks)
    
    if REMOVE_FLAG is False:
        print("REMOVE_FLAG is False")

else:
    print("Error: not logged in")

