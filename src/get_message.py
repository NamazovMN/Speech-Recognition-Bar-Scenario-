import os
from gtts import gTTS
import speech_recognition as sr


class Listen:
    """
    Class is utilized to set the configuration of the microphone
    """

    def __init__(self):
        """
        Method is utilized as an initializer of the class object
        """
        self.recognition = sr.Recognizer()
        self.mic = sr.Microphone()

    @staticmethod
    def speak(text: str) -> None:
        """
        Method is utilized to transform text to speech. It is used to deliver machine's messages to the user, verbally
        :param text: input text which is message from the machine to the user
        :return: None
        """
        speech_object = gTTS(text=text, lang="en", slow=False)
        speech_object.save("response.mp3")
        os.system("mpg321 response.mp3")

    def init_mic(self) -> None:
        """
        Method initializes the microphone and calibrates it according to the environment noise
        :return: None
        """
        print("Please wait, microphone is calibrating now. It will take 4 seconds.")
        print("You can speak after the beep sound.")
        self.speak("Please wait, microphone is calibrating now. It will take 4 seconds.")
        self.speak("You can speak after the beep sound!")
        with self.mic as source:
            self.recognition.adjust_for_ambient_noise(source, duration=4)
        os.system("mpg321 beep.mp3")

    def get_the_order(self, text: str) -> str:
        """
        Method is utilized for collecting the answer of the user of any kind (age, order or refusal)
        :param text: text which machine asks information to be provided
        :return: text script of the user
        """
        self.speak(text)

        speech_customer = None
        print('Please provide your order to microphone!')
        while not speech_customer:

            with self.mic as source:
                audio_customer = self.recognition.listen(source)

            try:
                speech_customer = self.recognition.recognize_google(audio_customer)
                break
            except sr.UnknownValueError:
                self.speak("Google Speech Recognition could not understand what you said!")
        return speech_customer
