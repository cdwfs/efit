import efit

import mutagen
import mutagen.id3
import mutagen.mp4
import os.path
import sys

def get_itunes_star_rating(song):
    if song.rating_computed:
        return 0
    if song.rating == None:
        return 0
    return round(song.rating * 5 / 100)

def update_mp3_rating(song_path, itunes_stars):
    "Assumes song_path is a valid file. itunes_stars is 0-5."
    # Extract current POPM rating, if any.
    max_stars = 5
    try:
        id3 = mutagen.id3.ID3(song_path)
        popm = id3.getall("POPM")[0]
        if popm.rating != None:
            current_popm_stars = round(popm.rating * max_stars / 255)
    except mutagen.id3._util.ID3NoHeaderError as e: current_popm_stars = 0
    except IndexError as e: current_popm_stars = 0
    # Update POPM tag with new rating if necessary
    if itunes_stars != current_popm_stars:
        print(f"\r{' '*32}\r{song.name}: {current_popm_stars} -> {itunes_stars} stars")
        id3 = mutagen.id3.ID3(song_path)
        rating = round(itunes_stars * 255 / max_stars)
        frame = mutagen.id3.POPM(email="quodlibet@lists.sacredchao.net", rating=rating, count=0)
        id3.setall("POPM", [frame])
        id3.save(song_path, v1=mutagen.id3.ID3v1SaveOptions.REMOVE)

def update_m4a_rating(song_path, itunes_stars):
    "Assumes song_path is a valid file. itunes_stars is 0-5."
    # There is no universal standard for per-file ratings in M4A files.
    # Different players have adopted different conventions in the meantime.
    # It's not clear yet what range each of them uses (0-5, 0-100, 0-255, etc.)
    # For now I'll just cram the itunes star value into every field so as to not
    # lose any data.
    # The "rate" atom stores an integer from 0-100 (used by MediaMonkey)
    changed_tag = False
    mp4_file = mutagen.mp4.MP4(song_path)
    if mp4_file.tags == None:
        mp4_file.add_tags()
        changed_tag = True
    tags = mp4_file.tags

    try: current_rating = round(int(tags["rate"][0]) * 5 / 100)
    except KeyError as e: current_rating = 0
    except TypeError as e:
        print(f"\r{' '*32}\r{song_path}: tag issue!")
        sys.exit(-1)
    if current_rating != itunes_stars:
        print(f"\r{' '*32}\r{song.name}: {current_rating} -> {itunes_stars} stars")
        tags["rate"] = [str(round(itunes_stars * 100 / 5))]
        changed_tag = True
    # Various extended atoms may or may not be used, but store their values as
    # MP4FreeForm instead of raw strings.
    extended_atoms = [
        "----:com.apple.iTunes:POPULARIMETER",
        "----:com.apple.iTunes:RATING",
        "----:com.apple.iTunes:RATING MM",
        "----:com.apple.iTunes:RATING WINAMP",
        "----:com.apple.iTunes:RATING WMP",
    ]
    for key in extended_atoms:
        try: current_rating = int.from_bytes(bytes(tags[key][0]),"little") - ord('0')
        except KeyError as e: current_rating = 0
        if current_rating != itunes_stars:
            tags[key] = [mutagen.mp4.MP4FreeForm(bytes(str(itunes_stars),"utf8"))]
            changed_tag = True
    if changed_tag:
        tags.save(song_path)

if __name__ == "__main__":
    lib_filename = sys.argv[1]
    lib = efit.load_library_from_file(lib_filename)
    song_count = len(lib.songs)
    i_song = 0
    for _,song in lib.songs.items():
        i_song += 1
        if efit.is_valid_song(song):
            try:
                song_path = efit.get_song_path(song)
                if not os.path.isfile(song_path):
                    print(f"\r{' '*32}\r{song.location}: file not found")
                    continue
            except TypeError:
                print(f"\r{' '*32}\rpath error for {song.location}")
                continue
            except ValueError:
                print(f"\r{' '*32}\rpath error for {song.location}")
                continue
            itunes_stars = get_itunes_star_rating(song)
            suffix = song_path[-4:].lower()
            if suffix == ".mp3":
                update_mp3_rating(song_path, itunes_stars)
            elif suffix == ".m4a":
                update_m4a_rating(song_path, itunes_stars)
            else:
                print(f"\r{' '*32}\r{song.name}: skipping unrecognized file type")

        print(f"\r{i_song:6}/{song_count:6} songs processed", end="")