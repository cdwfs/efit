import efit

import mutagen
import mutagen.id3
import os.path
import sys

def set_popm_rating(filename, stars, max_stars = 5):
    id3 = mutagen.id3.ID3(filename)
    rating = round(stars * 255 / max_stars)
    frame = mutagen.id3.POPM(email="quodlibet@lists.sacredchao.net", rating=rating, count=0)
    id3.setall("POPM", [frame])
    id3.save(filename, v1=mutagen.id3.ID3v1SaveOptions.REMOVE)

def get_popm_rating(filename, max_stars = 5):
    if not os.path.isfile(filename):
        return 0
    try:
        id3 = mutagen.id3.ID3(filename)
        popm = id3.getall("POPM")[0]
        if popm.rating == None:
            return 0
        return round(popm.rating * max_stars / 255)
    except mutagen.id3._util.ID3NoHeaderError as e:
        return 0
    except IndexError as e:
        return 0

def get_itunes_star_rating(song):
    if song.rating_computed:
        return 0
    if song.rating == None:
        return 0
    return round(song.rating * 5 / 100)

if __name__ == "__main__":
    lib_filename = sys.argv[1]
    lib = efit.load_library_from_file(lib_filename)
    song_count = len(lib.songs)
    i_song = 0
    for _,song in lib.songs.items():
        i_song += 1
        if efit.is_valid_song(song):
            song_path = efit.get_song_path(song)
            itunes_stars = get_itunes_star_rating(song)
            popm_stars = get_popm_rating(song_path)
            if itunes_stars != popm_stars:
                print(f"\r{' '*32}\r{song.name}: {popm_stars} -> {itunes_stars} stars")
                set_popm_rating(song_path, itunes_stars)
        print(f"\r{i_song:6}/{song_count:6} songs processed", end="")