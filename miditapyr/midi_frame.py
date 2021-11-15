from miditapyr import mido_io 
from mido import MidiFile

# When object of class MidiFrameTidy is updated with method update_tidy_mf,
# this also triggers an update of the observing class MidiFrameCompact
# (observer pattern inspired by https://en.wikipedia.org/wiki/Observer_pattern#Python)
class MidiFrameTidy:
    """Class containing the :class:`~pandas.DataFrame` :obj:`midi_frame_tidy`. 
    
    :obj:`midi_frame_tidy` can be updated with :meth:`update_tidy_mf`. 
    This also triggers an update of objects of the observing class :class:`MidiFrameCompact`.

    :param midi_frame_raw: :class:`~pandas.DataFrame` resulting of :func:`~mido_io.midi_to_df`.
    """
    def __init__(self, midi_frame_raw):
        self._observers = []
        self.midi_frame_tidy = mido_io.tidy_df(midi_frame_raw)

    def register_observer(self, observer):
        self._observers.append(observer)

    def update_tidy_mf(self, tidy_mf_mod):
        self.midi_frame_tidy = tidy_mf_mod
        for obs in self._observers:
            obs.update_mf_compact(self, tidy_mf_mod)


class MidiFrameCompact:
    """Class containing the :class:`~pandas.DataFrame` :obj:`midi_frame_compact` observing an object of  :class:`MidiFrameTidy`.

    When the observed object :obj:`midi_frame_tidy` is updated with :meth:`MidiFrameTidy.update_tidy_mf`, :obj:`midi_frame_compact`
    is also automatically updated with :meth:`MidiFrameCompact.update_mf_compact`.

    :param midi_frame_tidy: :class:`~pandas.DataFrame` resulting of :func:`~miditapyr.mido_io.tidy_df`.
    """
    def __init__(self, midi_frame_tidy):
        midi_frame_tidy.register_observer(self)
        self.midi_frame_compact = mido_io.compact_df(
            midi_frame_tidy.midi_frame_tidy, 
            repair_reticulate_conversion = True
        )

    def update_mf_compact(self, midi_frame_tidy, tidy_mf_mod):
        self.midi_frame_compact = mido_io.compact_df(
            tidy_mf_mod, 
            repair_reticulate_conversion = True
        )

class MidiFrames(object):
    """
    Structure that reads in a midi file and has the following attributes:
    
    * :attr:`midi_file`: The midi data as a :class:`~mido.MidiFile` object.
    * :attr:`midi_frame_raw`:  :class:`~pandas.DataFrame` returned by :func:`~miditapyr.mido_io.midi_to_df`.
    * :attr:`midi_frame_tidy`:  :class:`~miditapyr.midi_frame.MidiFrameTidy` object (contains :obj:`midi_frame_tidy.midi_frame_tidy`, a :class:`~pandas.DataFrame` returned by :func:`~miditapyr.mido_io.tidy_df`).
    * :attr:`midi_frame_compact`: :class:`~miditapyr.midi_frame.MidiFrameCompact` object (contains :obj:`midi_frame_compact.midi_frame_compact`, a :class:`~pandas.DataFrame` returned by :func:`~miditapyr.mido_io.compact_df`).
    * :meth:`~MidiFrames.write_file`: Writes back the midi data to a midi file.
    
    The dataframe :attr:`midi_frame_tidy.midi_frame_tidy` can be manipulated with the method :meth:`~miditapyr.midi_frame.MidiFrameTidy.update_tidy_mf`.
    This also triggers an update of the dataframe :obj:`midi_frame_compact.midi_frame_compact` with the method :func:`~miditapyr.midi_frame.MidiFrameCompact.update_mf_compact`.
    
    When :func:`~miditapyr.midi_frame.MidiFrameTidy.update_tidy_mf` was not called, the attribute :obj:`midi_frame_compact.midi_frame_compact` should be
    identical to :obj:`midi_frame_raw`. After calling :func:`~miditapyr.midi_frame.MidiFrameTidy.update_tidy_mf`, :obj:`midi_frame_compact.midi_frame_compact`
    should also contain the changes made to :obj:`midi_frame_tidy.midi_frame_tidy`.


    You can write back the midi data to a midi file by calling the method :meth:`~MidiFrames.write_file`.

    :param midi_file_string: String containing the path to the input midi file.
    """
    def __init__(self, midi_file_string):
        self.midi_file = MidiFile(midi_file_string)
        self.midi_frame_raw = mido_io.midi_to_df(self.midi_file)
        self.midi_frame_tidy = MidiFrameTidy(self.midi_frame_raw)
        self.midi_frame_compact = MidiFrameCompact(self.midi_frame_tidy) 

    def write_file(self, out_file_string):
        """Write midi data back to midi file

        :param out_file_string: midi file path where the file should be stored.
        """
        mido_io.df_to_midi(
            self.midi_frame_compact.midi_frame_compact,
            self.midi_file.ticks_per_beat,
            out_file_string
        )

