import speech_recognition as sr
import pyttsx3
import os
import re
import subprocess
import webbrowser
from google import genai
from google.genai import types

# ==============================
# 🔐 Configuration
# ==============================
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    API_KEY = "AIzaSyCVRIYfmOwhdeViKJrNAqqD8SRb9i6DOEY"  # fallback

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"❌ Gemini Client Error: {e}")

# ==============================
# 🗣️ Voice Setup
# ==============================
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)
recognizer = sr.Recognizer()

def speak(text):
    """Make Jarvis speak reliably."""
    print(f"🧠 Jarvis: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"⚠️ Speech synthesis failed: {e}")

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        print("🔍 Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"🗣️ You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("⚠️ Didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Sorry, I couldn't reach the recognition service.")
        return ""

def clean_response(text):
    text = re.sub(r'\\n|\n|\r', ' ', text)
    text = re.sub(r'[*_#>\[\]{}|]', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def chat_with_gemini(prompt):
    try:
        config = types.GenerateContentConfig(
            system_instruction="You are Jarvis, an intelligent assistant. Speak clearly and concisely.",
        )
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt],
            config=config,
        )
        return clean_response(response.text)
    except Exception as e:
        print("❌ Gemini Exception:", str(e))
        return "There was a problem connecting to the Gemini AI service."

# ==============================
# 💻 Device Control Functions
# ==============================
def shutdown():
    speak("Shutting down your system.")
    os.system("shutdown /s /t 1")

def restart():
    speak("Restarting your system.")
    os.system("shutdown /r /t 1")

def lock_pc():
    speak("Locking your computer.")
    os.system("rundll32.exe user32.dll,LockWorkStation")

def open_chrome():
    speak("Opening Google Chrome.")
    path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    if os.path.exists(path):
        subprocess.Popen([path])
    else:
        speak("Chrome not found on this system.")

def search_google(query):
    speak(f"Searching Google for {query}")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def open_folder(folder_name):
    folder_path = os.path.join("C:\\Users\\gupta\\PycharmProjects\\PythonProject1\\", folder_name)
    if os.path.exists(folder_path):
        speak(f"Opening folder {folder_name}")
        os.startfile(folder_path)
    else:
        speak("Sorry, I can't find that folder.")

def open_notepad():
    speak("Opening Notepad.")
    subprocess.Popen(['notepad.exe'])

def open_calculator():
    speak("Opening Calculator.")
    subprocess.Popen(['calc.exe'])

# ==============================
# 🔁 Main Loop
# ==============================
if __name__ == "__main__":
    speak("Hello, I am Jarvis. Say 'Jarvis' to activate me.")

    while True:
        print("🕒 Waiting for wake word 'Jarvis'...")
        wake_input = listen()

        if "jarvis" in wake_input:
            speak("Yes? What would you like me to do?")
            command = listen()

            if not command:
                speak("Sorry, I didn't catch that.")
                continue

            command_lower = command.lower()

            # Exit commands
            if any(word in command_lower for word in ["exit", "stop", "bye"]):
                speak("Goodbye! Have a great day.")
                break

            # Device control
            elif "shutdown" in command_lower:
                shutdown()
                break
            elif "restart" in command_lower:
                restart()
                break
            elif "lock pc" in command_lower or "lock computer" in command_lower:
                lock_pc()
            elif "open chrome" in command_lower:
                open_chrome()
            elif "open notepad" in command_lower:
                open_notepad()
            elif "open calculator" in command_lower:
                open_calculator()
            elif "search for" in command_lower or "google" in command_lower:
                search_query = command_lower.replace("search for", "").replace("google", "").strip()
                if search_query:
                    search_google(search_query)
                else:
                    speak("What should I search for?")
            elif "open folder" in command_lower:
                folder = command_lower.replace("open folder", "").strip()
                open_folder(folder)
            else:
                # Chat with Gemini AI
                response = chat_with_gemini(command)
                speak(response)

