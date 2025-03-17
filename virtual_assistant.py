import os
import requests
import pyttsx3
import pyjokes
import speech_recognition as sr
import datetime
import webbrowser
import pywhatkit as kit
import random
from tkinter import Tk, Label, Button, Text, PhotoImage
from googleapiclient.discovery import build

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Replace with your Google API Key and Search Engine ID
GOOGLE_API_KEY = "AIzaSyD9bOyFNm0rW1W9pcjRfBsirOjxtOkIKQs"
SEARCH_ENGINE_ID = "316f396935a2e4b8a"

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user and convert speech to text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            speak("Sorry, I'm having trouble with the speech service.")
            return None

# Function to speak text and display it in the output box
def speak(text):
    # Display the text in the GUI's output box
    output_box.insert('end', text + "\n")  # Add the text to the output box
    output_box.see('end')  # Automatically scroll to the latest entry
    app.update()  # Update the GUI

    # Speak the text
    engine.say(text)
    engine.runAndWait()


# Function to start listening for commands
def start_assistant():
    global listening
    listening = True
    speak("Voice Assistant Activated. How can I assist you?")
    while listening:
        command = listen()
        if command:
            process_command(command)


# Function to stop the assistant
def stop_assistant():
    global listening
    listening = False
    speak("Stopping the assistant. Goodbye!")
    app.quit()
# Core function to process commands
def process_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you?")
    elif "tell a joke" in command:
        tell_joke()
    elif "find hospital" in command:
        find_nearest_hospital()
    elif "search health" in command:
        search_health_info()
    elif "open youtube" in command:
        open_youtube()
    elif "play a song" in command:
        play_song()
    elif "open google" in command:
        open_google()
    elif "open calendar" in command:
        open_calendar()
    elif "what time is it" in command or "current time" in command:
        tell_time()
    elif "play music on gaana" in command:
        play_music_on_gaana()
    elif "open whatsapp" in command:
        open_whatsapp()
    elif "search" in command:
        search_question(command)
    elif "check symptoms" in command:
        check_symptoms()
    elif "find pharmacy near me" in command:
        find_pharmacy_nearme()
    elif "emergency numbers" in command:
        emergency_numbers()
    elif "medicine information" in command:
          get_medicine_info()
    elif "mental health support" in command:
        mental_health_support()
    elif "book doctor appointment" in command:
        book_doctor_appointment()
    elif "calculate bmi" in command:
        calculate_bmi()
    elif "health tips" in command:
        daily_health_tip()
    elif "stop" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't understand the command. Can you repeat?")


# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Function to open YouTube
def open_youtube():
    speak("Opening YouTube.")
    webbrowser.open("https://www.youtube.com")

def play_song():
    speak("Which song would you like to hear?")
    song = listen()
    if song:
        speak(f"Playing {song} on YouTube.")
        kit.playonyt(song)
    else:
        speak("Sorry, I didn't catch the song name.")

# Function to open Google
def open_google():
    speak("Opening Google.")
    webbrowser.open("https://www.google.com")

# Function to open Google Calendar
def open_calendar():
    speak("Opening Google Calendar.")
    webbrowser.open("https://calendar.google.com")

# Function to tell the current time
def tell_time():
    now = datetime.datetime.now()  # Get the current date and time
    time_str = now.strftime("%I:%M %p")  # Format time (e.g., 03:45 PM)
    speak(f"The current time is {time_str}.")

# Function to play music on Gaana
def play_music_on_gaana():
    speak("What song would you like to play on Gaana?")
    song = listen()
    if song:
        url = f"https://gaana.com/search/{song.replace(' ', '+')}"
        speak(f"Playing {song} on Gaana.")
        webbrowser.open(url)
    else:
        speak("Sorry, I didn't catch the song name.")

# Function to open WhatsApp Web
def open_whatsapp():
    speak("Opening WhatsApp Web.")
    webbrowser.open("https://web.whatsapp.com")
# Function to search a question on Google
def search_question(command):
    query = command.replace("search for", "").strip()
    if query:
        speak(f"Searching for {query} on Google.")
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
    else:
        speak("Sorry, I didn't catch your query.")
