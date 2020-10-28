from pyknon.music import Note,NoteSeq,Rest
from pyknon.genmidi import Midi
import random
import os


# C_note = Note(0, 5, dur=0.25)
#
# quarter_rest = Rest(0.25) # quarter rest
#
# A_note = Note(9, 5, 0.25)
#
# seq = NoteSeq([C_note, A_note, quarter_rest, C_note]) # Nota eklemek için
#
#
# midi = Midi(1, tempo=120)
# midi.seq_notes(seq, track=0)
# midi.write("simple_noteseq.mid")

def get_random_note_seq(n, pitches, durations, rests=True):
    # Add a rest to the set of pitches if desired.
    if rests:
        pitches.add('r')

    this_seq = ''

    for i in range(n):
        pitch = random.sample(pitches, 1)
        duration = random.sample(durations, 1)
        this_seq += pitch[0] + duration[0] + ' '

    return NoteSeq(this_seq)

durations = {
    "2", # half note
    "4", # quarter note
    "8", # eighth note
    "16" # sixteenth note
}

A_major = {
    'A',
    'B',
    'C#',
    'D',
    'E',
    'F#',
    'G#'
}


notes_A_major = get_random_note_seq(128, A_major, durations)
midi = Midi(1, tempo=120)
midi.seq_notes(notes_A_major, track=0)
midi.write("A_major01.mid")

