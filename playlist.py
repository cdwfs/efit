import argparse
import efit
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", "-l", required=True, help="iTunes library file [.xml, .bz2, .pkl]")
    parser.add_argument("--playlist", "-p", required=True, help="name of playlist to extract from library")
    parser.add_argument("--output", "-o", required=True, help="output playlist file [.m3u8]")
    args = parser.parse_args()

    lib_filename = args.library
    playlist_name = args.playlist
    out_filename = args.output
    lib = efit.load_library_from_file(lib_filename)
    efit.export_playlist(lib, playlist_name, out_filename)
