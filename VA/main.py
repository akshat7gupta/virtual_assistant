import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import smtplib
import sys
import pyjokes
#import youtube
import urllib.parse
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from plutoMP import Ui_MainWindow


engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[0].id)
newVoiceRate = 150
engine.setProperty('rate', newVoiceRate)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<=12:
        speak("good morning")
    elif hour>12 and hour<18:
        speak("good afternoon")
    else:
        speak("Rom Rom bhaaiyoo")
    speak(" I am pluto, please tell how may i help you")


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    # Enable low security in gmail
    server.login('anku32373@gmail.com', 'ollboxgcedqcvtge')
    server.sendmail('anku32373@gmail.com', to, content)
    server.close()

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("recognizing...")
            self.query = r.recognize_google(audio, language='eng-in')
            print(f"user said:{self.query}")

        except Exception as e:
             speak("I couldn't recognize what you said, please repeat...")
             return'none'
        return self.query


    def TaskExecution(self):
        wish()
        while True:

            self.query = self.takecommand().lower()

            #logic building for tasks

            if "time" in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"the time is {strTime}")

            elif "notepad" in self.query:
                speak("Opening notepad")
                bpath = "C:\\WINDOWS\\system32\\notepad.exe"
                os.startfile(bpath)

            elif "open chrome" in self.query:
                apath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                speak("What should I search")
                search = self.takecommand().lower()
                speak("searching...")
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(apath))
                webbrowser.get('chrome').open(f"{search}.com")

            elif "open command prompt" in self.query:
                speak("opening command prompt...")
                os.system("start cmd")

            elif "date" in self.query:
                year = int(datetime.datetime.now().year)
                month = int(datetime.datetime.now().month)
                date = int(datetime.datetime.now().day)
                speak(f"Today is {date} {month} {year}")

            elif "camera" in self.query:
                speak("opening camera...")
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()

            elif "music" in self.query:
                speak("playing music...")
                music_dir = "C:\\Users\\aksha\\music"
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir, rd))

            elif "ip address" in self.query:
                ip = get('http://api.ipify.org').text
                speak(f"your IP address is {ip}")

            elif "wikipedia" in self.query:
                speak("searching wikipedia...")
                self.query = self.query.replace("wikipedia","")
                results = wikipedia.summary(self.query, sentences=2)
                speak("according to wikipedia")
                speak(results)
                print(results)


            elif "youtube" in self.query:
                speak("opening YouTube")
                self.query = self.query.replace("youtube", "").strip()  # Remove 'youtube' from query
                search_query = urllib.parse.quote(self.query)
                url = f"https://www.youtube.com/results?search_query={search_query}"
                webbrowser.open(url)

            elif "video conference" in self.query:
                speak("starting video conference...")
                self.video_conference()

            elif "open google" in self.query:
                speak("what should i search on google")
                cm = self.takecommand().lower()
                webbrowser.open(f"{cm}")

            elif 'joke' in self.query:
                speak(pyjokes.get_joke())

            elif "send mail" in self.query:
                try:
                    speak("what should i say?")
                    content = self.takecommand().lower()
                    to = "akshat7.0gupta@gmail.com"
                    sendEmail(to,content)
                    speak("email sent!")

                except Exception as e:
                    print(e)
                    speak("I am not able to send this email")

            elif "log out" in self.query:
                os.system("shutdown - l")
                speak("Do you wish to logout of your computer ? (yes or no): ")
                ansl = self.takecommand().lower()
                if 'yes' in ansl:
                    os.system("shutdown - l")
                else:
                    exit()

            elif "shut down pc" in self.query:
                speak("Do you wish to shutdown your computer ? (yes or no): ")
                ans = self.takecommand().lower()
                if 'yes' in ans:
                    os.system("shutdown /s /t 1")
                else:
                    exit()

            elif "restart" in self.query:
                speak("Do you wish to restart your computer ? (yes or no): ")
                ansr = self.takecommand().lower()
                if 'yes' in ansr:
                    speak("shutting down")
                    os.system("shutdown /r /t 1")
                else:
                    speak("okay")
                    exit()

            elif "write a note" in self.query:
                speak("What should i write")
                note = self.takecommand()
                file = open('mynotes.txt', 'w')
                speak(" Should i include date and time")
                snfm = self.takecommand()
                if 'yes' in snfm:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    file.write(strTime)
                    file.write(" :- ")
                    file.write(note)
                else:
                    file.write(note)

            elif "reminder" in self.query:
                speak("what should I remember?")
                data = self.takecommand()
                speak("you told me to remember " + data)
                rem = open("data.txt", "w")
                rem.write(data)
                rem.close()

            elif "do you know anything" in self.query:
                rem = open("data.txt", "r")
                speak("you said me to remember that " + rem.read())

            elif "show my notes" in self.query:
                speak("Showing Notes")
                file = open("mynotes.txt", "r")
                speak("here are your notes. "
                      "" + file.read())

            elif "stop" in self.query:
                speak("thanks for using me, Happy to help! have a good day")
                sys.exit()


            speak("do you want me to do anything else")


startExe = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.StartTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def StartTask(self):
        self.ui.movie = QtGui.QMovie(":/newPrefix/ebbdf7ce4f7f502d1f28b96b5cbd7a1f.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("MetallicNegativeBobolink-max-1mb.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("Phone_Booth_03_prores_v008.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("MeekPlayfulIbizanhound-max-1mb.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(200000)

        startExe.start()

    def showTime(self):

        while True:
          #   QApplication.processEvents()
          #  dt = datetime.datetime.now()
           # self.textBrowser.setText('Date:- %s:%s:%s' % (dt.day, dt.month, dt.year))
            #self.textBrowser_3.setText('Date:- %s:%s:%s' % (dt.day, dt.month, dt.year))
            t_ime = QTime.currentTime()
            d_ate = QDate.currentDate()
            time = t_ime.toString()
            date = d_ate.toString()
            label_time = "Time :" + time
            label_date = "Date : " + date
            self.ui.textBrowser.setText(label_date)
            self.ui.textBrowser_3.setText(label_time)

app = QApplication(sys.argv)
pluto = Main()
pluto.show()
exit(app.exec_())





