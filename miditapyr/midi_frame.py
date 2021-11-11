from miditapyr import mido_io
from mido import MidiFile

class MidiFrame():
    """
    Structure to read in a midi file as a mido.MidiFile. 
    
    Then the data is translated to dataframes with midi_to_df(), tidy_df() 
    and compact_df() and written back to a midi file if out_file_string is provided.
    The intermediate result of tidy_df() can be manipulated with mod_fun (of provided).

    :param midi_file_string: String containing the path to the input midi file.
    :param mod_fun: Function object to manipulate the intermediate result of tidy_df().
    :param out_file_string: String containing the path to the output midi file.
    """
    def __init__(self, midi_file_string, mod_fun=None, out_file_string=None):
        midi_file = MidiFile(midi_file_string)
        midi_frame_raw = mido_io.midi_to_df(midi_file)
        midi_frame_tidy = mido_io.tidy_df(midi_frame_raw)
        if mod_fun is not None:
            midi_frame_tidy = mod_fun(midi_frame_tidy)
        midi_frame_compact = mido_io.compact_df(midi_frame_tidy, repair_reticulate_conversion = True)
        self.midi_frame_raw = midi_frame_raw
        self.midi_frame_tidy = midi_frame_tidy
        self.midi_frame_compact = midi_frame_compact
        self.midi_file_name = midi_file_string
        self.midi_file = midi_file
        if out_file_string is not None:
            mido_io.df_to_midi(
                self.midi_frame_compact,
                self.midi_file.ticks_per_beat,
                out_file_string
            )

