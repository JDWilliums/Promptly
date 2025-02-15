# 🎙️ Promptly - AI Voice Assistant

Promptly is a **lightweight AI voice assistant** that integrates **speech-to-text (STT) and text-to-speech (TTS)** with **ChatGPT** for seamless voice interaction.

## 🚀 Features
- ✅ **Voice Input** - Speak instead of typing
- ✅ **AI Chat Integration** - Get responses from ChatGPT
- ✅ **Text-to-Speech** - AI replies in a natural voice
- ✅ **Push-to-Talk** - Hands-free interaction

## 📂 File Structure
```
Promptly/
│── utils/
│   ├── api_handler.py              # API handling (ChatGPT, ElevenLabs, Whisper)
│   ├── config.json                 # API keys (DO NOT SHARE THIS FILE)
│── main.py                         # GUI application
│── requirements.txt                 # Dependencies
│── .gitignore                       # Prevents uploading sensitive files
│── README.md                        # Project documentation
```

## 📦 Installation

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/JDWilliums/promptly.git
cd promptly
```

### 2️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

### 3️⃣ **Set Up API Keys**
- Create a file: `utils/config.json`
- Add your API keys:
```json
{
    "api_key": "your-openai-api-key-here",
    "elevenlabs_api_key": "your-elevenlabs-api-key-here",
    "elevenlabs_voice_id": "your-voice-id-here"
}
```

### 4️⃣ **Run the Application**
```sh
python main.py
```

## 🛠️ **Contributing**
1. **Fork the repo**
2. **Create a feature branch:** `git checkout -b my-new-feature`
3. **Commit changes:** `git commit -m "Added new feature"`
4. **Push changes:** `git push origin my-new-feature`
5. **Create a Pull Request**

## 📜 License
This project is licensed under the MIT License.

---

🚀 **Enjoy using Promptly!** If you find this project useful, consider giving it a ⭐ on GitHub!

