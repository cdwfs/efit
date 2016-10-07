import pyItunes
import os.path
import sys

def export_playlist(lib, list_name, pls_filename):
    playlists = lib.getPlaylistNames()
    if list_name not in playlists:
        print("Unknown playlist '%s'. Valid playlist names:" % list_name)
        for pl in playlists:
            print(pl)
        sys.exit(1)
    playlist = lib.getPlaylist(list_name)

    out_file = open(pls_filename, "w", encoding="utf-8")
    out_file.write("#EXTM3U\n")
    file_num = 0
    for song in playlist.tracks:
        file_num += 1
        out_file.write("%s\n" % (os.path.normpath(song.location)))
    out_file.close()

if __name__ == "__main__":
    lib = pyItunes.Library(sys.argv[1])
    export_playlist(lib, sys.argv[2], sys.argv[3])
