import efit
import sys

if __name__ == "__main__":
    lib_filename = sys.argv[1]
    playlist_name = sys.argv[2]
    out_filename = sys.argv[3]
    lib = efit.load_library_from_file(lib_filename)
    efit.export_playlist(lib, playlist_name, out_filename)
