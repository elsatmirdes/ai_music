from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from form import Ui_MainWindow
from pyknon.music import NoteSeq
from pyknon.genmidi import Midi
from annotated_turkish_syllables import get_syllables
from googletrans import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from listen import play_music
import pygame
import sys
import os
import random

class App(QtWidgets.QMainWindow):

    def __init__(self):
        super(App,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        if os.path.isdir("midi"):
            pass
        else:
            os.mkdir("midi")

        self.translator = Translator()

        self.ui.createbutton.clicked.connect(self.createMusic)
        self.ui.playbutton.clicked.connect(self.play_music)

    def play_music(self):
        location_file = str(os.getcwd())
        replace = location_file.replace("\\", "/")
        qmsgBox = QMessageBox()
        qmsgBox.setStyleSheet(f"background:url({replace}/images/bg.jpg); color: white;")

        pos_or_neg = self.translate_and_analysis()
        try:
            if pos_or_neg < 0.0:
                midi_file = 'midi/musicSad.midi'

            elif pos_or_neg > 0.0:
                midi_file = 'midi/musicActive.midi'

            elif pos_or_neg == 0.0:
                midi_file = "midi/nMusic.midi"

        except Exception:
            QMessageBox.critical(qmsgBox,"Error","Not found with play midi file")

        finally:
            pass

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
        # translate
        metin = self.ui.sentence.toPlainText() # cümle alınır
        translation = self.translator.translate(metin) # ingilizceye çevirilir
        metin_eng = translation.text

        # analysis
        sid = SentimentIntensityAnalyzer()
        positive_or_negative = sid.polarity_scores(metin_eng)

        return positive_or_negative # -1 ile 1 arasında değer döndürür (float)

    # nota number - kaç nota ve akordan oluşmasını belirler (cümleyi hecelerine ayırır ve hece kadar nota akor döndürür)
    def nota_number(self):
        metin = self.ui.sentence.toPlainText()
        syllables = get_syllables(u'{}'.format(metin))

        nota_n = 0
        for n in syllables:
            nota_n += 1

        return nota_n

    def nota(self, pitches, durations, rests=True):
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
            "A4 C4 E4",  # Am
            "A2 D2 F2",  # Dm
            "B B2 G2 B4 E",  # Em
            "G4 B4 D4",  # G
            "F4 A4 C4",  # F
            "G4 C4 E4",  # C
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

    def sad_chord(self):
        chors = []
        chords = [
            "A8 C8 E8",  # Am
            "A8 D8 F8",  # Dm
            "B B2 G2 B4 E",  # Em
            "G8 B8 D8",  # G
            "F2 A2 C2",  # F
            "G4 C4 E4",  # C
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

        if self.translate_and_analysis() > 0.0 or self.translate_and_analysis() < 0.3000:
            tempo = 120

        if self.translate_and_analysis() > 0.4000 or self.translate_and_analysis() < 0.5000:
            tempo = 140

        if self.translate_and_analysis() > 0.5000:
            tempo = 160

        for i in range(self.nota_number()):
            midi = Midi(2, tempo=tempo, channel=[0,9], instrument=[20,40,60])
            midi.seq_notes(self.nota(A_major,dur), track=0, channel=2)
            midi.seq_notes(self.nota(A_major,dur), track=1, channel=9)
            # midi.seq_chords(self.active_chord(), track=0, channel=1)
            midi.seq_chords(self.active_chord(), track=0, channel=1)
            midi.write("midi/musicActive.midi")

        print(tempo)

    def sad_music(self):
        C_major = {
            "C", "B", "A", "D", "E", "F", "G"
        }

        dur = {
            "4", "8", "16"
        }
        time = 0

        if self.translate_and_analysis() < 0.0 or self.translate_and_analysis() > -0.2000:
            tempo = 60

        if self.translate_and_analysis() < -0.3000 or self.translate_and_analysis() > -0.4000:
            tempo = 50

        if self.translate_and_analysis() <= -0.5000:
            tempo = 40

        for i in range(self.nota_number()):
            midi = Midi(2, tempo=tempo, instrument=[40, 60])
            midi.seq_chords(self.sad_chord(), track=0, channel=3)
            midi.seq_notes(self.nota(C_major, dur), track=0, channel=1)
            midi.seq_notes(self.nota(C_major, dur), track=1, channel=2)
            midi.write("midi/musicSad.midi")
            time += 1
        print(tempo)

    def notr_music(self):
        C_major = {
            "C", "B", "A", "D", "E", "F", "G"
        }

        dur = {
            "2", "4", "8", "16"
        }

        time = 0
        for i in range(self.nota_number()):
            midi = Midi(2, tempo=80, instrument=[40, 60])
            midi.seq_chords(self.sad_chord(), track=0, channel=3)
            midi.seq_notes(self.nota(C_major, dur), track=0, channel=3)

            midi.write("midi/nMusic.midi")
            time += 1

    def createMusic(self):
        location_file = str(os.getcwd())
        replace = location_file.replace("\\", "/")
        qmsgBox = QMessageBox()
        qmsgBox.setStyleSheet(f"background:url({replace}/images/bg.jpg); color: white;")


        analiz_sonucu = self.translate_and_analysis()

        if analiz_sonucu > 0.0:
            QMessageBox.information(qmsgBox,"Created Music","\nPozitif (+) cümle girdiniz. Müzik başarıyla oluştruldu.\n")
            self.active_music()

        elif analiz_sonucu < 0.0:
            QMessageBox.information(qmsgBox, "Created Music", "\nNegatif (-) cümle girdiniz. Müzik başarıyla oluştruldu.\n")
            self.sad_music()

        elif analiz_sonucu == 0.0:
            QMessageBox.information(qmsgBox, "Created Music", "\nNötr cümle girdiniz. Müzik başarıyla oluşturuldu\n")
            self.notr_music()

        else:
            QMessageBox.information(qmsgBox,"Could not be created","\nMüzik Oluşurulamadı\n")

def run():
    ap = QtWidgets.QApplication(sys.argv)
    win = App()
    win.setFixedSize(404,419) # pencere boyutlandırma işlemi kapatıldı
    win.show()
    sys.exit(ap.exec_())


if __name__ == "__main__":
    run()