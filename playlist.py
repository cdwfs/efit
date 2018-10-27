import argparse
import efit
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", "-L", required=True, help="iTunes library file [.xml, .bz2, .pkl]")
    parser.add_argument("--all", "-a", action='store_true', required=False, help="export all playlists")
    parser.add_argument("playlists", nargs="*", help="playlist(s) to extract from library")
    args = parser.parse_args()

    lib_filename = args.library
    lib = efit.load_library_from_file(lib_filename)
    
    if args.all:
        playlist_names = lib.getPlaylistNames()
        for playlist_name in playlist_names:
            efit.export_playlist(lib, playlist_name, playlist_name+".m3u")
    elif len(args.playlists) == 0:
        playlist_names = lib.getPlaylistNames()
        for playlist_name in playlist_names:
            playlist = lib.getPlaylist(playlist_name)
            print("%s (%u tracks)" % (playlist_name, sum(map(efit.is_valid_song, playlist.tracks))))
    else:
        for playlist_name in args.playlists:
            if not playlist_name in lib.getPlaylistNames():
                print("Skipping '%s' (no such playlist in library)" % playlist_name)
                continue
            efit.export_playlist(lib, playlist_name, playlist_name+".m3u")

