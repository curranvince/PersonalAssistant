import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import time
import wikipedia
import pyjokes
import webbrowser
import os

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[17].id)

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)
        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")
        except Exception as e:
            say("Pardon me, please say that again")
            return "No command"
        return statement

def executeCommand(command):
    keywords = [ ['bye','sleep'],
        ['time'],
        ['Wikipedia', 'pedia'],
        ['open'],
        ['search'],
        ['joke'],
        ['play', 'Play']]
    if any(x in command for x in keywords[0]):
        exit()
    elif any(x in command for x in keywords[1]):
        TimeCommand().execute()
    elif any(x in command for x in keywords[2]):
        WikiCommand().execute(command)
    elif any(x in command for x in keywords[3]):
        OpenCommand().execute(command)
    elif any(x in command for x in keywords[4]):
        SearchCommand().execute(command)
    elif any(x in command for x in keywords[5]):
        JokeCommand().execute()
    elif any(x in command for x in keywords[6]):
        MusicCommand().execute(command)

def run():
    executeCommand(takeCommand())

class Command():
   def execute(self):
       raise NotImplementedError("Method not implemented")

class TimeCommand(Command):
    def execute(self):
        time = datetime.datetime.now().strftime('%I:%M %p')
        say('Time is ' + time)

class GreetingCommand(Command):
    def execute(self):
        hour=datetime.datetime.now().hour
        if hour>=0 and hour<12:
            say("Good Morning, master")
        elif hour>=12 and hour<18:
            say("Good Afternoon, master")
        else:
            say("Good Evening, master")

class WikiCommand(Command):
    def execute(self, statement):
        statement = statement.replace("Wikipedia", "")
        statement = statement.replace("pedia", "")
        results = wikipedia.summary(statement, sentences=3)
        say("According to Wikipedia" + results)

class OpenCommand(Command):
    def execute(self, statement):
        if 'Google' in statement:
            webbrowser.open("https://www.google.com", 1)
            say("Your tab is open, master")
        elif 'YouTube' in statement:
            webbrowser.open("https://www.youtube.com", 1)

class SearchCommand(Command):
    def execute(self, statement):
        statement = statement.replace("search", "")
        pywhatkit.search(statement)
        say("Your tab is open, master")

class JokeCommand(Command):
    def execute(self):
        say(pyjokes.get_joke())

class MusicCommand(Command):
    def execute(self, statement):
        song = statement.replace("play", "")
        pywhatkit.playonyt(song)   

GreetingCommand().execute()
while True:
    run()