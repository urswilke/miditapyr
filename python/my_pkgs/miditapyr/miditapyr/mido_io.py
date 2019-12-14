# mido:

def mido_midi_df(mid):
    l = []
    m = []
    for i, track in enumerate(mid.tracks):
        for msg in track:
            l.append(vars(msg))
            m.append(msg.is_meta)
    df = pandas.DataFrame(l)
    df['meta'] = m
    df['name'] = df['name'].astype('str')
    # df['time_s'] = mido.tick2second(df['time'])
    df['i_track'] = np.cumsum(df['type'].str.contains('track_name'))
    df_meta = df.query('meta').dropna(how = 'all', axis = 1).drop('meta', axis=1)
    df_notes = df.query('not meta').dropna(how = 'all', axis = 1).drop('meta', axis=1)
    
    return df_meta, df_notes, mid.ticks_per_beat


def df2mido_midifile(df, ticks_per_beat):
    from mido import MetaMessage, Message, MidiFile, MidiTrack

    outfile = MidiFile(ticks_per_beat=ticks_per_beat)
    
    track = MidiTrack()
    # track.append(Message('program_change', program=12))
    
    for i in range(len(df)):
        # meta messages:
        if df.loc[i, 'type'] == 'track_name':
            track = MidiTrack()
            outfile.tracks.append(track)
        elif df.loc[i, 'type'] == 'set_tempo':
            track.append(MetaMessage('set_tempo', tempo = df.loc[i, 'tempo'].astype(int)))
        elif df.loc[i, 'type'] == 'time_signature':
            track.append(MetaMessage('time_signature',
                                 numerator = df.loc[i, 'numerator'].astype(int), 
                                 denominator = df.loc[i, 'denominator'].astype(int)))#, 
    #                              clocks_per_click = df.loc[i, 'clocks_per_click'], 
    #                              notated_32nd_notes_per_beat = df.loc(i, 'notated_32nd_notes_per_beat')))
        elif df.loc[i, 'type'] == 'note_on':
            track.append(Message('note_on', 
                                 note=df.loc[i, 'note'].astype(int), 
                                 velocity=df.loc[i, 'velocity'].astype(int), 
                                 channel=df.loc[i, 'channel'].astype(int), 
                                 time=df.loc[i, 'time'].astype(int)))
        elif df.loc[i, 'type'] == 'note_off':
            track.append(Message('note_off', 
                                 note=df.loc[i, 'note'].astype(int), 
                                 velocity=df.loc[i, 'velocity'].astype(int), 
                                 time=df.loc[i, 'time'].astype(int)))
    return outfile

def df2mido_midifile(df_meta, df_notes, ticks_per_beat):
    from mido import MetaMessage, Message, MidiFile, MidiTrack
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


