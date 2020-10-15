from pandas import DataFrame
import pandas as pd
import numpy as np
from mido import MidiTrack, MidiFile, MetaMessage, Message

def mido_midi_df(mid):
    """Function to create a tuple of 2 dataframes and an integer containing the
    information parsed by mido.MidiFile()

    :param mid: object returned by mido.MidiFile() :type mid: mido.MidiFile

    :return: a tuple of three dataframes, containing the meta / note information
    and mid.ticks_per_beat :rtype: tuple """
    l = []
    m = []
    for i, track in enumerate(mid.tracks):
        for msg in track:
            l.append(vars(msg))
            m.append(msg.is_meta)
    df = DataFrame(l)
    df['meta'] = m
    df['name'] = df['name'].astype('str')
    # df['time_s'] = mido.tick2second(df['time'])
    df['i_track'] = np.cumsum(df['type'].str.contains('track_name'))
    df_meta = df.query('meta').dropna(how = 'all', axis = 1).drop('meta', axis=1)
    df_notes = df.query('not meta').dropna(how = 'all', axis = 1).drop('meta', axis=1)

    return df_meta, df_notes, mid.ticks_per_beat



def df2mido_midifile(df_meta, df_notes, ticks_per_beat):
    """
    Function to transform the tuple of 2 dataframes produced by the function
    mido_midi_df() into a mido outfile object

    :param df_meta: dataframe containing the meta event information returned by
    mido_midi_df() :type df_meta: pandas.DataFrame :param df_notes: dataframe
    containing the note information returned by mido_midi_df() :type df_notes:
    pandas.DataFrame :param ticks_per_beat: integer containing the
    ticks_per_beat information returned by mido_midi_df() :type ticks_per_beat:
    integer

    :return: outfile
    :rtype: mido.outfile object
    """
    df_notes = df_notes.reset_index()
    outfile = MidiFile(ticks_per_beat=ticks_per_beat)

    track = MidiTrack()

    track.append(MetaMessage('set_tempo', tempo = int(df_meta.loc[df_meta.type == 'set_tempo', 'tempo'])))
    track.append(MetaMessage('time_signature',
                             numerator = int(df_meta.loc[df_meta.type == 'time_signature', 'numerator']),
                             denominator = int(df_meta.loc[df_meta.type == 'time_signature', 'denominator'])))#,
    #                              clocks_per_click = df.loc[i, 'clocks_per_click'],
    #                              notated_32nd_notes_per_beat = df.loc(i, 'notated_32nd_notes_per_beat')))

    # track.append(Message('program_change', program=12))
    new_track_row = np.array(df_notes.i_track != df_notes.i_track.shift(1))
    last_in_track_row = np.array(df_notes.i_track != df_notes.i_track.shift(1))
    end_of_track_times = np.array(df_meta.loc[df_meta.type == 'end_of_track', 'time'])
    i_track = 0
    for i in range(len(df_notes)):
        # meta messages:
        # if df.loc[i, 'type'] == 'track_name':
        if new_track_row[i]:
            track = MidiTrack()
            outfile.tracks.append(track)
        if last_in_track_row[i]:
            track.append(MetaMessage('end_of_track', time = end_of_track_times[i_track]))
            i_track += 1
        if df_notes.loc[i, 'type'] == 'note_on':
            track.append(Message('note_on',
                                 note=df_notes.loc[i, 'note'].astype(int),
                                 velocity=df_notes.loc[i, 'velocity'].astype(int),
                                 channel=df_notes.loc[i, 'channel'].astype(int),
                                 time=df_notes.loc[i, 'time'].astype(int)))
        elif df_notes.loc[i, 'type'] == 'note_off':
            track.append(Message('note_off',
                                 note=df_notes.loc[i, 'note'].astype(int),
                                 velocity=df_notes.loc[i, 'velocity'].astype(int),
                                 time=df_notes.loc[i, 'time'].astype(int)))
    return outfile


