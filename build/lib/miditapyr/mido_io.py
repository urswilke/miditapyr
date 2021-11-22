import pandas as pd
from mido import MidiTrack, MidiFile, MetaMessage, Message
import io, pkgutil
import os, sys

def frame_midi(mid):
    """Function to create a dataframe containing the
    information parsed by :class:`~mido.MidiFile`

    :param mid: object of class :class:`~mido.MidiFile`
    :type mid: :class:`~mido.MidiFile`

    :return: a dataframe, containing 3 columns:
    :rtype: :class:`~pandas.DataFrame`

    The function :func:`~miditapyr.mido_io.nest_midi` returns a
    dataframe of the same format. This dataframe contains these columns:

        * **i_track**: the track number
        * **msg**: the (meta) event information in :class:`~mido.MidiFile` in a list of dictionaries
        * **meta**: whether the event in 'msg' is a `mido meta event <https://mido.readthedocs.io/en/latest/midi_files.html#meta-messages>`_

    """
    l = []
    for i_track, track in enumerate(mid.tracks):
        for msg in track:
            l.append({**{'i_track': i_track}, **{'meta': msg.is_meta}, **{'msg': vars(msg)}})
    df = pd.DataFrame(l)
    # df.ticks_per_beat = mid.ticks_per_beat

    return df


def unnest_midi(dfc):
    """
    Function to transform the dataframe returned by :func:`~frame_midi` in a tidy
    format (cf. https://r4ds.had.co.nz/tidy-data.html)

    :param dfc: Dataframe returned by :func:`~frame_midi`

    :type dfc: :class:`~pandas.DataFrame`

    :return: a dataframe
    :rtype: :class:`~pandas.DataFrame`

    The returned dataframe with the columns i_track and meta of :func:`~unnest_midi`. The
    msg column is exploded and each key in the dicts in the `msg` column of
    :func:`~miditapyr.mido_io.frame_midi` is stored in its own column.

    """

    df_unnest_wide = pd.DataFrame(list(dfc['msg']))
    df = pd.concat([dfc[['i_track', 'meta']],
                    df_unnest_wide],
                   axis = 1)
    return df

def split_df(df):
    """Function to create a tuple of 2 dataframes containing the
    information in :class:`~mido.MidiFile`

    :param df: dataframe returned by :func:`~unnest_midi`
    :type dfc: :class:`~pandas.DataFrame`

    :return: a tuple of 2 dataframes, containing the meta / note information
    :rtype: tuple """
    df_meta = df.query('meta').dropna(how = 'all', axis = 1)#.drop('meta', axis=1)
    df_notes = df.query('not meta').dropna(how = 'all', axis = 1)#.drop('meta', axis=1)

    return df_meta, df_notes

def write_midi(dfc, ticks_per_beat, filename):
    """
    Function to write midi dataframes returned by :func:`~nest_midi` back to a midi
    file

    :param dfc: dataframe containing the meta event information returned by :func:`~unnest_midi`
    :type dfc: :class:`~pandas.DataFrame`
    :param ticks_per_beat: integer containing the ticks_per_beat information in :class:`~mido.MidiFile`
    :type ticks_per_beat: integer
    :param filename: string containing the name of the midi file to be written
    :type filename: string
    """
    outfile = MidiFile()
    outfile.ticks_per_beat = ticks_per_beat
    track = MidiTrack()
    outfile.tracks.append(track)
    for index, row in dfc.iterrows():
        if row['meta'] == True:
            if row['msg']['type'] == 'track_name':
                track = MidiTrack()
                outfile.tracks.append(track)
            track.append(MetaMessage(**row['msg']))
        else:
            track.append(Message(**row['msg']))
    outfile.save(filename)

def nest_midi(df, repair_reticulate_conversion = False):
    """
    Function to transform the dataframe returned by :func:`~unnest_midi` back to a format
    as in the result of :func:`~unnest_midi`

    :param df: Dataframe returned by :func:`~unnest_midi`
    :type dfc: :class:`~pandas.DataFrame`

    :return: a dataframe, containing 3 columns
    :rtype: :class:`~pandas.DataFrame`

    The function :func:`miditapyr.mido_io.frame_midi` returns a
    dataframe of the same format. This dataframe contains these columns:

        * **i_track**: the track number
        * **msg**: the (meta) event information in :class:`~mido.MidiFile` `(see here) <https://mido.readthedocs.io/en/latest/midi_files.html#>`_ in a list of dictionaries
        * **meta**: whether the event in 'msg' is a `mido meta event <https://mido.readthedocs.io/en/latest/midi_files.html#meta-messages>`_

    """
    dict_list = [v.dropna().to_dict() for k,v in df.drop(columns=['i_track', 'meta']).iterrows()]
    # This is necessary because conversion the R package reticulate that
    # converts dataframes from pandas to R converts integers to R numeric types.
    # When converting back to pandas this would cause an error in mido when
    # calling write_midi() on the result of this function...
    if repair_reticulate_conversion == True:
        for dicts in dict_list:
            for key, value in dicts.items():
                if type(value) == float:
                    dicts[key] = int(value)

    df_events = pd.DataFrame()
    df_events['msg'] = dict_list
    dfc2 = pd.concat([df[['i_track', 'meta']].reset_index(drop=True),
                      df_events.reset_index(drop=True)
                     ],
                     axis = 1)
    return dfc2


def get_test_midi_file(as_string=False):
    # midi_file = pkgutil.get_data(__name__, 'data/test_midi_file.mid') mostly
    # inspired by
    # https://stackoverflow.com/questions/5003755/how-to-use-pkgutils-get-data-with-csv-reader-in-python :
    package = 'miditapyr'
    loader = pkgutil.get_loader(package)
    mod = sys.modules.get(package) or loader.load_module(package)
    midi_file = os.path.dirname(mod.__file__) + '/data/test_midi_file.mid'
    mido_midi_file = MidiFile(midi_file)
    if as_string == False:
        result = mido_midi_file
    else:
        result = midi_file
    return result
    # return midi_file
