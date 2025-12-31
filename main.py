import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time

Activation_word = "nonsense"

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

    def listening(self):

        def active_listen():
            with sr.Microphone() as mic:
                print("\nListening for 'nonsense'....")
                self.r.adjust_for_ambient_noise(mic, duration=0.5)
                audio = self.r.listen(mic)
                return audio

        while True:
                audio = active_listen()

                try:
                    audio_text = self.r.recognize_google(audio).lower()
                    print(f"Recognized: {audio_text}")

                    if Activation_word in audio_text:
                        print("System: Activation word detected!")
                        self.speak("How can I help you?")
                    else:
                        print(f"Repeating: {audio_text}")
                        self.speak(audio_text)

                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    print(f"Sorry error occurred: {e}")

def main():
    NS_bot = NonSense_Bot()
    NS_bot.listening()

if __name__ == "__main__":
    main()