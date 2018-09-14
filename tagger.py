import efit

import codecs
import mutagen
import mutagen.id3
import os.path
import sys
import time

def print_tag_errors(lib):
    song_count = len(lib.songs.items())
    song_index = 0
    for id, song in lib.songs.items():
        song_index += 1
        print("\r%s\r%d/%d" % (' '*40, song_index, song_count), end='')
        sys.stdout.flush()
        if not efit.is_valid_song(song):
            continue # song is a podcast, protected file, video, 
        song_path = efit.get_song_path(song)
        if not song_path:
            continue # song can not be found on the current drive
        #print(codecs.encode(song_path, encoding='utf-8', errors='replace'))
        try:
            id3 = mutagen.id3.ID3(song_path)
            # Remove unwanted tag frames
            for fid in ["GVAD", "GBAD", "GEOB", "RGAD", "RVAD", "LAME", "TENM", "UFID", "WXXX", "XSOT"]:
                id3.delall(fid)
            id3.save(song_path, v1=mutagen.id3.ID3v1SaveOptions.REMOVE)
        except mutagen.id3._util.ID3NoHeaderError as e:
            print("\nERROR:", e, "in:")
            print(codecs.encode(song_path, encoding='utf-8', errors='replace'))
        except:
            e = sys.exc_info()[0]
            print("\nERROR: ", e, " in:")
            print(codecs.encode(song_path, encoding='utf-8', errors='replace'))
            raise

def fix_tags(file_list):
    for line in open(file_list, "r"):
        filename = line.strip()
        if os.path.isfile(filename):
            try:
                id3 = mutagen.id3.ID3(filename)
                # Remove unwanted tag frames
                for fid in ["GVAD", "GBAD", "GEOB", "RGAD", "RVAD", "LAME", "TENM", "UFID", "WXXX"]:
                    id3.delall(fid)
                #id3.save(filename, v1=mutagen.id3.ID3v1SaveOptions.REMOVE)
            except mutagen.id3._util.ID3NoHeaderError as e:
                print("ERROR: in " + codecs.encode(song_path, encoding='utf-8', errors='replace') + ":" + e)
            except:
                e = sys.exc_info()[0]
                print("ERROR: in " + codecs.encode(song_path, encoding='utf-8', errors='replace') + ":" + e)
                raise
            #print(codecs.encode(filename, encoding='utf-8', errors='replace'))

if __name__ == "__main__":
    lib_filename = sys.argv[1]
    lib = efit.load_library_from_file(lib_filename)
    print_tag_errors(lib)

    #fix_tags(sys.argv[1])
