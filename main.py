from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QMessageBox
from form import Ui_MainWindow
from pyknon.music import Note,NoteSeq,Rest
from pyknon.genmidi import Midi
from annotated_turkish_syllables import get_syllables
from googletrans import Translator, constants
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from listen import play_music
import pygame
import nltk
import sys
import random

class App(QtWidgets.QMainWindow):

    def __init__(self):
        super(App,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.translator = Translator()

        self.ui.createbutton.clicked.connect(self.createMusic)
        self.ui.playbutton.clicked.connect(self.play_music)

    def play_music(self):
        if self.translate_and_analysis()<0.0:
            midi_file = 'midi/musicSad.midi'
        if self.translate_and_analysis()>0.0:
            midi_file = 'midi/musicActive.midi'

        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)

        # optional volume 0 to 1.0
        pygame.mixer.music.set_volume(0.8)
        try:
            play_music(midi_file)

        except KeyboardInterrupt:
            # if user hits Ctrl/C then exit
            # (works only in console mode)
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.stop()
            raise SystemExit

    # -1<x<1
    def translate_and_analysis(self):
        metin = self.ui.sentence.toPlainText()

        translation = self.translator.translate(metin, src='tr', dest='en')
        metin_eng = translation.text

        # analysis
        sid = SentimentIntensityAnalyzer()

        positive_or_negative = sid.polarity_scores(metin_eng)

        return float(positive_or_negative)

    # nota number
    def nota_number(self):
        metin = self.ui.sentence.toPlainText()
        # translation = self.translator.translate(metin, src='tr', dest='en')
        # metin_eng = translation.text
        syllables = get_syllables(u'{}'.format(metin))

        nota_n = 0
        for i in syllables:
            nota_n += 1

        return nota_n

    def active_nota(self, pitches, durations, rests=True):
        if rests:
            pitches.add('r')

        this_seq = ''

        for i in range(self.nota_number()):
            pitch = random.sample(pitches, 1)
            duration = random.sample(durations, 1)

            this_seq += pitch[0] + duration[0] + ' '

        return NoteSeq(this_seq).retrograde()

    def active_chord(self):

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
            if say == self.nota_number():
                break
        return chors

    def active_music(self):
        A_major = {
            "A", "B", "C", "D", "E", "F", "G"
        }

        dur = {
            "2", "4", "8", "16"
        }

        for i in range(self.nota_number()):
            midi = Midi(2, tempo=120, instrument=[40, 60])
            midi.seq_chords(self.active_chord(), track=0, time=0.5, channel=3)
            midi.seq_notes(self.active_nota(A_major, dur), track=0, channel=3, time=1)
            midi.write("midi/musicActive.midi")

    def sad_music(self):
        C_major = {
            "C", "B", "A", "D", "E", "F", "G"
        }

        dur = {
            "4", "8", "16"
        }

        for i in range(self.nota_number()):
            midi = Midi(2, tempo=60, instrument=[40, 60])
            midi.seq_chords(self.active_chord(), track=0, time=0.5, channel=3)
            midi.seq_notes(self.active_nota(C_major, dur), track=0, channel=3, time=1)
            midi.write("midi/musicSad.midi")

    def createMusic(self):
        if self.translate_and_analysis()>0.0:
            QMessageBox.information(self,"Created Music","\nOlumlu cümle girdiniz. Müzik başarıyla oluştruldu.\n")
            self.active_music()

        if self.translate_and_analysis()<0.0:
            QMessageBox.information(self, "Created Music", "\nNegatif cümle girdiniz. Müzik başarıyla oluştruldu.\n")
            self.sad_music()

def run():
    ap = QtWidgets.QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(ap.exec_())

run()