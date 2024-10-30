import tkinter as tk
import subprocess
import json
import os
import sys

paths = {
    "Zarah": "Blind - Zarah/main.py",
    "Ava": "Mute - Ava/ttos.py",
    "Echo": "Deaf - Echo/main.py",
    "Hollow": "Hand Amputated - Hollow/main.py",
    "BlindKeyboardTraining": "keyboardtraining.py"
}

processes = {}

config_file = "ai_toggle_config.json"

def save_config():
    """Save the current state of the checkbuttons to a config file."""
    config = {
        "Zarah": var_zarah.get(),
        "Ava": var_ava.get(),
        "Echo": var_echo.get(),
        "Hollow": var_hollow.get(),
        "BlindKeyboardTraining": var_blindkeyboardtraining.get()
    }
    with open(config_file, "w") as f:
        json.dump(config, f)

def load_config():
    """Load the state of the checkbuttons from a config file."""
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    return {}

def toggle_ai(ai_name, var):
    if var.get():
        processes[ai_name] = subprocess.Popen(["python", paths[ai_name]])
        print(f"{ai_name} started")
    else:
        if ai_name in processes:
            processes[ai_name].terminate()
            print(f"{ai_name} stopped")
    save_config()

def add_to_startup():
    """Add the application to system startup."""
    if sys.platform == "win32":
        startup_dir = os.path.join(os.getenv('APPDATA'), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        shortcut_path = os.path.join(startup_dir, "AI_Toggle_App.lnk")
        if not os.path.exists(shortcut_path):
            import winshell
            with winshell.shortcut(shortcut_path) as shortcut:
                shortcut.path = sys.executable
                shortcut.arguments = f'"{os.path.realpath(__file__)}"'
                shortcut.description = "AI Toggle App"
                shortcut.icon_location = (sys.executable, 0)
    elif sys.platform == "linux":
        autostart_dir = os.path.expanduser("~/.config/autostart")
        os.makedirs(autostart_dir, exist_ok=True)
        desktop_entry = f"""
        [Desktop Entry]
        Type=Application
        Exec={sys.executable} {os.path.realpath(__file__)}
        Hidden=false
        NoDisplay=false
        X-GNOME-Autostart-enabled=true
        Name=AI Toggle App
        Comment=Start AI Toggle App at login
        """
        with open(os.path.join(autostart_dir, "AI_Toggle_App.desktop"), "w") as f:
            f.write(desktop_entry)

root = tk.Tk()
root.title("AI Toggle App")
root.geometry("300x230")

var_zarah = tk.BooleanVar()
var_ava = tk.BooleanVar()
var_echo = tk.BooleanVar()
var_hollow = tk.BooleanVar()
var_blindkeyboardtraining = tk.BooleanVar()

config = load_config()
var_zarah.set(config.get("Zarah", False))
var_ava.set(config.get("Ava", False))
var_echo.set(config.get("Echo", False))
var_hollow.set(config.get("Hollow", False))
var_blindkeyboardtraining.set(config.get("BlindKeyboardTraining", False))

check_zarah = tk.Checkbutton(root, text="Zarah", variable=var_zarah, command=lambda: toggle_ai("Zarah", var_zarah))
check_ava = tk.Checkbutton(root, text="Ava", variable=var_ava, command=lambda: toggle_ai("Ava", var_ava))
check_echo = tk.Checkbutton(root, text="Echo", variable=var_echo, command=lambda: toggle_ai("Echo", var_echo))
check_hollow = tk.Checkbutton(root, text="Hollow", variable=var_hollow, command=lambda: toggle_ai("Hollow", var_hollow))
check_blindkeyboardtraining = tk.Checkbutton(root, text="Blind Keyboard Training", variable=var_blindkeyboardtraining, command=lambda: toggle_ai("BlindKeyboardTraining", var_blindkeyboardtraining))

check_zarah.pack(pady=10)
check_ava.pack(pady=10)
check_echo.pack(pady=10)
check_hollow.pack(pady=10)
check_blindkeyboardtraining.pack(pady=10)

add_to_startup()

root.mainloop()

for process in processes.values():
    process.terminate()