def df_2_midi(df_meta, df_notes, ticks_per_beat, file):
    """
    Function to write midi dataframes returned by mido_midi_df() back to a midi
    file a mido outfile object

    :param df_meta: dataframe containing the meta event information returned by
    mido_midi_df() :type df_meta: pandas.DataFrame :param df_notes: dataframe
    containing the note information returned by mido_midi_df() :type df_notes:
    pandas.DataFrame :param ticks_per_beat: integer containing the
    ticks_per_beat information returned by mido_midi_df() :type ticks_per_beat:
    integer :param file: string containing the name of the midi file to be
    written :type file: string
    """
    outfile = df2mido_midifile(df_meta, df_notes, ticks_per_beat)
    outfile.save(file)







def midi_to_df(mid):
    """Function to create a dataframe containing the
    information parsed by mido.MidiFile()

    :param mid: object returned by mido.MidiFile()
    :type mid: mido.MidiFile

    :return: a dataframe, containing 3 columns:
    :rtype: pandas.DataFrame

    The function :func:`miditapyr.mido_io.compact_df` returns a
    dataframe of the same format. This dataframe contains these columns:

        * **i_track**: the track number
        * **msg**: the (meta) event information read by `mido.MidiFile() <https://mido.readthedocs.io/en/latest/midi_files.html#>`_ in a list of dictionaries
        * **meta**: whether the event in 'msg' is a `mido meta event <https://mido.readthedocs.io/en/latest/midi_files.html#meta-messages>`_

    """
    l = []
    for i_track, track in enumerate(mid.tracks):
        for msg in track:
            l.append({**{'i_track': i_track}, **{'meta': msg.is_meta}, **{'msg': vars(msg)}})
    df = pd.DataFrame(l)
    # df.ticks_per_beat = mid.ticks_per_beat

    return df


def tidy_df(dfc):
    """
    Function to transform the dataframe returned by midi_to_df() in a tidy
    format (cf. https://r4ds.had.co.nz/tidy-data.html)

    :param dfc: Dataframe returned by midi_to_df

    :type dfc: pandas.DataFrame

    :return: a dataframe
    :rtype: pandas.DataFrame

    The returned dataframe with the columns i_track and meta of midi_to_df. The
    msg column is exploded and each key in the dicts in the `msg` column of
    :func:`miditapyr.mido_io.midi_to_df` is stored in its own column.

    """

    df = pd.concat([dfc[['i_track', 'meta']],
                    pd.DataFrame(list(dfc['msg']))
                    ],
                   axis = 1)
    return df

def split_df(df):
    """Function to create a tuple of 2 dataframes containing the
    information parsed by mido.MidiFile()

    :param df: dataframe returned by tidy_df()
    :type dfc: pandas.DataFrame

    :return: a tuple of 2 dataframes, containing the meta / note information
    :rtype: tuple """
    df_meta = df.query('meta').dropna(how = 'all', axis = 1)#.drop('meta', axis=1)
    df_notes = df.query('not meta').dropna(how = 'all', axis = 1)#.drop('meta', axis=1)

    return df_meta, df_notes

def df_to_midi(dfc, ticks_per_beat, filename):
    """
    Function to write midi dataframes returned by midi_to_df() back to a midi
    file

    :param dfc: dataframe containing the meta event information returned by midi_to_df
    :type dfc: pandas.DataFrame
    :param ticks_per_beat: integer containing the ticks_per_beat information returned by mido.MidiFile
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

def compact_df(df, repair_reticulate_conversion = False):
    """
    Function to transform the dataframe returned by tidy_df() back to a format
    as in the result of midi_to_df()

    :param df: Dataframe returned by tidy_df()
    :type dfc: pandas.DataFrame

    :return: a dataframe, containing 3 columns
    :rtype: pandas.DataFrame

    The function :func:`miditapyr.mido_io.midi_to_df` returns a
    dataframe of the same format. This dataframe contains these columns:

        * **i_track**: the track number
        * **msg**: the (meta) event information read by `mido.MidiFile() <https://mido.readthedocs.io/en/latest/midi_files.html#>`_ in a list of dictionaries
        * **meta**: whether the event in 'msg' is a `mido meta event <https://mido.readthedocs.io/en/latest/midi_files.html#meta-messages>`_

    """
    dict_list = [v.dropna().to_dict() for k,v in df.drop(columns=['i_track', 'meta']).iterrows()]
    # This is necessary because conversion the R package reticulate that
    # converts dataframes from pandas to R converts integers to R numeric types.
    # When converting back to pandas this would cause an error in mido when
    # calling df_to_midi() on the result of this function...
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
