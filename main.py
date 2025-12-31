import speech_recognition as sr
import pyttsx3

class NonSense_Bot:

    def __init__(self):
        self.r = sr.Recognizer()
    
    def listening(self):
        with sr.Microphone() as mic:
            print("Listening....")
            self.r.adjust_for_ambient_noise(mic, duration=1)
            audio_text = self.r.listen(mic)
            print("Done")

            try:
                return audio_text
            except Exception as e:
                print(f"Sorry error occured.\n\n{e}")
    
    

def main():
    NS_bot = NonSense_Bot()
    NS_bot.listening()
    return 0

if __name__ == "__main__":
    main()