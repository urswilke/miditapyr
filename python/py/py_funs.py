# librosa:

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

# music21:

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


def get_midi_pitch_note_table():
    b=pandas.DataFrame({'pitch': range(128)})
    for i in range(128):
        a = note.Note()
        a.pitch.midi = i
        b.loc[i,"note"] = a
        b.loc[i,"octave"] = a.octave
        b.loc[i,"name"] = a.name
        b.loc[i,"nameWithOctave"] = a.nameWithOctave
         #following is necessary because otherwise, e.g.,  E-1 can have 2 meanings (E flat & octave: 1 or E & octave: -1)
        b.loc[i,"nameWithOctave_unique"] = ''.join(map(str, [b.loc[i,"name"].replace('-', 'b'), int(b.loc[i,"octave"])]))
    b.octave = b.octave.astype('int')
    return b


def music21_midi_df(mid):
    df = pandas.DataFrame()
    for i_track in range(len(mid.parts)):
        
        # i_track = 0
        c = list(mid.parts[i_track])
        c
        dfi = pandas.DataFrame({
            'i_track': i_track + 1,
            'event': c,
        #     'rest': [i.isRest for i in c]
        })
        dfi['meta'] = [all(x != "GeneralNote" for x in i.classes) for i in c]
        df = df.append(dfi)
        
    df = df.reset_index()
    df.loc[~df['meta'], 'rest'] = [i.isRest for i in df.loc[~df['meta'], 'event']]
    df.rest = df.rest.replace(np.NaN, False)

    note_events = ~df['rest'] & ~df['meta']
    chord_events = [isinstance(i, chord.Chord) for i in df.event]
    df.loc[note_events, 'notes'] = [list(i.pitches) for i in df.loc[note_events, 'event']]
    df.loc[note_events, 'midi'] = [list(p.midi for p in np.atleast_1d(i)) for i in df.loc[note_events, 'notes']]
    # df.loc['pitch_classes'] = ''
    df.loc[note_events, 'pitch'] = [list(p.nameWithOctave for p in np.atleast_1d(i)) for i in df.loc[note_events, 'notes']]
    # df.pitch_classes = df.pitch_classes.replace(np.NaN, '')

    # df.loc[note_events, 'pitch_classes'] = [[' '.join(str(p.nameWithOctave)) for p in i] for i in df.loc[note_events, 'notes']]
    df.loc[note_events, 'vel'] = [i.volume.velocity for i in df.loc[note_events, 'event']]
    df.loc[chord_events, 'type'] = [i.commonName for i in df.loc[chord_events, 'event']]
    df.loc[chord_events, 'quality'] = [i.quality for i in df.loc[chord_events, 'event']]
    df['offset'] = [i.offset for i in df['event']]
    df['dur'] = [i.duration.quarterLength for i in df['event']]
    df.offset = df.offset.astype('float')
    df.dur = df.dur.astype('float')
    return df



