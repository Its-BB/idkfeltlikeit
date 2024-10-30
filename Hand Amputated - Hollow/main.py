import cv2
import mediapipe as mp
import pyautogui
import DictApp
import requests
from bs4 import BeautifulSoup
from SearchNow import searchYoutube
import pyttsx3
import wikipedia
import threading
import re
import os.path
import pygame
import wolframalpha
import speech_recognition as sr
import webbrowser
import datetime
import os
import threading

def setup_microphone():
    r = sr.Recognizer()
    m = None
    input_mic = 'ZEBRONICS'  # Use whatever is your desired input
    for i, microphone_name in enumerate(
        sr.Microphone.list_microphone_names()):
        if microphone_name == input_mic:
            m = sr.Microphone(device_index=i)
    return r, m

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Systems Started")

eye_tracking_enabled = True

def toggle_eye_tracking():
    global eye_tracking_enabled
    if eye_tracking_enabled:
        eye_tracking_enabled = False
        speak("Eye tracking turned off")
    else:
        eye_tracking_enabled = True
        speak("Eye tracking turned on")

WOLFRAM_ALPHA_APP_ID = "H4W9AA-2WWXPPL5JT"

def fetch_wolfram_alpha_result(query):
    try:
        client = wolframalpha.Client(WOLFRAM_ALPHA_APP_ID)
        res = client.query(query)
        result = next(res.results).text
        return result
    except Exception as e:
        print(f"Error fetching result Due to Calculation Issues: {e}")
        return None

def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,timeout=8,phrase_time_limit=8)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')

        print(f"User said: {query}\n")

        # Check if the user wants to type something
        if "type" in query:
            # Extract the text that the user wants to type
            text_to_type = query.replace("type", "").strip()

            print(f"Typing: {text_to_type}")

            # Replaces alphabetical characters with special characters
            special_characters = {
                'comma': ',',
                'coma': ',',
                'period': '.',
                'question mark': '?',
                'exclamation mark': '!',
                'colon': ':',
                'semicolon': ';',
                'single quote': "'",
                'double quote': '"',
                'open parenthesis': '(',
                'close parenthesis': ')',
                'open bracket': '[',
                'close bracket': ']',
                'open brace': '{',
                'close brace': '}',
                'ampersand': '&',
                'at symbol': '@',
                'hash symbol': '#',
                'dollar sign': '$',
                'percent sign': '%',
                'caret': '^',
                'asterisk': '*',
                'underscore': '_',
                'hyphen': '-',
                'plus sign': '+',
                'equal sign': '=',
                'less than sign': '<',
                'greater than sign': '>',
                'forward slash': '/',
                'backslash': '\\',
                'pipe': '|',
                'tilde': '~',
                'grave accent': '`',
            }

            # Replace spoken numbers with their written form
            for word, char in special_characters.items():
                text_to_type = text_to_type.replace(word, char)

            # Handle spoken numbers using Wolfram Alpha
            number_pattern = re.compile(r'\b(?:one|two|three|four|five|six|seven|eight|nine)\s*(?:thousand)?\b', re.IGNORECASE)
            matches = re.findall(number_pattern, text_to_type)
            for match in matches:
                result = fetch_wolfram_alpha_result(match)
                if result is not None:
                    text_to_type = text_to_type.replace(match, result)

            # Set the typing delay (you can adjust this value)
            typing_delay = 0.1  # 100 milliseconds

            # Simulate typing the text using pyautogui with delay
            pyautogui.typewrite(text_to_type, interval=typing_delay)
            return "None"  # Return None to indicte that no other comand should be executed

        return query.lower()

    except sr.UnknownValueError:
        print("Say that again please...")
        return "None"

    except sr.RequestError as e:
        print(f"Error during speech recognition: {e}")
        return "None"

def openappweb(query):
    speak("Launching, sir")
    query = query.replace("open", "").replace("holo", "").replace("launch", "").strip()
    
    if query in DictApp.dictapp:
        os.system(f"start {DictApp.dictapp[query]}")
    else:
        webbrowser.open(f"https://www.{query}.com")

def closeappweb(query):
    speak("Closing, sir")
    closed_tabs = False
    
    if "one tab" in query or "1 tab" in query:
        pyautogui.hotkey("ctrl", "w")
        closed_tabs = True

    elif "to tab" in query or "2 tab" in query:
        for _ in range(2):
            pyautogui.hotkey("ctrl", "w")
        closed_tabs = True

    elif any(f"{i} tab" in query for i in range(3, 6)):
        num_tabs = int(next(filter(str.isdigit, query)))
        for _ in range(num_tabs):
            pyautogui.hotkey("ctrl", "w")
        closed_tabs = True

    if not closed_tabs:
        for app, process_name in DictApp.items():
            if app in query:
                os.system(f"taskkill /f /im {process_name}.exe")
                closed_tabs = True
                break

    if closed_tabs:
        speak("All tabs closed")

