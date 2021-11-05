import pandas as pd
import mido
import miditapyr.mido_io as mt


mido_midi_file = mt.get_test_midi_file()
dfc0 = mt.midi_to_df(mido_midi_file)
dft0 = mt.tidy_df(dfc0)
dfc1 = mt.compact_df(dft0, True)
dft1 = mt.tidy_df(dfc1)

def test_tidy_compact_roundtripping():
    # test that from tidy -> compact -> back to tidy results in the same
    # dataframe:
    assert dft0.equals(dft1)



def test_save_read_roundtripping(tmp_path):
    # test that for a midifile saved and read in by miditapyr ('dfc2'), saving
    # and reloading by miditapyr results in equal dataframes (in tidy
    # format).
    d = tmp_path / "sub"
    filename2 = 'temp_midifile' + '2' + '.mid'
    d.mkdir()
    path2 = d / filename2
    mt.df_to_midi(dfc1, mido_midi_file.ticks_per_beat, path2)
    mido_midi_file2 = mido.MidiFile(path2)
    dfc2 = mt.midi_to_df(mido_midi_file2)
    dft2 = mt.tidy_df(dfc2)

    d = tmp_path / "sub"
    filename3 = 'temp_midifile' + '3' + '.mid'
    path3 = d / filename3
    mt.df_to_midi(dfc2, mido_midi_file.ticks_per_beat, path3)
    mido_midi_file3 = mido.MidiFile(path3)
    dfc3 = mt.midi_to_df(mido_midi_file3)
    dft3 = mt.tidy_df(dfc3)

    d = tmp_path / "sub"
    filename4 = 'temp_midifile' + '4' + '.mid'
    path4 = d / filename4
    mt.df_to_midi(dfc3, mido_midi_file.ticks_per_beat, path4)
    mido_midi_file4 = mido.MidiFile(path4)
    dfc4 = mt.midi_to_df(mido_midi_file4)
    dft4 = mt.tidy_df(dfc4)

    # The tests only pass for midifiles that have been generated from dataframes
    # in miditapyr:
    assert dft3.equals(dft2)
    assert dft4.equals(dft3)
    # i.e. this wouldn't pass
    # assert dft1.equals(dft0)
    assert mido_midi_file3.ticks_per_beat == mido_midi_file4.ticks_per_beat
