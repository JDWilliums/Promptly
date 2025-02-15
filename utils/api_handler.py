import openai
import json
import os
import platform
import sounddevice as sd
import requests
import numpy as np
import wave
from elevenlabs.client import ElevenLabs
from elevenlabs import play



CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

ELEVENLABS_URL = "https://api.elevenlabs.io/v1/text-to-speech/"
WHISPER_API_URL = "https://api.openai.com/v1/audio/transcriptions"

class OpenAIHandler:
    """
    Handles communication with the OpenAI API and ElevenLabs TTS, as well as API key management.
    """
    def __init__(self):
        self.api_key, self.elevenlabs_api_key, self.elevenlabs_voice_id = self.load_config()
        self.client = openai.OpenAI(api_key=self.api_key) if self.api_key else None

    def set_api_key(self, api_key):
        """Sets the OpenAI API key, initializes the client, and saves it to the config file."""
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        self.save_config()

    def save_config(self):
        """Saves API keys to a local config file without overwriting existing values."""
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        config["api_key"] = self.api_key
        config["elevenlabs_api_key"] = self.elevenlabs_api_key
        config["elevenlabs_voice_id"] = self.elevenlabs_voice_id
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

    def load_config(self):
        """Loads API keys from the config file if it exists."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                api_key = config.get("api_key")
                if not api_key:
                    print("[ERROR] OpenAI API key is missing from config.json")
                else:
                    print(f"[DEBUG] OpenAI API Key Loaded: {api_key[:5]}... (truncated for security)")
                return (
                    api_key,
                    config.get("elevenlabs_api_key"),
                    config.get("elevenlabs_voice_id"),
                )
        return None, None, None



    def send_message(self, prompt):
        """Sends a message to OpenAI API and returns the response."""
        if not self.client:
            return {"error": "API key is not set. Please enter an API key in Settings."}
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Change if needed
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Keep responses concise and prioritize important information in the spoken reply."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=300,
            )
            
            content = response.choices[0].message.content.strip()
            return {"spoken_text": content.split(". ")[0], "content": content}
        except openai.APIError as e:
            return {"error": f"API Error: {e}"}
        except openai.AuthenticationError:
            return {"error": "Invalid API key. Please check your key and try again."}
        except Exception as e:
            return {"error": f"An error occurred: {e}"}
    
    def record_audio(self, filename="input.wav", duration=5, samplerate=44100):
        """Records audio from the microphone and saves it as a WAV file."""
        print("[DEBUG] Recording audio...")
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
        sd.wait()
        
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())
        print("[DEBUG] Audio recording saved as", filename)
        return filename
    
    def transcribe_audio(self, filename="input.wav"):
        """Transcribes recorded audio using OpenAI Whisper API."""
        print("[DEBUG] Sending audio to Whisper for transcription...")
        
        if not self.api_key:
            print("[ERROR] OpenAI API key is missing.")
            return ""
        
        print(f"[DEBUG] Using API Key: {self.api_key[:5]}... (truncated for security)")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        files = {
            "file": (filename, open(filename, "rb"), "audio/wav"),
            "model": (None, "whisper-1")
        }
        
        try:
            response = requests.post(WHISPER_API_URL, headers=headers, files=files)
            if response.status_code == 200:
                transcription = response.json().get("text", "")
                print("[DEBUG] Transcription: ", transcription)
                return transcription
            else:
                print("[ERROR] Whisper API response: ", response.json())
                return ""
        except Exception as e:
            print("[ERROR] Whisper API error:", e)
            return ""

    def text_to_speech(self, text1):
        """Uses ElevenLabs TTS to convert text to speech."""
        print("\n[DEBUG] text_to_speech() called")
        print(f"[DEBUG] Text Received: {text1}")
        
        if not text1:
            print("[ERROR] No text provided for TTS.")
            return
        if not self.elevenlabs_api_key:
            print("[ERROR] Missing ElevenLabs API key.")
            return
        if not self.elevenlabs_voice_id:
            print("[ERROR] Missing ElevenLabs Voice ID.")
            return
        
        headers = {
            "xi-api-key": self.elevenlabs_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text1,
            "voice_id": self.elevenlabs_voice_id,
            "model_id": "eleven_monolingual_v2",
            "settings": {"stability": 0.5, "similarity_boost": 0.8}
        }
        
        print("[DEBUG] Sending request to ElevenLabs TTS API...")
        print("[DEBUG] Headers:", headers)
        print("[DEBUG] Payload:", payload)
        
        try:
            client = ElevenLabs(api_key=self.elevenlabs_api_key)

            audio = client.text_to_speech.convert(
                text=text1,
                voice_id=self.elevenlabs_voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128"
            )
            play(audio)
            
            
        except Exception as e:
            print("[ERROR] TTS Error:", e)

    def play_audio(self, file_path):
        """Plays the generated audio file cross-platform."""
        print("[DEBUG] Attempting to play audio file:", file_path)
        
        system = platform.system()
        try:
            if system == "Windows":
                os.system(f"start {file_path}")
            elif system == "Darwin":  # macOS
                os.system(f"afplay {file_path}")
            elif system == "Linux":
                os.system(f"mpg123 {file_path}")  # Requires mpg123 package
            else:
                print("[ERROR] Unsupported OS for audio playback.")
        except Exception as e:
            print("[ERROR] Error playing audio:", e)

if __name__ == "__main__":
    handler = OpenAIHandler()
    print("\n[DEBUG] API Handler initialized.")

    # 🔥 Test STT Manually
    print("\n[DEBUG] Recording audio for 5 seconds... Speak now!")
    audio_file = handler.record_audio()
    
    print("\n[DEBUG] Transcribing audio...")
    transcribed_text = handler.transcribe_audio(audio_file)

    print("\n[DEBUG] Final Transcription:", transcribed_text)

