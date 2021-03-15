
import pyttsx3


# pyttsx3 settings

engine = pyttsx3.init()

rate = engine.getPropoerty('rate')
engine.setProperty('rate', 150)

engine.getProperty('volume')
engine.setProperty('volume', 1.5)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# play

mila_speech =  ""

engine.say(mila_speech)

# play
#engine.save_to_file(mila_speech, './φ/mila/2-Intel.mp3')
engine.runAndWait()

