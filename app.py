from pyknon.music import Note,NoteSeq,Rest
from pyknon.genmidi import Midi
import random
import os


def random_music(n,pitches,durations,rests=True):
    if rests:
        pitches.add('r')

    this_seq = ''

    for i in range(n):
        pitch = random.sample(pitches, 1)
        duration = random.sample(durations, 1)

        this_seq += pitch[0] + duration[0] + ' '

    return NoteSeq(this_seq).retrograde()

def get_chord(n):

    chors = []
    chords = [
        "A C2 E2",  # Am
        "A2 D F2",  # Dm
        "B B2 G2 B4 E",  # Em
        "G B2 D2",  # G
        "F A2 C2",  # F
        "G2 C E2",  # C
        "G2 B E2"  # B
    ]

    say = 0
    while True:
        r = random.randint(0, 6)
        nota_add = NoteSeq(chords[r]).retrograde()
        chors.append(nota_add)
        say += 1
        if say == n:
            break
    return chors

def perkusyon():
    A_major = {
        "A","B","C","D","E","F","G"
    }

    C_major = {
        "C","A","D","E","G","B","F"
    }

    dur = {
        "2","4","8","16"
    }

    for i in range(10):
        midi = Midi(2, tempo=90, instrument=[40, 60])
        midi.seq_chords(get_chord(10), track=0,time=0.5,channel=3)
        midi.seq_notes(random_music(10,A_major,dur),track=0,channel=3,time=1)
        midi.write("midi/midi_per.midi")

perkusyon()