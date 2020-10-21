import mido
import miditapyr as mt

def test_roundtripping():
    # mido_mid_file = mido.MidiFile(mt.get_test_midi_file())
    mido_mid_file = mt.get_test_midi_file()
    dfc = mt.midi_to_df(mido_mid_file)

    assert dfc.eq(mt.compact_df(mt.tidy_df(dfc))).all(axis=1).all()
