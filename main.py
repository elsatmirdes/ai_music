from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QMessageBox
from form import Ui_MainWindow
from pyknon.music import NoteSeq
from pyknon.genmidi import Midi
from annotated_turkish_syllables import get_syllables
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from listen import play_music
from google_trans_new import google_translator
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

        self.ui.createbutton.clicked.connect(self.createMusic)
        self.ui.playbutton.clicked.connect(self.play_music)
        self.ui.extractAction.triggered.connect(self.exit)
        self.ui.listen_pos.triggered.connect(self.listen_pozitif)
        self.ui.listen_notr.triggered.connect(self.listen_notr)
        self.ui.listen_neg.triggered.connect(self.listen_negatif)


    def play_music(self):
        pos_or_neg = self.translate_and_analysis()
        try:
            if pos_or_neg < 0.0:
                midi_file = 'midi/musicSad.midi'

            elif pos_or_neg > 0.0:
                midi_file = 'midi/musicActive.midi'

            elif pos_or_neg == 0.0:
                midi_file = "midi/nötrMusic.midi"

        except TypeError:
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

        except UnboundLocalError:
            location_file = str(os.getcwd())
            replace = location_file.replace("\\", "/")
            qmsgBox = QMessageBox()

            qmsgBox.setStyleSheet("background:rgb(207,179,255,0.9);\ncolor:black;\nfont: 75 10pt 'MS Shell Dlg 2';\nQPushButton{background-color: blue;}")
            qmsgBox.setWindowIcon(QtGui.QIcon(f"{replace}/images/indir.png"))

            QMessageBox.critical(qmsgBox, "Error", "\nMüzik oynatılırken hata oluştu\nOluşturulan müzik oynatılır. Önce müzik oluştur.\n")

    # -1<x<1
    def translate_and_analysis(self):
        translator = google_translator()
        try:
            # translate
            metin = self.ui.sentence.toPlainText() # cümle alınır
            translate = translator.translate(metin)

            # analysis
            sid = SentimentIntensityAnalyzer()
            positive_or_negative = sid.polarity_scores(translate).get("compound")

            return positive_or_negative  # -1 ile 1 arasında değer döndürür (float)

        except Exception:
            location_file = str(os.getcwd())
            replace = location_file.replace("\\", "/")
            qmsgBox = QMessageBox()

            qmsgBox.setStyleSheet("background:rgb(207,179,255,0.9);\ncolor:black;\nfont: 75 10pt 'MS Shell Dlg 2';\nQPushButton{background-color: blue;}")
            qmsgBox.setWindowIcon(QtGui.QIcon(f"{replace}/images/indir.png"))


            QMessageBox.critical(qmsgBox, "Error", "\nMüzik oluştururken hata oluştu. İnternet bağlantınızı kontrol edin\n")

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
            "A2 D2 F2",  # Dm
            "B4 B4 G4 B4 E2",  # Em
            "G4 B4 D4",  # G
            "F4 A4 C4",  # F
            "G4 C4 E4",  # C
            "G2 B2 E2"  # B
        ]


        say = 0
        while True:
            r = random.randint(0, 6)
            nota_add = NoteSeq(chords[r]).retrograde()
            chors.append(nota_add)
            say += 1
            if say == self.nota_number():
                chors.append(NoteSeq("F2 A2 C2"))
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
            midi.write(f"midi/musicActive.midi")

        print(tempo)

    def sad_music(self):
        C_major = {
            "A", "B", "C", "D", "E", "F"
        }

        dur = {
            "4", "8", "16"
        }


        if self.translate_and_analysis() < 0.0 or self.translate_and_analysis() > -0.2000:
            tempo = 60

        if self.translate_and_analysis() < -0.3000 or self.translate_and_analysis() > -0.4000:
            tempo = 50

        if self.translate_and_analysis() <= -0.5000:
            tempo = 40
        time = 0
        for i in range(self.nota_number()):
            midi = Midi(2, tempo=tempo,channel=[0,9], instrument=[40, 60])
            midi.seq_chords(self.sad_chord(), track=0, channel=3)
            midi.seq_notes(self.nota(C_major, dur), track=0, channel=1)
            # midi.seq_notes(self.nota(C_major, dur), track=1, channel=2)
            midi.write("midi/musicSad.midi")
            time += 1

        print(self.sad_chord()[-1])
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

            midi.write("midi/nötrMusic.midi")
            time += 1

    def listen_pozitif(self):
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)

        # optional volume 0 to 1.0
        pygame.mixer.music.set_volume(0.8)
        play_music("midi/musicActive.midi")

    def listen_notr(self):
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)

        # optional volume 0 to 1.0
        pygame.mixer.music.set_volume(0.8)
        play_music("midi/nötrMusic.midi")

    def listen_negatif(self):
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)

        # optional volume 0 to 1.0
        pygame.mixer.music.set_volume(0.8)
        play_music("midi/musicSad.midi")

    def createMusic(self):
        location_file = str(os.getcwd())
        replace = location_file.replace("\\", "/")
        qmsgBox = QMessageBox()

        qmsgBox.setStyleSheet("background:rgb(207,179,255,0.9);\ncolor:black;\nfont: 75 10pt 'MS Shell Dlg 2';\nQPushButton{background-color: blue;}")
        qmsgBox.setWindowIcon(QtGui.QIcon(f"{replace}/images/indir.png"))

        analiz_sonucu = self.translate_and_analysis()
        try:
            if analiz_sonucu > 0.0:
                QMessageBox.information(qmsgBox,"Created Music","\nPozitif (+) cümle girdiniz. Müzik başarıyla oluşturuldu.\n")
                self.active_music()
            elif analiz_sonucu < 0.0:
                QMessageBox.information(qmsgBox, "Created Music", "\nNegatif (-) cümle girdiniz. Müzik başarıyla oluşturuldu.\n")
                self.sad_music()
            elif analiz_sonucu == 0.0:
                QMessageBox.information(qmsgBox, "Created Music", "\nNötr cümle girdiniz. Müzik başarıyla oluşturuldu\n")
                self.notr_music()
        except TypeError:
            pass

    def exit(self):
        QtWidgets.qApp.quit()

def run():
    ap = QtWidgets.QApplication(sys.argv)
    win = App()
    win.setFixedSize(404,419) # pencere boyutlandırma işlemi kapatıldı
    win.show()
    sys.exit(ap.exec_())


if __name__ == "__main__":
    run()