# Function to check symptoms
def get_medicine_info():
    speak("Please name the medicine you want information about.")
    medicine_name = listen()
    if medicine_name:
        try:
            # Initialize the Google Custom Search API client
            service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
            
            # Perform the search query
            result = service.cse().list(q=medicine_name, cx=SEARCH_ENGINE_ID).execute()
            items = result.get("items", [])
            
            if items:
                top_result = items[0]
                title = top_result.get("title", "No title available")
                snippet = top_result.get("snippet", "No snippet available")
                link = top_result.get("link", "No link available")
                
                # Speak the result
                speak(f"Here is what I found about {medicine_name}: {title}. {snippet}. Opening more details in your browser.")
                print(f"Title: {title}\nSnippet: {snippet}\nLink: {link}")
                webbrowser.open(link)  # Open the link in a browser
            else:
                speak(f"Sorry, I couldn't find any information about {medicine_name}.")
        except Exception as e:
            print(f"An error occurred: {e}")
            speak("There was an error while fetching the information.")
    else:
        speak("Sorry, I didn't catch the medicine name.")



# Function to find the nearest hospital
def find_nearest_hospital():
    speak("Please tell me your city or location.")
    location = listen()
    if location:
        # Generate a Google Maps search URL with the provided location
        url = f"https://www.google.com/maps/search/hospitals+near+{location.replace(' ', '+')}"
        speak(f"Finding hospitals near {location}. Opening results in your browser.")
        webbrowser.open(url)
    else:
        speak("Sorry, I couldn't understand your location. Please try again.")


# Function to search health-related info
def search_health_info():
    speak("What health topic would you like to search for?")
    query = listen()
    if query:
        search_google(query)
    else:
        speak("Sorry, I didn't catch your query.")

# Function to search Google using API (unused here, keeping it for other use cases)
def search_google(query):
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        result = service.cse().list(q=query, cx=SEARCH_ENGINE_ID).execute()
        items = result.get("items", [])
        if items:
            top_result = items[0]
            title = top_result.get("title", "No title available")
            snippet = top_result.get("snippet", "No snippet available")
            link = top_result.get("link", "No link available")

            speak(f"I found this: {title}. {snippet}")
            print(f"Title: {title}\nSnippet: {snippet}\nLink: {link}")
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find any results.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("There was an error while fetching the information.")

# Function to check symptoms
def check_symptoms():
    speak("Please tell me the symptoms you are experiencing.")
    symptoms = listen()
    if symptoms:
        speak(f"Checking for information related to {symptoms}.")
        search_google(symptoms)
    else:
        speak("Sorry, I couldn't get your symptoms. Please try again.")

# Function to find nearby pharmacies
def find_pharmacy_nearme():
    speak("Please tell me your city or location.")
    location = listen()
    if location:
        # Generate a Google Maps search URL with the provided location
        url = f"https://www.google.com/maps/search/pharmacies+near+{location.replace(' ', '+')}"
        speak(f"Finding pharmacies near {location}. Opening results in your browser.")
        webbrowser.open(url)
    else:
        speak("Sorry, I couldn't understand your location. Please try again.")

# Function to provide emergency numbers
def emergency_numbers():
    speak("Here are some emergency numbers you can contact.")
    speak("For medical emergencies, dial 112 or 911.")
    speak("For fire emergencies, dial 101.")
    speak("For police emergencies, dial 100.")
    speak("For ambulance services, dial 108.")

# Function to provide medicine information
def get_medicine_info():
    speak("Please name the medicine you want information about.")
    medicine_name = listen()
    if medicine_name:
        try:
            # Initialize the Custom Search API
            service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
            
            # Perform the search query
            result = service.cse().list(q=medicine_name, cx=SEARCH_ENGINE_ID).execute()
            items = result.get("items", [])
            
            if items:
                top_result = items[0]
                title = top_result.get("title", "No title available")
                snippet = top_result.get("snippet", "No snippet available")
                link = top_result.get("link", "No link available")
                
                # Speak the result
                speak(f"Here is what I found about {medicine_name}: {title}. {snippet}. Opening more details in your browser.")
                print(f"Title: {title}\nSnippet: {snippet}\nLink: {link}")
                webbrowser.open(link)  # Open the link in a browser
            else:
                speak(f"Sorry, I couldn't find any information about {medicine_name}.")
        except Exception as e:
            print(f"An error occurred: {e}")
            speak("There was an error while fetching the information.")
    else:
        speak("Sorry, I didn't catch the medicine name.")

