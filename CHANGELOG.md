## CHANGELOG

* **0.1**
    * add dynamic linking to used objects in documentation with sphinx.ext.intersphinx
    * **Breaking changes**
        * rename functions:
            * `midi_to_df()` to `frame_midi()`
            * `tidy_df()` to `unnest_midi()`
            * `compact_df()` to `nest_midi()`
            * `df_to_midi()` to `write_midi()`
        * rename classes:
            * `MidiFrameTidy` to `MidiFrameUnnested`
            * `MidiFrameCompact` to `MidiFrameNested`
        * rename "tidy" to "unnested"
        * rename "compact" to "nested"
        * rename midi_frame_nested.midi_frame_nested to midi_frame_nested.df
        * rename midi_frame_unnested.midi_frame_unnested to midi_frame_unnested.df


* **0.0.3**
    * add MidiFrames class
    * adapt documentation


* **0.0.2**
    * add codecov gh action
    * add ci workflow gh action
    * add badges
    * include notebook in readthedocs
    * add hex logo
    * add midi file "miditapyr/data/test_midi_file.mid" included in package
    * add function get_test_midi_file() loading "test_midi_file.mid"
    * add requirements.txt and adapt setup.py
    * add test for roundtripping



* **0.0.1**
    * rewrite notebooks/pyramidi_integration.ipynb
    * use new notebooks/test_midi_file.mid
    * also add notebooks/test_midi_file.mp3
    * remove function mido_midi_df
    * remove function df2mido_midifile
    * remove function df_2_midi
    * add function compact_df
    * add function df_to_midi
    * add function split_df
    * add function tidy_df
    * add function midi_to_df
* **0.0.0.9000**
    * Work in progress
