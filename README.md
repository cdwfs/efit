Escape From iTunes
------------------

A bundle of Python scripts to help an iTunes user of 13+ years
gracefully migrate to a new platform with my library intact.

Use cases important to me:

- **[DONE]** Load an exported iTunes library XML file.
- **[DONE]** Convert library to a more compact, easier-to-load format (pickle, most likely).
- **[DONE]** Support processing MP3 and M4A (AAC) files
- **[DONE]** Copy star ratings from iTunes library (stored as library-level metadata) to per-file metadata (`POPM` for ID3, `rate` for M4A, etc.).
- **[DONE]** Export existing iTunes playlists to a standard format ([.M3U8](https://en.wikipedia.org/wiki/M3U).
- **[DONE]** Scan & report mismatches between iTunes library ratings and ID3 ratings.
- **[DONE]** Scan and report/fix Library errors (random pointless tags, missing files, malformed metadata, etc.)
- Limited "smart playlist" generation (create and export new playlists.
  directly from the library, using an iTunes-like query language).
- Long-term, maybe just ditch the iTunes baggage entirely and develop a custom
  library format.

Dependencies:

- [libpytunes](https://github.com/liamks/libpytunes) -- iTunes XML library loading and manipulation
- [mutagen](https://github.com/quodlibet/mutagen) -- audio tag manipulation
