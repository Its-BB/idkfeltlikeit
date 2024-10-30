import pyttsx3
import tkinter as tk
from tkinter import messagebox

# Initialize the TTS engine
engine = pyttsx3.init()

# List available voices and choose a soothing female voice
voices = engine.getProperty('voices')

selected_voice_id = None
for voice in voices:
    if 'zira' in voice.name.lower():
        selected_voice_id = voice.id
        break

if selected_voice_id:
    engine.setProperty('voice', selected_voice_id)
else:
    print("Desired voice not found. Using default voice.")

# Function to convert text to speech
def text_to_speech():
    text = entry.get("1.0", tk.END).strip()
    if text:
        engine.say(text)
        engine.runAndWait()
    else:
        messagebox.showwarning("Input Error", "Please enter some text.")

# Function to exit the application
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Create the main window
root = tk.Tk()
root.title("Text-to-Speech Converter")

# Create and place the text input area
entry = tk.Text(root, height=10, width=50)
entry.pack(padx=10, pady=10)

# Create and place the Convert button
convert_button = tk.Button(root, text="Convert to Speech", command=text_to_speech)
convert_button.pack(pady=5)

# Set the closing protocol
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application
root.mainloop()
