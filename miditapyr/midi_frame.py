from miditapyr import mido_io 
from mido import MidiFile

# When object of class MidiFrameUnnested is updated with method update_unnested_mf,
# this also triggers an update of the observing class MidiFrameNested
# (observer pattern inspired by https://en.wikipedia.org/wiki/Observer_pattern#Python)
class MidiFrameUnnested:
    """Class containing the :class:`~pandas.DataFrame` :obj:`df`. 
    
    :obj:`df` can be updated with :meth:`update_unnested_mf`. 
    This also triggers an update of objects of the observing class :class:`MidiFrameNested`.

    :param midi_frame_raw: :class:`~pandas.DataFrame` resulting of :func:`~miditapyr.mido_io.frame_midi`.
    """
    def __init__(self, midi_frame_raw=None):
        self._observers = []
        self._df = None

        if midi_frame_raw is not None:
            self._df = self.calc_df(midi_frame_raw)

    @property
    def df(self):
        if self._df is None:
            raise Exception('df is None')
        return self._df

    def calc_df(self, midi_frame_raw):    
        self._df = mido_io.unnest_midi(midi_frame_raw)

    def register_observer(self, observer):
        self._observers.append(observer)

    def update_unnested_mf(self, unnested_mf_mod):
        self._df = unnested_mf_mod
        for obs in self._observers:
            obs.update_mf_nested(self, unnested_mf_mod)


class MidiFrameNested:
    """Class containing the :class:`~pandas.DataFrame` :obj:`df` observing an object of  :class:`MidiFrameUnnested`.

    When the observed object :obj:`midi_frame_unnested` is updated with :meth:`MidiFrameUnnested.update_unnested_mf`, :obj:`midi_frame_nested`
    is also automatically updated with :meth:`MidiFrameNested.update_mf_nested`.

    :param midi_frame_unnested: :class:`~pandas.DataFrame` resulting of :func:`~miditapyr.mido_io.unnest_midi`.
    """
    def __init__(self, midi_frame_unnested=None):
        midi_frame_unnested.register_observer(self)
        self._df = None

        if midi_frame_unnested._df is not None:
            self._df = self.calc_df(midi_frame_unnested)

    @property
    def df(self):
        if self._df is None:
            raise Exception('df is None')
        return self._df

    def calc_df(self, midi_frame_unnested):    
        self._df = mido_io.nest_midi(
            midi_frame_unnested.df, 
            repair_reticulate_conversion = True
        )

    def update_mf_nested(self, midi_frame_unnested, unnested_mf_mod):
        self._df = mido_io.nest_midi(
            unnested_mf_mod, 
            repair_reticulate_conversion = True
        )

class MidiFrames(object):
    """
    Structure that reads in a midi file and has the following attributes:
    
    :ivar `midi_file`: The midi data as a :class:`~mido.MidiFile` object.
    :ivar `midi_frame_raw`:  :class:`~pandas.DataFrame` returned by :func:`~miditapyr.mido_io.frame_midi`.
    :ivar `midi_frame_unnested`:  :class:`~miditapyr.midi_frame.MidiFrameUnnested` object (contains :obj:`midi_frame_unnested.df`, a :class:`~pandas.DataFrame` returned by :func:`~miditapyr.mido_io.unnest_midi`).
    :ivar `midi_frame_nested`: :class:`~miditapyr.midi_frame.MidiFrameNested` object (contains :obj:`midi_frame_nested.df`, a :class:`~pandas.DataFrame` returned by :func:`~miditapyr.mido_io.nest_midi`).
    
    The dataframe :attr:`midi_frame_unnested.df` can be manipulated with the method :meth:`~miditapyr.midi_frame.MidiFrameUnnested.update_unnested_mf`.
    This also triggers an update of the dataframe :obj:`midi_frame_nested.df` with the method :func:`~miditapyr.midi_frame.MidiFrameNested.update_mf_nested`.
    
    When :func:`~miditapyr.midi_frame.MidiFrameUnnested.update_unnested_mf` was not called, the attribute :obj:`midi_frame_nested.df` should be
    identical to :obj:`midi_frame_raw`. After calling :func:`~miditapyr.midi_frame.MidiFrameUnnested.update_unnested_mf`, :obj:`midi_frame_nested.df`
    should also contain the changes made to :obj:`midi_frame_unnested.df`.


    You can write back the midi data to a midi file by calling the method :meth:`~MidiFrames.write_file`.

    :param midi_file_string: String containing the path to the input midi file.
    """
    def __init__(self, midi_file_string=None):
        self._midi_file = MidiFile()
        self._midi_frame_raw = None
        self._midi_frame_unnested = MidiFrameUnnested(None)
        self._midi_frame_nested = MidiFrameNested(self._midi_frame_unnested) 

        if midi_file_string is not None:
            self.calc_attributes(midi_file_string)

    @property
    def midi_file(self):
        if self._midi_file is None:
            raise Exception('midi_file is None')
        return self._midi_file
    
    @property
    def midi_frame_raw(self):
        if self._midi_frame_raw is None:
            raise Exception('midi_frame_raw is None')
        return self._midi_frame_raw
    
    @property
    def midi_frame_unnested(self):
        if self._midi_frame_unnested is None:
            raise Exception('midi_frame_unnested is None')
        return self._midi_frame_unnested
    
    @property
    def midi_frame_nested(self):
        if self._midi_frame_nested is None:
            raise Exception('midi_frame_nested is None')
        return self._midi_frame_nested
    
    def calc_attributes(self, midi_file_string):    
        self._midi_file = MidiFile(midi_file_string)
        self._midi_frame_raw = mido_io.frame_midi(self.midi_file)
        self._midi_frame_unnested.calc_df(self.midi_frame_raw)
        self._midi_frame_nested.calc_df(self.midi_frame_unnested) 

    def write_file(self, out_file_string):
        """Write midi data back to midi file

        :param out_file_string: midi file path where the file should be stored.
        """
        mido_io.write_midi(
            self.midi_frame_nested.df,
            self.midi_file.ticks_per_beat,
            out_file_string
        )