# Function to provide mental health support
def mental_health_support():
    speak("If you're feeling down, it's important to talk to someone.")
    speak("You can contact a mental health professional or reach out to support helplines.")
    speak("In case of an emergency, dial 112 or 911.")

# Function to book doctor appointments
def book_doctor_appointment():
    speak("Would you like to find a doctor near you or search on platforms like Apollo or Practo?")
    preference = listen()
    
    if preference:  # Check if preference is not None
        if "near me" in preference or "nearby" in preference:
            speak("Which type of doctor do you need? For example, a general physician, dentist, or dermatologist.")
            doctor_type = listen()
            if doctor_type:
                speak(f"Where should I search for {doctor_type} doctors? Please tell me your city or location.")
                location = listen()
                if location:
                    # Generate a Google Maps search URL based on doctor type and location
                    url = f"https://www.google.com/maps/search/{doctor_type.replace(' ', '+')}+doctors+near+{location.replace(' ', '+')}"
                    speak(f"Searching for {doctor_type} doctors near {location}. Opening results in your browser.")
                    webbrowser.open(url)
                else:
                    speak("Sorry, I couldn't understand your location. Please try again.")
            else:
                speak("Sorry, I didn't catch the type of doctor you need. Please try again.")
        
        elif "apollo" in preference:
            speak("Opening Apollo Hospitals website for you.")
            webbrowser.open("https://www.apollohospitals.com/")

        elif "practo" in preference:
            speak("Opening Practo website for you.")
            webbrowser.open("https://www.practo.com/")

        else:
            speak("Sorry, I couldn't understand your preference. Please try again.")
    else:
        speak("Sorry, I didn't catch your response. Could you please repeat that?")



# BMI Calculator
def calculate_bmi():
    try:
        speak("Please tell me your weight in kilograms.")
        weight = float(listen())
        speak("Please tell me your height in meters.")
        height = float(listen())
        bmi = weight / (height ** 2)
        speak(f"Your Body Mass Index is {bmi:.2f}.")
        if bmi < 18.5:
            speak("You are underweight. Consider consulting a doctor or dietitian.")
        elif 18.5 <= bmi < 24.9:
            speak("Your BMI is normal. Keep up the good work!")
        elif 25 <= bmi < 29.9:
            speak("You are overweight. A balanced diet and exercise may help.")
        else:
            speak("You are in the obese range. It's recommended to consult a healthcare provider.")
    except ValueError:
        speak("Sorry, I couldn't calculate your BMI. Please ensure you provide valid numbers.")

# Health Tips
def daily_health_tip():
    tips = [
        "Drink plenty of water and stay hydrated.",
        "Eat a balanced diet rich in fruits and vegetables.",
        "Exercise for at least 30 minutes a day.",
        "Get 7-8 hours of quality sleep every night.",
        "Practice mindfulness or meditation to reduce stress.",
    ]
    tip = random.choice(tips)
    speak(f"Here's your health tip for today: {tip}")




# Function to display an image in the GUI
def display_image():
    try:
        # Ensure the correct relative or absolute path
        assistant_image = PhotoImage(file="./image/assistant.png")
        Label(app, image=assistant_image).pack(pady=20)
        # Prevent garbage collection of the image
        app.image = assistant_image
    except Exception as e:
        print(f"Error loading image: {e}")
        Label(app, text="(Image not found)", font=("Helvetica", 12), fg="red").pack(pady=10)


# GUI Setup
app = Tk()
app.title("Virtual Assistant")
app.geometry("800x800")

# Add image to the frame
display_image()

# GUI components
Label(app, text="Welcome to the Virtual Assistant", font=("Helvetica", 16)).pack(pady=10)
Button(app, text="Start Listening", font=("Helvetica", 12), command=start_assistant).pack(pady=10)
Button(app, text="Stop Listening", font=("Helvetica", 12), command=stop_assistant).pack(pady=10)


output_box = Text(app, wrap="word", height=30, width=70)
output_box.pack(pady=20)

# Run the GUI
app.mainloop()
