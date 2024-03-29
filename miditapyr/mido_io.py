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
    """Get the example midi file included in the

    :param as_string: Should the midi file be returned as a file path or as a :class:`~mido.MidiFile` object, defaults to False
    :type as_string: bool, optional
    :return: file path or as a :class:`~mido.MidiFile`
    :rtype: file path or as a :class:`~mido.MidiFile`
    """
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




def split_midi_frame(df_unnested):
    """
    Split unnested midi frame into 3 dataframes.

    :param df_unnested: result of :func:`~unnest_midi`
    :type df_unnested: :class:`~pandas.DataFrame`
    :returns: (tuple) of 3 dataframes df_meta, df_not_notes & df_notes
    
       - :obj:`df_meta` - (containing all mido meta events), 
       - :obj:`df_not_notes` - (non-meta events that are not :obj:`note_on` or :obj:`note_off`) & 
       - :obj:`df_notes` - (all :obj:`note_on` or :obj:`note_off` events).

    :rtype: tuple of 3 :class:`~pandas.DataFrame`
    """
    df_meta, df_not_meta = split_df(df_unnested)

    is_note_row = df_not_meta.type.str.contains('^note_o[nf]f?$')

    df_notes = df_not_meta[is_note_row]
    df_not_notes = df_not_meta[~is_note_row]

    return df_meta, df_not_notes, df_notes

def pivot_notes_wide(df_notes):
    """
    Write :obj:`note_on` and :obj:`note_off` events in the same line (long to wide)

    :param df_notes: Notes dataframe from :func:`split_midi_frame`
    :type df_notes: :class:`~pandas.DataFrame`
    :return: Dataframe with half the number of rows, but the time & velocity columns occur twice for all :obj:`note_on` or :obj:`note_off` events.
    :rtype: :class:`~pandas.DataFrame`
    """
    df_notes_c = df_notes.copy(deep = True)
    # # calculate absolute time for all events in each track:
    # df_notes_c['t']=df_notes_c.groupby(['i_track'])['time'].cumsum()
    # df_notes_c = df_notes_c.reset_index()
    df_notes_c['i_note'] = df_notes_c.groupby(['i_track', 'note', 'type']).cumcount()

    index_cols = ['i_track', 'note', 'i_note', 'channel']

    val_cols = ['t', 'velocity']


    df_wide = df_notes_c.pivot(
        index=index_cols,
        columns=['type'], 
        values=val_cols
    )

    # join 
    # https://stackoverflow.com/a/33290844
    df_wide.columns = ['_'.join(col).strip() for col in df_wide.columns.values]
    df_wide.reset_index(inplace=True)

    # df_wide = pd.DataFrame(df_wide.to_records(index=False))

    return df_wide


def pivot_notes_long(dfw):
    """
    Write :obj:`note_on` and :obj:`note_off` events in two lines (wide to long)

    :param dfw: Transforms notes in wide dataframe format to long format.
    :type dfw: :class:`~pandas.DataFrame`
    :return: Dataframe with twice the number of rows, where the time & velocity columns occur in two rows for all :obj:`note_on` or :obj:`note_off` events.
    :rtype: :class:`~pandas.DataFrame`
    """
    dfl = pd.wide_to_long(
        dfw, 
        ['t', 'velocity'], 
        ['i_track', 'note', 'i_note', 'channel'], 
        'type', 
        sep = '_', 
        suffix=r'note_o[nf]f?'
    ).reset_index().sort_values(['i_track', 't'])
    # dfl['time'] = dfl.groupby('i_track')['t'].diff().fillna(0).astype(int)
    dfl['meta'] = False
    # dfl = dfl.drop(['t', 'i_note'], axis=1)
    # dfl = dfl[['i_track', 'meta', 'type', 'time', 'note', 'velocity', 'channel']]
    dfl = dfl.reset_index(drop=True)
    return dfl

def add_abs_time(df):
    """
    Add a column of absolute time

    :param df: unnested midi frame
    :type df: :class:`~pandas.DataFrame`
    :return: Dataframe with absolute time column 't' added.
    :rtype: :class:`~pandas.DataFrame`
    """
    df_c = df.copy(deep = True)
    df_c['t']=df_c.groupby(['i_track'])['time'].cumsum()
    df_c = df_c.reset_index()
    return df_c


def merge_midi_frames(df_meta, df_not_notes, df_notes):
    """
    Merge dataframes resulting of :func:`split_midi_frame`.

      - :obj:`df_meta` - (containing all mido meta events), 
       - :obj:`df_not_notes` - (non-meta events that are not :obj:`note_on` or :obj:`note_off`) & 
       - :obj:`df_notes` - (all :obj:`note_on` or :obj:`note_off` events).

    :param df_meta: Contains all mido meta events.
    :type df_meta: :class:`~pandas.DataFrame`
    :param df_not_notes: Non-meta events that are not :obj:`note_on` or :obj:`note_off`.
    :type df_not_notes: :class:`~pandas.DataFrame`
    :param df_notes: All :obj:`note_on` or :obj:`note_off` events.
    :type df_notes: :class:`~pandas.DataFrame`
    :return: unnested midi frame
    :rtype: :class:`~pandas.DataFrame`
    """
    l_dfs = [df_meta, df_not_notes, df_notes]

    midi_fram_mod = pd.concat(l_dfs)
    midi_fram_mod
    midi_fram_mod = midi_fram_mod.sort_values(['i_track', 't'])
    midi_fram_mod['time'] = midi_fram_mod.groupby('i_track')['t'].diff().fillna(0).astype(int)
    cols = [
        'meta',
        'i_track',
        'type',
        'name',
        'time',
        'note',
        'velocity',
        'channel'
        'tempo',
        'numerator',
        'denominator',
        'clocks_per_click',
        'notated_32nd_notes_per_beat',
    ]
    return midi_fram_mod[cols]    