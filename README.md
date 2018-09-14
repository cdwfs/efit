Escape From iTunes
------------------

A bundle of Python scripts to help an iTunes user of 13+ years
gracefully migrate to a new platform with my library intact.

Use cases important to me:

- **[DONE]** Load an exported iTunes library XML file.
- **[DONE]** Convert library to a more compact, easier-to-load format (pickle, most likely).
- Copy star ratings from iTunes library (stored as library-level metadata) to ID3v2.
  POPM tags (stored per-file).
- **[DONE]** Export existing iTunes playlists to a standard format.
  Must support UTF8 filenames. ([.M3U8](https://en.wikipedia.org/wiki/M3U)?)

- Limited "smart playlist" generation (create and export new playlists.
  directly from the library, like "everything by Pink Floyd").
- Scan & report mismatches between iTunes library ratings and ID3 ratings.
- Long-term, maybe just ditch the iTunes baggage entirely and develop a custom
  library format.

Dependencies:

- [libpytunes](https://github.com/liamks/libpytunes) -- iTunes XML library loading and manipulation
- [mutagen](https://github.com/quodlibet/mutagen) -- ID3 tag manipulation
