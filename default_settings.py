# Default settings class which is used for speech recognition settings, such as
# @ microphone setting and initialization
# @ getting the message from the user, which is used for taking orders
# @ speech generator function for generating the speech from the text.
# 
# Designed by Mahammad Namazov
# 24.02.2020

from gtts import gTTS
import os
import pyaudio
import random
import spacy
import speech_recognition as sr

class Settings(object):

    def __init__(self, microphone, recognizer, language):
        self.microphone = microphone
        self.recognition = recognizer
        self.language = language

    # initialization of the microphone
    def init_mic(self):
        print("Please wait, microphone is callibrating now. It will take 4 seconds.")
        print("You can speak after the beep sound.")
        with self.microphone as source:
            self.recognition.adjust_for_ambient_noise(source, duration=4)
        os.system("mpg321 beep.mp3")
    
    # it is used getting the order from the user
    def get_the_message(self):
        self.init_mic()
        speech_customer = ''
        with self.microphone as source:
            audio_customer=self.recognition.listen(source)
        try:
            speech_customer = self.recognition.recognize_google(audio_customer)
            return speech_customer
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand what you said!")
        except sr.RequestError as e:
            print("Could not request results from Google SRS; {0}".format(e))

    # it is used for transforming sentences (texts) to the speech
    def speech_generator(self, response):
        speech_object = gTTS(text = response, lang = self.language, slow = False)
        speech_object.save("response.mp3")
        os.system("mpg321 response.mp3")