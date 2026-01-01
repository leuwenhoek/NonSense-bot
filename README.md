# 🎙️ NonSense-Bot

**NonSense-Bot** is an empathetic, witty, and slightly chaotic AI voice assistant powered by Google's Gemini 2.0 Flash.  
Unlike standard utility-focused AI, NonSense-Bot is designed to be an *emotional partner* — prioritizing active listening, sympathy, and casual conversation over robotic task management 🤍🌀

---

## ✨ Features

- 🎤 **Voice Interaction**  
  Hands-free communication using `SpeechRecognition` and `gTTS` (Google Text-to-Speech).

- 🧠 **Emotional Intelligence**  
  Transition-based persona that shifts from witty humor to deep empathy depending on your mood.

- 💾 **Long-Term Memory**  
  A dedicated **"memorize"** command allows the bot to store specific facts or memories in a local JSON database.

- 🎨 **Rich Terminal Interface**  
  Beautiful UI with real-time status updates, animations, and styled text using the `Rich` library.

- 😎 **Persona-Driven**  
  Speaks like a casual 20-year-old friend — simple language, slang, warmth, and zero robotic vibes.

---

## 🛠️ Tech Stack

- **LLM:** Google Gemini 2.0 Flash (`google-generativeai`)
- **Speech-to-Text:** `SpeechRecognition` (Google Web Speech API)
- **Text-to-Speech:** `gTTS`
- **Audio Playback:** `pygame`
- **Terminal UI:** `rich`
- **Environment Management:** `python-dotenv`

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

- Python **3.9+**  
- Google Gemini API Key  
  👉 https://aistudio.google.com/

---

### 2️⃣ Installation

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📦 `requirements.txt`

Create a file named **`requirements.txt`** in the project root and paste this 👇

```txt
speechrecognition
google-generativeai
python-dotenv
gtts
pygame
rich
pyaudio
```

---

## 🐍 Special Instructions for Python 3.14 (Windows 64-bit)

⚠️ **PyAudio installation can break on newer Python versions**, so follow this carefully 👇

### Step 1: Download Wheel

```
pyaudio-0.2.14-cp314-cp314-win_amd64.whl
```

(Source: Python Champollion Physics – SourceForge)

---

### Step 2: Install Using `uv`

```bash
uv pip install pyaudio-0.2.14-cp314-cp314-win_amd64.whl
```

---

### Step 3: Verify Installation

```bash
python -c "import pyaudio; print(pyaudio.__version__)"
```

---

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

---

## ▶️ Running the Bot

```bash
python main.py
```

---

## 🎮 How to Use

- 🟢 **Wake Word:** Say **"nonsense"**
- 💬 **Conversation:** Just talk normally
- 🧠 **Memorization:**  
  "Memorize that my favorite color is midnight blue."
- ❌ **Exit:** `Ctrl + C`

---

## 📂 Project Structure

```plaintext
├── main.py
├── requirements.txt
├── .env
├── config/
│   ├── Instruction.json
│   └── Memory.json
└── audio/
```

---

## 🛠️ Customization

Edit `config/Instruction.json`:

- `temperature` → Creativity level  
- `system_instruction` → Core personality  
- `humor_level` → low / medium / high  

---

## ⚠️ System Notes

- 🎙️ Mic must be default input
- 🪟 Windows: Allow microphone access
- 🐧 Linux:
```bash
sudo apt install portaudio19-dev espeak
```

---

## ❤️ Final Note

NonSense-Bot isn’t just an assistant —  
it’s a listener, a friend, and sometimes a little chaotic therapist 
