import speech_recognition
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)
    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        return "None"
    return query


query = takeCommand().lower()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# ... (other imports)

def searchGoogle(query):
    if "tell us about" in query or "what is" in query or "who is" in query or "about" in query or "tell me about" in query:
        # Use the original query for searching on Google
        google_query = query.replace("tell us about", "").replace("what is", "").replace("who is", "").replace("about", "").replace("tell me about", "")
        webbrowser.open(f"https://www.google.com/search?q={google_query}")
        pywhatkit.search(google_query)
        speak(f"Here is what I found on Google about {google_query}")
    else:
        # Use the original query for searching on Google
        google_query = query
        webbrowser.open(f"https://www.google.com/search?q={google_query}")
        pywhatkit.search(google_query)
        speak(f"Here is what I found on Google about {google_query}")

    
def searchYoutube(query, play_video=True):
    if "youtube" in query:
        speak("This is what I found for your search!")
        query = query.replace("youtube search", "")
        query = query.replace("youtube", "")
        query = query.replace("zarah", "")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        if play_video:
            pywhatkit.playonyt(query)
            speak("Done, Sir")


def searchWikipedia(query):
    if "tell us about" in query or "what is" in query or "who is" in query or "about" in query or "tell me about" in query:
        # Use the original query for searching on Wikipedia
        wikipedia_query = query.replace("tell us about", "").replace("what is", "").replace("who is", "").replace("about", "").replace("tell me about", "")
        try:
            results = wikipedia.summary(wikipedia_query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple possible matches. Please specify the topic.")
        except wikipedia.exceptions.PageError as e:
            speak("Sorry, I couldn't find information about that.")

    else:
        # Use the original query for searching on Wikipedia
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple possible matches. Please specify the topic.")
        except wikipedia.exceptions.PageError as e:
            speak("Sorry, I couldn't find information about that.")

def searchSpotify(query):
    if "spotify" in query:
        speak("This is what I found for your search!")
        query = query.replace("spotify search", "")
        query = query.replace("spotify", "")
        query = query.replace("zarah", "")
        web = "https://open.spotify.com/search/" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, Sir")
        