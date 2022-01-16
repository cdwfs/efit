import efit

import mutagen
import mutagen.id3
import mutagen.mp4
import os.path
import sys

def get_album_cover_size(song_path):
    "Assumes song_path is a valid file."
    _,ext = os.path.splitext(song_path)
    if ext.lower() == '.mp3':
        try:
            id3 = mutagen.id3.ID3(song_path)
            apics = id3.getall("APIC:cover")
            if len(apics) == 0:
                return 0 # no covers stored
            elif len(apics) > 1:
                print(f"\r{' '*32}\r{song.name}: has multiple cover images")
            return len(apics[0].data)
        except mutagen.id3._util.ID3NoHeaderError as e: return 0
        except IndexError as e: return 0
    elif ext.lower() == '.m4a':
        mp4_file = mutagen.mp4.MP4(song_path)
        if mp4_file.tags == None:
            return 0
        tags = mp4_file.tags
        try: covers = tags['covr']
        except KeyError as e: return 0 # no covers stored
        if len(covers) == 0: return 0 # no covers stored
        elif len(covers) > 1:
            print(f"\r{' '*32}\r{song.name}: has multiple cover images")
        return len(covers[0])
    else:
        print(f"\r{' '*32}\r{song.name}: skipping unrecognized file type ({ext})")
        return 0

if __name__ == "__main__":
    lib_filename = sys.argv[1]
    lib = efit.load_library_from_file(lib_filename)
    song_count = len(lib.songs)
    i_song = 0
    song_sizes = []
    largest_size = 0
    total_size = 0
    for _,song in lib.songs.items():
        i_song += 1
        if efit.is_valid_song(song):
            try: song_path = efit.get_song_path(song)
            except ValueError as e:
                print(f"\r{' '*32}\r{song.name}: file not found")
                continue
            cover_size = get_album_cover_size(song_path)
            if cover_size != 0:
                song_sizes.append((cover_size, song))
            if cover_size > largest_size:
                print(f"\r{' '*32}\r{song.name}: {cover_size} bytes")
                largest_size = cover_size
            total_size += cover_size
        print(f"\r{i_song:6}/{song_count:6} songs processed", end="")
    sorted_sizes = sorted(song_sizes, key=lambda x:x[0], reverse=True)
    for s in sorted_sizes[:1000]:
        print(f"{s[0]}|||{s[1].artist}||||||{s[1].album}{s[1].name}")
    print(f"Total covers size: {total_size/(1024*1024)} MB")