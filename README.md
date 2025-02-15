# 🎙️ Promptly - AI Voice Assistant

Promptly is a **lightweight AI voice assistant** that integrates **speech-to-text (STT) and text-to-speech (TTS)** with **ChatGPT** for seamless voice interaction.

## 🚀 Features
✅ **Voice Input** - Speak instead of typing  
✅ **AI Chat Integration** - Get responses from ChatGPT  
✅ **Text-to-Speech** - AI replies in a natural voice  
✅ **Push-to-Talk** - Hands-free interaction  

## 📂 File Structure

Promptly/ │── utils/ │ ├── api_handler.py # API handling (ChatGPT, ElevenLabs, Whisper) │ ├── config.json # API keys (DO NOT SHARE THIS FILE) │── main.py # GUI application │── requirements.txt # Dependencies │── .gitignore # Prevents uploading sensitive files │── README.md # Project documentation

## 📦 Installation
### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/yourusername/promptly.git
cd promptly

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Set Up API Keys
Create a file: utils/config.json
Add your API keys:
{
    "api_key": "your-openai-api-key-here",
    "elevenlabs_api_key": "your-elevenlabs-api-key-here",
    "elevenlabs_voice_id": "your-voice-id-here"
}

4️⃣ Run the Application
python main.py
