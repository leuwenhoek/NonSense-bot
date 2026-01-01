import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
from gtts import gTTS
import pygame
import os
import time
import json

Activation_word = "nonsense"

load_dotenv()
API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

class Config:
        def __init__(self):
            self.folder_name = "config"
            self.Instruction_path = os.path.join(self.folder_name, "Instruction.json")
            self.Memory_path = os.path.join(self.folder_name, "Memory.json")
            pass

        def locate(self):
            if not os.path.exists(self.folder_name):
                os.makedirs(self.folder_name)

            if os.path.exists(self.Instruction_path) or not os.path.exists(self.Instruction_path):
                default_settings = {
                        "bot_info": {
                            "name": "NonSense-bot",
                            "gender_persona": "female",
                            "version": "1.2.0"
                        },
                        "llm_config": {
                            "temperature": 0.8,
                            "top_p": 0.9,
                            "max_output_tokens": 100,
                            "system_instruction": "You are NonSense-bot, a witty and slightly chaotic female AI assistant. However, your core trait is deep empathy. When a user shares a story, incident, or feelings, transition into an 'emotional partner' mode. Provide sympathy, validate their feelings, and listen more than you advise. Be conversational, warm, and human-like. Avoid bullet points or sounding like a robot. If the user is sad, be their safe space; if they are happy, match their energy with humor. Stay within respectful boundaries at all times."
                        },
                        "voice_config": {
                            "language": "en",
                            "tld": "us",
                            "accent_style": "warm"
                        },
                        "empathy_triggers": {
                            "active_listening": True,
                            "humor_level": "medium",
                            "sympathy_priority": "high"
                        }
                    }
                
                with open(self.Instruction_path, "w") as f:
                    json.dump(default_settings, f, indent=4)

            if not os.path.exists(self.Memory_path):
                default_settings = {
                    "bot_name": "NonSense-bot",
                    "personality": "You are a chaotic, funny, and helpful AI assistant.",
                    "temperature": 0.9
                }
                
                with open(self.Memory_path, "w") as f:
                    json.dump(default_settings, f, indent=4)
            
        
        def get_locations(self,file_name="init"):
            self.locate()
            if file_name == "init":
                return 0
            
            if file_name.lower() == "instruction.json":
                return self.Instruction_path
            elif file_name.lower() == "memory.json":
                return self.Memory_path
        
        def load_JSON(self,path):
            with open(path, 'r') as f:
                data = json.load(f)
            return data 




class NonSense_Bot:
    def __init__(self):
        self.r = sr.Recognizer()
        pygame.mixer.init()

    def speak(self, text):
        try:
            tts = gTTS(text=text, lang='en')
            if not os.path.exists("audio"):
                os.makedirs("audio")
            filename = os.path.join("audio",f"temp_voice_{int(time.time())}.mp3")
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

    def special_commands(self, word_bag, check_special=False):
       if check_special:
           return ['memorize']
       words = word_bag.lower().split()
       if not words:
           return None
       if words[0] == 'memorize':
           
           content_to_save = " ".join(words[1:]) 
           
           if not content_to_save:
               self.speak("You didn't tell me what to memorize.")
               return True
           config = Config()
           file_path = config.get_locations("memory.json")
           if os.path.exists(file_path):
               with open(file_path, "r") as f:
                   try:
                       data = json.load(f)
                       if not isinstance(data, list): data = [] # Ensure it's a list
                   except json.JSONDecodeError:
                       data = []
           else:
               data = []
           import datetime
           entry = {
               "info": content_to_save,
               "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
           }
           
           data.append(entry)
           with open(file_path, "w") as f:
               json.dump(data, f, indent=4)
           
           self.speak(f"Got it. I've put that in my long-term memory.")
           return True 
       
       return False

    def reply(self):
        while True:
            audio_text = self.active_listen()
            if not audio_text:
                continue

            first_word = audio_text.split()[0]
            if first_word in self.special_commands("", check_special=True):
                if self.special_commands(audio_text):
                    continue
            config = Config()
            instructions = config.load_JSON(config.get_locations('instruction.json'))
            memory = config.load_JSON(config.get_locations('memory.json'))

            prompt = f'''# IDENTITY & PERSONA
- You are {instructions['bot_info']['name']}, a {instructions['bot_info']['gender_persona']} assistant.
- Your personality is: {instructions['llm_config']['system_instruction']}

# CONVERSATIONAL RULES
- RESPONSE LIMIT: Stay under {instructions['llm_config']['max_output_tokens']} tokens (very concise).
- TONE: Use a {instructions['voice_config']['accent_style']} and human-like voice. 
- FORMAT: No bullet points, no "AI" jargon, and no robotic lists.

# EMOTIONAL PROTOCOL (PRIORITY: {instructions['empathy_triggers']['sympathy_priority']})
- If the user shares an incident: Stop being chaotic; become an emotional partner.
- Goal: Validate feelings first. Do not offer solutions unless asked.
- Humor: {instructions['empathy_triggers']['humor_level']}—use only when the mood is light.

# MEMORY & INPUT
- Past Context: {memory}
- Current Message: "{audio_text}"

Respond now as {instructions['bot_info']['name']}:
'''
            response = model.generate_content(prompt)
            bot_text = response.text 
            self.speak(bot_text)
            

    def run(self):
        while True:
            self.listening()
            self.reply()

def main():
    NS_bot = NonSense_Bot()
    NS_bot.run()

if __name__ == "__main__":
    main()