import pytest 
import pandas as pd
import mido
import miditapyr.mido_io as mtio
import miditapyr.midi_frame as mtmf

@pytest.fixture
def mfm():
    mid = mtio.get_test_midi_file(as_string=True)
    mfm = mtmf.MidiFrames(mid)
    return mfm


def test_init_empty_and_fill(mfm):
    mid = mtio.get_test_midi_file(as_string=True)
    mfe = mtmf.MidiFrames()


    with pytest.raises(Exception) as e_info:
        mfe.midi_frame_unnested.df

    assert e_info.value.args[0] == 'df is None'

    mfe.calc_attributes(mid)

    assert mfe.midi_frame_unnested.df.equals(mfm.midi_frame_unnested.df)
    


def test_modify_midi_frame(mfm):
    mfu = mfm.midi_frame_unnested.df
    mfn = mfm.midi_frame_nested.df

    mfm.midi_frame_unnested.update_unnested_mf(mfu.loc[0:10,])

    assert mfm.midi_frame_nested.df.equals(mfn.loc[0:10,])
