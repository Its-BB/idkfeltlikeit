import wolframalpha
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def WolfRamAlpha(query):
    apikey = "H4W9AA-2WWXPPL5JT"
    requester = wolframalpha.Client(apikey)
    requested = requester.query(query)
    try:
        answer = next(requested.results).text
        return answer
    except:
        speak("The value is not answerable")

def Calc(query):
    num = str(query)
    num = num.replace("zarah", "")
    num = num.replace("multiply", "*")
    num = num.replace("multiplied by", "*")
    num = num.replace("plus", "+")
    num = num.replace("minus", "-")
    num = num.replace("divide", "/")
    num = num.replace("bracket open", "(")
    num = num.replace("bracket close", ")")
    num = num.replace("into", "*")

    Final = str(num)
    try:
        result = WolfRamAlpha(Final)
        print(f"{result}")
        speak(result)
    except:
        speak("The value is not answerable")
