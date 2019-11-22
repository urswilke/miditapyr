def get_predominant_note(C_chroma):
    df_note_indices = pandas.DataFrame({'index': C_chroma.argmax(axis=0)})
    # df_note_indices
    
    letters = [ascii_uppercase for _ in range(12)]
    df_notes = pandas.DataFrame({
        'index': list(range(12)),
        'note': librosa.hz_to_note(440.0 * (2.0 ** np.linspace(3/12, 1+2/12, 12)), octave=False)
        }
    )
    res = pandas.merge(df_note_indices, df_notes, how='left', on=['index'])
    return(res)


from music21 import *
import pandas
import numpy as np
def get_element_list(parts):
    notes_for_instruments = []
    for i in range(len(parts.parts)):
        instruments = []
        notes_to_parse = parts.parts[i].recurse()
        instr = parts.parts[i].getInstrument()
        instruments.append(instr.instrumentName)
        notes, quarters = [],[] 
        for element in notes_to_parse:   
            if isinstance(element, note.Note):  
        # if element is a note, extract pitch   
                notes.append(str(element.pitch.name))
            # notes.append(str(element.duration.quarternotes))
            elif(isinstance(element, chord.Chord)):  
            # if element is a chord, append the normal form of the   
            # chord (a list of integers) to the list of notes.   
                notes.append(' '.join(str(n.pitch.name) for n in element.notes))  
            elif isinstance(element, note.Rest):
                notes.append('Rest')
    notes_for_instruments.append(notes)
    return(notes_for_instruments)
    
def get_element_durs(parts):
    durs_for_instruments = []
    for i in range(len(parts.parts)): 
        instruments = []
        notes_to_parse = parts.parts[i].recurse()
        instr = parts.parts[i].getInstrument()
        instruments.append(instr.instrumentName)
        notes, quarters = [],[] 
        for element in notes_to_parse:   
            if isinstance(element, note.Note) | isinstance(element,chord.Chord) | isinstance(element, note.Rest):  
        # if element is a note, extract pitch   
                notes.append(str(element.duration.quarterLength))
        durs_for_instruments.append(notes)
    return(durs_for_instruments)


def get_midi_df(midi):
    parts = instrument.partitionByInstrument(midi.chordify()) 
    df_mid = pandas.DataFrame({
        'notes': get_element_list(parts)[0], 
        'dur': get_element_durs(parts)[0]
        }
    )
    df_mid['dur'] = df_mid['dur'].astype('float')
    df_mid['endtime'] = np.cumsum(df_mid.dur)
    df_mid['begintime'] = df_mid['endtime'] - df_mid['dur']
    return(df_mid)


def get_df_midi(midi):
    notes_for_instruments = []
    res = pandas.DataFrame()
    for i in range(len(midi.parts)):
        instruments = []
        durs = []
        velocity = []
        offset = []
        pitches = []
        notes, quarters = [],[]
        notes_to_parse = midi.parts[i].recurse()
        instr = midi.parts[i].getInstrument()
        instruments.append(instr.instrumentName)
        for element in notes_to_parse:
            if isinstance(element, note.Note):
        # if element is a note, extract pitch
                notes.append(str(element.pitch.name))
                velocity.append(str(element.volume.velocity))
                durs.append(element.duration.quarterLength)
                offset.append(element.offset)
                pitches.append(element.pitch.midi)
            # notes.append(str(element.duration.quarternotes))
            elif(isinstance(element, chord.Chord)):
            # if element is a chord, append the normal form of the
            # chord (a list of integers) to the list of notes.
                notes.append(' '.join(str(n.pitch.name) for n in element.notes))
                velocity.append(str(element.volume.velocity))
                durs.append(element.duration.quarterLength)
                offset.append(element.offset)
                pitches.append(' '.join([str(p.midi) for p in element.pitches]))
            elif isinstance(element, note.Rest):
                notes.append('Rest')
                velocity.append('nan')
                durs.append(element.duration.quarterLength)
                offset.append(element.offset)
                pitches.append(np.nan)
#     notes_for_instruments.append(notes)
        res_i = pandas.DataFrame(
            {
                'instr': i,
                'note': notes,
                'pitch': pitches,
                'dur': [float(i) for i in durs],
                'vel': [float(i) for i in velocity],
                'offset': [float(i) for i in offset]
            }
        )
        res = pandas.concat([res, res_i])
    return(res)


def explode_chords_df(df_mid):
    df_expl = df_mid.assign(notes=df_mid['notes'].str.split(' ')).explode('notes')
    return(df_expl)


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

def get_midi_pitch_note_table():
    b=pandas.DataFrame({'pitch': range(128)})
    for i in range(128):
        a = note.Note()
        a.pitch.midi = i
        b.loc[i,"note"] = a
        b.loc[i,"name"] = a.name
        b.loc[i,"nameWithOctave"] = a.nameWithOctave
    return b

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
