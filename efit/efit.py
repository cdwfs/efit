import pyItunes
import ntpath   # Assume paths in the Library are Windows-style
import os.path
import pickle

# List of absolute paths to directories where music are stored on the local system.
# If a song's can't be found at song.location, these directories will be searched
# in order.
music_roots = [
]

def load_library_from_file(filename):
    """Loads an iTunes library from either an XML file (exported from iTunes) or a pickled .pkl file."""
    base, ext = os.path.splitext(filename)
    if ext == ".xml":
        lib = pyItunes.Library(filename)
        if not os.path.exists(base + ".pkl"):
            print("Converting XML library to PKL...")
            save_library_as_pkl(lib, base + ".pkl")
            print("...done. Use %s.pkl for faster load times!" % base)
        return lib
    elif ext == ".pkl":
        lib_file = open(filename, "rb")
        lib = pickle.load(lib_file)
        lib_file.close()
        return lib
    else:
        raise Exception("Can not load libraries of type " + ext)
    return None

def save_library_as_pkl(library, filename):
    """Saves a library as a pickled .pkl file. PKL files are about 10x faster to load than XML."""
    pkl_file = open(filename, "wb")
    pickle.dump(library, pkl_file)
    pkl_file.close()

def is_valid_song(song):
    """Returns True if a song meets a variety of validity criteria (not a podcast, not a ringtone, etc."""
    return (True
            and song.location != None
            and song.genre not in ['Podcast', 'Voice Memo']
            and ntpath.splitext(song.location)[1].lower() not in ['.m4p', '.m4r']
            and "video" not in song.kind.lower()
            and ntpath.isabs(song.location) # many podcasts are only identifiable by their relative path in the Library
    )

def get_song_path(song):
    """Returns an absolute path to the specified song.

If the song can not be found at song.location, this function will attempt to location the song in
the directory(s) passed in the "roots" list. If it still can't be found anywhere, None is returned."""
    raw_path = song.location
    norm_path = ntpath.normpath(raw_path)
    if ntpath.isfile(norm_path):
        return norm_path
    # Can't find song in the listed location; look for it in the provided list of roots
    for root in music_roots:
        norm_root = os.path.normpath(root)
        rel_path = None
        full_path = norm_path
        while True:
            full_path, elem = ntpath.split(full_path)
            if len(elem) == 0:
                break # not found in this root
            if rel_path:
                rel_path = os.path.join(elem, rel_path)
            else:
                rel_path = elem
            candidate = os.path.join(norm_root, rel_path)
            if os.path.isfile(candidate):
                return candidate
    # Give up!
    return None

def export_playlist(lib, list_name, out_filename):
    """Exports a pre-existing playlist from the library in the standard .m3u8 format."""
    playlists = lib.getPlaylistNames()
    if list_name not in playlists:
        raise Exception("Unknown input playlist: '%s'" % list_name)
    playlist = lib.getPlaylist(list_name)

    _, ext = os.path.splitext(out_filename)

    if ext.lower() == '.m3u8':
        out_file = open(out_filename, "w", encoding="utf-8")
        out_file.write("#EXTM3U\n")
        file_num = 0
        for song in playlist.tracks:
            if not is_valid_song(song):
                print("Skipping %s: not a valid song" % song.name)
                continue
            song_path = get_song_path(song)
            if not song_path:
                print("Skipping %s: no such file" % song.location)
                continue
            file_num += 1
            out_file.write("%s\n" % song_path)
        out_file.close()
