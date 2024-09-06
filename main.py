import speech_recognition as sr
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import webbrowser
import pyttsx3
import requests
import time
import pyjokes
import musicLibrary
import wikipedia
import random
import os

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to fetch top news headlines
def get_top_headlines():
    api_key = '*API_Key*'  # Replace with your actual NewsAPI key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get('articles', [])
        
        if articles:
            speak("Here are the top news headlines")
            for i, article in enumerate(articles[:5], start=1):  # Get top 5 articles
                speak(f"{i}. {article['title']}")
        else:
            speak("No news found.")
    else:
        speak(f"Error fetching news: {response.status_code}")

# Function to get weather information
def get_weather(city):
    api_key = '*ApiKey*'  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    
    if weather_data["cod"] == 200:
        main = weather_data["main"]
        temperature = main["temp"]
        description = weather_data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature} degrees Celsius with {description}.")
    else:
        speak("City not found.")

# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Function to set a reminder
def set_reminder(minutes):
    speak(f"Setting a reminder for {minutes} minutes.")
    time.sleep(int(minutes) * 60)
    speak("Reminder! Time's up.")

# Function to search Wikipedia
def search_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    speak(results)

def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Normalize volume (convert level to a float between 0.0 and 1.0)
    volume_level = int(level) / 100.0
    volume.SetMasterVolumeLevelScalar(volume_level, None)
    speak(f"Setting volume to {level} percent")

# Function to process user commands
def processCommand(command):
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
    elif command.startswith("play"):
        song = command.split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in command:
        get_top_headlines()
    elif "weather" in command:
        city = command.split("weather in ")[1]
        get_weather(city)
    elif "joke" in command:
        tell_joke()
    elif "reminder" in command:
        minutes = command.split("reminder for ")[1].split(" ")[0]
        set_reminder(minutes)
    elif "search" in command:
        query = command.split("search for ")[1]
        search_wikipedia(query)
    elif "shutdown" in command:
        shutdown_system()
    elif "restart" in command:
        restart_system()
    elif "volume" in command:
        level = command.split("volume to ")[1]
        set_volume(level)
# Function to shutdown the system
def shutdown_system():
    speak("Shutting down the system.")
    os.system("shutdown /s /t 1")

# Function to restart the system
def restart_system():
    speak("Restarting the system.")
    os.system("shutdown /r /t 1")

# Function to control system volume
def set_volume(level):
    os.system(f"setvol {level}")

if __name__ == "__main__":
    speak("Initializing Voice Mate.....")
    
    while True:
        # Listen for the wake word "Voicemate"
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            word = r.recognize_google(audio)
            print(f"Recognized word: {word}")
            
            if word.lower() == "voice mate":
                speak("Yes, how can I assist?")
                
                # Listen for the actual command
                with sr.Microphone() as source:
                    print("Voice Mate Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print(f"Command: {command}")
                    processCommand(command.lower())

        except Exception as e:
            print("Error: {0}".format(e))
