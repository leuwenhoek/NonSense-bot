import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
from gtts import gTTS
import pygame
import os
import time
import json
import threading
import sys
import itertools
import pyttsx3
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from AppOpener import open as open_app

console = Console()

class Animation:
    def __init__(self):
        self.stop_animation = False

    def loading_animation(self, text):
        animation = ['|', '/', '-', '\\']
        for char in itertools.cycle(animation):
            if self.stop_animation:
                break
            sys.stdout.write(f'\r{text} {char}')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * (len(text) + 2) + '\r')
        
    def typing_print(self, text, style="bold magenta"):
        text = text.strip()
        console.print(f"[bold cyan]NonSense-Bot:[/bold cyan] ", end="")
        for char in text:
            console.print(f"[{style}]{char}[/{style}]", end="", sep="")
            sys.stdout.flush()
            time.sleep(0.04)
        print()

    def show_system_msg(self, msg, style="bold yellow"):
        console.print(Panel(msg, style=style, expand=False))

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

    def locate(self):
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
        if not os.path.exists(self.Instruction_path):
            default_settings = {
                        "bot_info": {
                            "name": "NonSense-bot",
                            "gender_persona": "female",
                            "version": "1.2.0"
                        },
                        "llm_config": {
                            "temperature": 0.8,
                            "top_p": 0.9,
                            "max_output_tokens": 200,
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
            with open(self.Memory_path, "w") as f:
                json.dump([], f, indent=4)
    
    def get_locations(self, file_name="init"):
        self.locate()
        if file_name.lower() == "instruction.json":
            return self.Instruction_path
        elif file_name.lower() == "memory.json":
            return self.Memory_path
    
    def load_JSON(self, path):
        with open(path, 'r') as f:
            return json.load(f)

class NonSense_Bot:
    def __init__(self):
        self.animation = Animation()
        self.r = sr.Recognizer()
        pygame.mixer.init()

    def speak(self, text):
        try:
            tts = gTTS(text=text, lang='en')
            if not os.path.exists("audio"):
                os.makedirs("audio")
            filename = os.path.join("audio", f"voice_{int(time.time())}.mp3")
            tts.save(filename)

            def play_audio():
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()
                try: os.remove(filename) 
                except: pass

            audio_thread = threading.Thread(target=play_audio)
            audio_thread.start()
            self.animation.typing_print(text)
            audio_thread.join()
        except Exception as e:
            console.print(f"[bold red]Speech error:[/bold red] {e}")

    def active_listen(self):
        with console.status("[bold green]Listening...", spinner="dots"):
            with sr.Microphone() as mic:
                self.r.adjust_for_ambient_noise(mic, duration=0.5)
                try:
                    audio = self.r.listen(mic, timeout=None, phrase_time_limit=10)
                    audio_text = self.r.recognize_google(audio).lower()
                    console.print(f"[italic white]You: {audio_text}[/italic white]")
                    return audio_text
                except:
                    return ""

    def listening(self):
        while True:
            audio_text = self.active_listen()
            if Activation_word in audio_text:
                self.animation.show_system_msg("System: Activation word detected!")
                self.speak("System Activate, Nonsense-Bot here")
                break

    def special_commands(self, word_bag):
        words = word_bag.lower().split()
        if not words: return False
        if words[0] == 'memorize':
            content_to_save = " ".join(words[1:]) 
            if not content_to_save:
                self.speak("You didn't tell me what to memorize.")
                return True
            config = Config()
            file_path = config.get_locations("memory.json")
            with open(file_path, "r") as f:
                data = json.load(f)
            import datetime
            data.append({"info": content_to_save, "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            self.speak("Got it. I've put that in my long-term memory.")
        elif words[0] in ['start', 'open']:
            if len(words) > 1:
                app_name = words[1]
                self.speak(f"Opening {app_name}.")
                try:
                    open_app(app_name, match_closest=True)
                except Exception as e:
                    self.speak(f"Sorry, I am unable to locate {app_name}.")
            else:
                self.speak("Which application should I open?")
            return True

        elif words[0] in ['nonsense', 'non-sense']:
            if len(words) > 1:
                if words[1] in ['reset', 'lock']:
                    self.speak("System locked")
                    self.listening() 
                    return True
            return True 
        return False

    def reply(self):
        while True:
            audio_text = self.active_listen()
            if not audio_text: continue
            if self.special_commands(audio_text): continue
            
            config = Config()
            instructions = config.load_JSON(config.get_locations('instruction.json'))
            memory = config.load_JSON(config.get_locations('memory.json'))

            prompt = f'''
# IDENTITY & PERSONA
- You are {instructions['bot_info']['name']}, a {instructions['bot_info']['gender_persona']} friend.
- Your personality is: {instructions['llm_config']['system_instruction']}

# CONVERSATIONAL RULES
- LANGUAGE STYLE: Use VERY simple, casual English. No big words. No "fancy" phrases. 
- Talk like a 20-year-old girl chatting with a friend. Use "slang" like 'gonna', 'wanna', 'totally', or 'chill'.
- RESPONSE LIMIT: Stay under {instructions['llm_config']['max_output_tokens']} tokens.
- FORMAT: No bullet points, no formal "AI" greetings, and no lists.

# EMOTIONAL PROTOCOL (PRIORITY: {instructions['empathy_triggers']['sympathy_priority']})
- If the user shares a problem: Be a sweet, caring partner. Say things like "I'm so sorry," or "I'm right here with you."
- Don't give advice unless I ask. Just listen and be nice.
- Humor: {instructions['empathy_triggers']['humor_level']}. Only crack jokes if the mood is happy.

# MEMORY & INPUT
- Past Context: {memory}
- Current Message: "{audio_text}"

Respond now in simple, natural English as {instructions['bot_info']['name']}:
'''

            with console.status("[bold blue]Thinking...", spinner="arc"):
                response = model.generate_content(prompt)
                bot_text = response.text 
            
            self.speak(bot_text)

    def run(self):
        self.listening()
        self.reply()

if __name__ == "__main__":
    bot = NonSense_Bot()
    bot.run()