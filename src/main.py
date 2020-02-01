
import sys
from time import sleep
from playsound import playsound

from PyQt5 import uic
from PyQt5.Qt import QApplication, QMainWindow
from PyQt5.QtCore import QRegExp, QThread, pyqtSignal
from PyQt5.QtGui import QRegExpValidator

class counterTimer(QThread):
    # Imposta un segnale per il thread
    signal = pyqtSignal(str)

    def __init__(self, inizioTime, loop):
        super(counterTimer, self).__init__()
        # Inizializza le variabili per il countdown
        self.inizioTime = inizioTime
        self.loop = loop
        self.nextiter = True

    def stopTime(self):
        #Funzione per stoppare tutti i loop
        self.loop = False
        self.nextiter = False

    def run(self):
        # primo loop per eseguirlo solo 1 volta
        for x in range(self.inizioTime):
            if not self.nextiter:
                break
            # Invia il nuovo numero da scrivere sullo schermo
            self.signal.emit(str(self.inizioTime-x))
            # Attende 1 secondo
            sleep(1)
        # Se il for NON è uscito con un break (uscita forzata)
        if self.nextiter:
            # Esegui il suono
            playsound('audio.mp3')

        # Se l'utente vuole infiniti loop allora dal secondo loop esegue questo while
        while(self.loop):
            for x in range(self.inizioTime):
                if not self.nextiter:
                    break
                self.signal.emit(str(self.inizioTime-x))
                sleep(1)
            if self.nextiter:
                playsound('audio.mp3')

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Dichiarazione della variabile per il thread
        self.thread_time = None
        # Carica .ui ed esegui la funzione self.mainWin()
        self.changeScreen("mainWin.ui",self.mainWin)

    def changeScreen(self, fileUi, nextFunct=""):
        # Memorizza la funzione da chiamare
        self.__nextFunct = nextFunct
        # Carica file ui
        uic.loadUi(fileUi, self)
        # Se la funzione successiva è impostata chiamala
        if self.__nextFunct != "":
            self.__nextFunct()
        # Mostra GUI
        self.show()

    def editTime(self, time):
        # Sovrascrive quello che c'è scritto sul widget
        self.lcdNumber.display(time)

    def startTime(self):
        # Controlla se il thread è attivo
        try:
            contatore_attivo = self.thread_time.isRunning()
        except AttributeError:
            contatore_attivo = False

        # Se è stato inserito un numero corretto  e il thread è spento
        if self.delayTimer.text() != "" and not contatore_attivo:
            # crea un thread con il tempo indicato (self.delayTimer.text()) e se deve andare in loop (self.loopTimer.checkState())
            self.thread_time = counterTimer(int(self.delayTimer.text()), self.loopTimer.checkState())
            # Collega i segnali del thread alla funzione che modifica il numero visualizzato
            self.thread_time.signal.connect(self.editTime)
            # Avvia il thread
            self.thread_time.start()

    def stopTime(self):
        # Se il thread è attivo esegue la funzione per disattivare il thread
        try:
            self.thread_time.stopTime()
        except AttributeError:
            pass

    #Main Load
    def mainWin(self):
        # Filtra l'input per il tempo
        self.delayTimer.setValidator(QRegExpValidator(QRegExp(r"[0-9]+")))
        # Collega i puldanti per le rispettive funzioni
        self.startTimer.clicked.connect(lambda: self.startTime())
        self.stopTimer.clicked.connect(lambda: self.stopTime())
        
# Start
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
