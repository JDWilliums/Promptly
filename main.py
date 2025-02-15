import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import threading
from utils.api_handler import OpenAIHandler

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

class OpenAIChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Promptly")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.api_handler = OpenAIHandler()
        self.api_key = self.api_handler.api_key
        
        self.create_widgets()

    def create_widgets(self):
        # Chat display area
        self.chat_window = tk.Text(self.root, height=15, state=tk.NORMAL, wrap=tk.WORD)
        self.chat_window.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # User input area
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=10, pady=5)

        self.text_input = tk.Text(frame, height=4, wrap=tk.WORD)
        self.text_input.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # Send button
        self.send_button = ttk.Button(frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=5, pady=5, ipadx=10, ipady=5, sticky="e")

        frame.columnconfigure(0, weight=1)

        # Push to Talk button
        self.talk_button = ttk.Button(self.root, text="🎤 Push to Talk", command=self.start_voice_input)
        self.talk_button.pack(pady=5)

        frame.columnconfigure(0, weight=1)

        # Menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="API Key", command=self.open_settings)

    def send_message(self):
        user_input = self.text_input.get("1.0", tk.END).strip()
        if not user_input:
            messagebox.showwarning("Warning", "Please enter a message!")
            return

        self.chat_window.insert(tk.END, f"You: {user_input}\n")
        self.text_input.delete("1.0", tk.END)

        if not self.api_handler.api_key:
            messagebox.showwarning("Warning", "API key is missing. Please enter it in Settings.")
            return

        response = self.api_handler.send_message(user_input)
        if "error" in response:
            self.chat_window.insert(tk.END, f"Error: {response['error']}\n")
        else:
            self.chat_window.insert(tk.END, f"{response['content']}\n")
            
            # Speak the response
            self.api_handler.text_to_speech(response["spoken_text"])

    def start_voice_input(self):
        """Handles speech-to-text transcription and sends the transcribed text to ChatGPT."""
        self.chat_window.insert(tk.END, "\n[DEBUG] Listening... Speak now!\n")
        threading.Thread(target=self.process_voice_input, daemon=True).start()

    def process_voice_input(self):
        """Records audio, transcribes it, and sends it to ChatGPT."""
        audio_file = self.api_handler.record_audio()
        transcribed_text = self.api_handler.transcribe_audio(audio_file)

        if transcribed_text:
            self.chat_window.insert(tk.END, f"You (Voice): {transcribed_text}\n")
            response = self.api_handler.send_message(transcribed_text)
            if "error" in response:
                self.chat_window.insert(tk.END, f"Error: {response['error']}\n")
            else:
                self.chat_window.insert(tk.END, f"{response['content']}\n")
                
                # Speak the AI response
                self.api_handler.text_to_speech(response["spoken_text"])

    def open_settings(self):
        def save_api_key():
            api_key = api_key_entry.get().strip()
            if api_key:
                self.api_handler.set_api_key(api_key)
                self.api_key = api_key
                messagebox.showinfo("Info", "API key saved!")
                settings_window.destroy()
            else:
                messagebox.showwarning("Warning", "API key cannot be empty!")

        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x150")
        settings_window.resizable(False, False)

        tk.Label(settings_window, text="Enter API Key:").pack(pady=10)
        api_key_entry = ttk.Entry(settings_window, width=30)
        api_key_entry.pack(pady=5)
        ttk.Button(settings_window, text="Save", command=save_api_key).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenAIChatApp(root)
    root.mainloop()