# Your eye-controlled mouse code here
def eye_controlled_mouse():
    cameraa = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()

    while True:
        if eye_tracking_enabled:  # Check if eye tracking is enabled
            _, frame = cameraa.read()
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = face_mesh.process(rgb_frame)
            landmark_points = output.multi_face_landmarks
            frame_h, frame_w, _ = frame.shape
            if landmark_points:
                landmarks = landmark_points[0].landmark
                for id, landmark in enumerate(landmarks[474:478]):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0))
                    if id == 1:
                        screen_x = screen_w * landmark.x
                        screen_y = screen_h * landmark.y
                        pyautogui.moveTo(screen_x, screen_y)
                left = [landmarks[145], landmarks[159]]
                for landmark in left:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 255))
                if (left[0].y - left[1].y) < 0.004:
                    pyautogui.click()
                    pyautogui.sleep(1)
            cv2.imshow('Eye Controlled Mouse', frame)
            cv2.waitKey(1)
        else:
            # Eye tracking is disabled, skip processing
            pass

if __name__ == "__main__":
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)

    r, m = setup_microphone()
    wishMe()
    # Start the eye-controlled mouse code in a separate thread
    mouse_thread = threading.Thread(target=eye_controlled_mouse)
    mouse_thread.start()

    while True:
        query = takeCommand().lower()
        # Logic for executing tasks based on query

        # Logic for executing tasks based on query
        if "bye" in query:
            speak("Feel free to talk to me again, Bye")
            cv2.destroyAllWindows()
            pygame.quit()
            exit()

        # Voice command handlers for other functionalities...
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "pause" in query:
            pyautogui.press("k")
            speak("video paused")

        elif "play the video" in query:
            pyautogui.press("k")
            speak("video played")

        elif "mute" in query:
            pyautogui.press("m")
            speak("video muted")

        elif "backspace" in query:
            pyautogui.press("backspace")
            speak("Done")

        elif "enter" in query:
            pyautogui.press("enter")
            speak("Done")

        elif "volume up" in query:
            from keyboardd import volumeup

            speak("Turning volume up, sir")
            volumeup()

        if 'open' in query:
            openappweb(query)
        elif "close" in query:
            closeappweb(query)


        elif "volume down" in query:
            from keyboardd import volumedown

            speak("Turning volume down, sir")
            volumedown()

        elif 'open google' in query:
            webbrowser.open("https://www.google.com/")

        elif 'open spotify' in query:
            webbrowser.open("https://open.spotify.com/search/")

            openappweb(query)
        elif "close" in query:
            from DictApp import closeappweb

            closeappweb(query)

        elif 'introduce yourself' in query:
            speak("HI, I Am Holo , Your Personal Computer AI Assistant")

        elif "what is your name" in query:
            speak("My Name Is Holo!")

        elif "how are you today" in query:
            speak("Oh I Am Doing Good, Thanks For Asking.")
            
        elif "spotify" in query:
            from SearchNow import searchSpotify
            searchSpotify(query)

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"Sir, the time is {strTime}")

        elif "shutdown the system" in query:
            os.system("shutdown /s /t 1")

        elif "restart the system" in query:
            os.system("shutdown /r")

        elif "nice" in query:
            speak("thank you for the compliment")

        elif "calculate" in query:
            from Calculatenumbers import Calc

            query = query.replace("calculate", "")
            query = query.replace("holo", "")
            Calc(query)

        elif "left click" in query:
            pyautogui.click(button='left')

        elif "right click" in query:
            pyautogui.click(button='right')
        
        elif "left click" in query:
            num_clicks = 1
        if "two" in query:
            num_clicks = 2
            pyautogui.click(button='left', clicks=num_clicks)
        elif "to" in query:
            num_clicks = 2
            pyautogui.click(button='left', clicks=num_clicks)
        elif "three" in query:
            num_clicks = 3
            pyautogui.click(button='left', clicks=num_clicks)
        elif "four" in query:
            num_clicks = 4
            pyautogui.click(button='left', clicks=num_clicks)

        elif "temperature" in query:
            search  = "temperature in kochi"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("div", class_="BNeawe").text
            speak(f"current{search} is {temp}")

        elif "thank you" in query:
            speak("you're Welcome")
        
        elif "hariom holo" in query:
            speak("Hari Om, Sir. I Am Ready And Good To Begin Helping!")

        elif "open mail" in query:
            webbrowser.open("https://mail.google.com/mail/u/0/")

        elif "scroll down" in query:
    # Scroll down the page
            pyautogui.scroll(500)  # Scroll down by 1 notch
            speak("Scrolling down")

        elif "scroll up" in query:
    # Scroll up the page
            pyautogui.scroll(-500)  # Scroll up by 1 notch
            speak("Scrolling up")

        elif "turn off eye tracking" in query:
            toggle_eye_tracking()

        elif "turn on eye tracking" in query:
            toggle_eye_tracking()

        elif eye_tracking_enabled:
            if "who is" in query:
                person = query.replace("who is", "").strip()
                searchWikipedia(person)

            elif "what is" in query:
                topic = query.replace("what is", "").strip()
                searchWikipedia(topic)

            elif "tell us about" in query or "tell me about" in query:
                searchWikipedia(query)

        elif "wikipedia" in query:
                from SearchNow import searchWikipedia

                searchWikipedia(query)

        elif 'open youtube' in query or 'youtube' in query:
            if 'open youtube' in query:
                query = query.replace("open", "").replace("youtube", "").strip()
            elif 'youtube' in query:
                query = query.replace("youtube", "").strip()
            if query:
                searchYoutube(query, play_video=False)


