import argparse
import efit
import os.path
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", "-L", required=True, help="iTunes library file [.xml, .bz2, .pkl]")
    args = parser.parse_args()

    lib_filename = args.library
    lib = efit.load_library_from_file(lib_filename)

    for id, song in lib.songs.items():
        if song.location != None and os.path.exists(song.location) == False:
            print("Song {s} at location {loc} does not exist".format(s=song.name, loc=song.location_escaped))
