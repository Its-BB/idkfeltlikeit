import pyttsx3
from pynput import keyboard
import time
from collections import deque

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust the speech rate if needed

# Variables to track the state of key presses
stop_flag = False

# Buffer to hold key presses
key_buffer = deque()

# Set to track currently pressed keys
pressed_keys = set()

def announce_keys():
    """Announce all key presses in the buffer."""
    while key_buffer:
        key_name = key_buffer.popleft()
        print(f"Announcing: {key_name}")  # Debug print
        engine.say(f"You pressed {key_name}")
        engine.runAndWait()

def on_press(key):
    global stop_flag

    try:
        key_name = key.char
    except AttributeError:
        key_name = str(key).replace("Key.", "")

    # Debug print to check key pressed
    print(f"Key pressed: {key_name}")
    
    if key == keyboard.Key.num_lock:
        # Stop the script if Numpad 1 is pressed
        stop_flag = True
        return False

    if not stop_flag and key_name not in pressed_keys:
        pressed_keys.add(key_name)
        key_buffer.append(key_name)

def on_release(key):
    try:
        key_name = key.char
    except AttributeError:
        key_name = str(key).replace("Key.", "")
    
    # Debug print to check key released
    print(f"Key released: {key_name}")
    
    if key_name in pressed_keys:
        pressed_keys.remove(key_name)

# Set up the listener for keyboard events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    try:
        while not stop_flag:
            announce_keys()
            time.sleep(0.1)  # Adjust the sleep time if needed
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
