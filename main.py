import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
from gtts import gTTS
import pygame
import os
import time

Activation_word = "nonsense"

load_dotenv()
API_KEY = os.environ.get("api_key")

class NonSense_Bot:
    def __init__(self):
        self.r = sr.Recognizer()
        pygame.mixer.init()

    def speak(self, text):
        try:
            tts = gTTS(text=text, lang='en')
            filename = f"temp_voice_{int(time.time())}.mp3"
            tts.save(filename)
            
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            pygame.mixer.music.unload()
            os.remove(filename)
        except Exception as e:
            print(f"Speech error: {e}")

    

    def active_listen(self):
        with sr.Microphone() as mic:
            print("\nListening...")
            self.r.adjust_for_ambient_noise(mic, duration=0.5)
            audio = self.r.listen(mic)
            
            audio_text = "" 

            try:
                audio_text = self.r.recognize_google(audio).lower()
            except sr.UnknownValueError:
                print("Recognition failed: I didn't catch that.")
            except sr.RequestError:
                print("Network error: Check your internet.")
            
            return audio_text

    def listening(self):

        while True:
                audio_text = self.active_listen()

                try:

                    if Activation_word in audio_text:
                        print("System: Activation word detected!")
                        self.speak("System Activate, Nonsense-Bot here")
                        break
                    else:
                        pass

                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    print(f"Sorry error occurred: {e}")

    def reply(self):
        while True:
            said = self.active_listen()
            

    def run(self):
        while True:
            self.listening()
            self.reply()

def main():
    NS_bot = NonSense_Bot()
    NS_bot.run()


if __name__ == "__main__":
    main()