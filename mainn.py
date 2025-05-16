import speech_recognition as sr
import pyttsx3
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
import random
from datetime import datetime

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Initialize NLP tools
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech rate

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=7)
    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except Exception as e:
        speak("Sorry, I didn't catch that. Please repeat.")
        return ""

def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text)
    # Stem and Lemmatize
    processed = [lemmatizer.lemmatize(stemmer.stem(token)) for token in tokens if token.isalpha()]
    return processed

# Sample flight and hotel database for demonstration
flights_db = [
    {"flight_no": "AI101", "from": "new york", "to": "london", "date": "2025-05-20", "time": "10:00"},
    {"flight_no": "BA202", "from": "new york", "to": "paris", "date": "2025-05-20", "time": "14:00"},
    {"flight_no": "DL303", "from": "london", "to": "new york", "date": "2025-05-21", "time": "09:00"},
    {"flight_no": "AF404", "from": "paris", "to": "new york", "date": "2025-05-21", "time": "17:00"},
    {"flight_no": "AA123", "from": "new york", "to": "london", "date": "2025-05-20", "time": "10:00"},
    {"flight_no": "BA234", "from": "london", "to": "paris", "date": "2025-05-21", "time": "14:30"},
    {"flight_no": "DL345", "from": "tokyo", "to": "dubai", "date": "2025-06-05", "time": "22:15"},
    {"flight_no": "EK456", "from": "sydney", "to": "los angeles", "date": "2025-05-30", "time": "08:00"},
    {"flight_no": "JL567", "from": "paris", "to": "tokyo", "date": "2025-05-16", "time": "16:45"},
    {"flight_no": "UA678", "from": "berlin", "to": "mumbai", "date": "2025-07-01", "time": "13:00"},
    {"flight_no": "SQ789", "from": "singapore", "to": "rome", "date": "2025-06-10", "time": "19:30"},
    {"flight_no": "QF890", "from": "london", "to": "los angeles", "date": "2025-05-25", "time": "11:00"},
    {"flight_no": "AF901", "from": "new york", "to": "paris", "date": "2025-05-22", "time": "17:20"},
    {"flight_no": "LH012", "from": "madrid", "to": "amsterdam", "date": "2025-06-18", "time": "06:50"},
    {"flight_no": "BA345", "from": "dubai", "to": "singapore", "date": "2025-06-22", "time": "21:10"},
    {"flight_no": "AA678", "from": "los angeles", "to": "new york", "date": "2025-07-03", "time": "09:45"},
    {"flight_no": "DL890", "from": "tokyo", "to": "seoul", "date": "2025-06-08", "time": "07:30"},
    {"flight_no": "EK234", "from": "mumbai", "to": "dubai", "date": "2025-07-10", "time": "18:00"},
    {"flight_no": "JL901", "from": "sydney", "to": "tokyo", "date": "2025-06-25", "time": "12:15"},
    {"flight_no": "UA567", "from": "amsterdam", "to": "berlin", "date": "2025-07-05", "time": "15:40"},
    {"flight_no": "SQ345", "from": "singapore", "to": "bangkok", "date": "2025-06-30", "time": "20:20"},
    {"flight_no": "QF123", "from": "los angeles", "to": "sydney", "date": "2025-05-28", "time": "23:55"},
    {"flight_no": "AF234", "from": "paris", "to": "madrid", "date": "2025-06-14", "time": "10:10"},
    {"flight_no": "LH789", "from": "amsterdam", "to": "london", "date": "2025-06-20", "time": "14:50"}
]


hotels_db = {
    "london": [
        {"name": "London Luxury Hotel", "price": 200},
        {"name": "Budget London Inn", "price": 80},
        {"name": "London Central Suites", "price": 150},
    ],
    "paris": [
        {"name": "Paris Grand Hotel", "price": 250},
        {"name": "Paris Budget Stay", "price": 90},
        {"name": "Paris Central Inn", "price": 130},
    ],
    "new york": [
        {"name": "NYC Skyline Hotel", "price": 220},
        {"name": "NYC Budget Rooms", "price": 75},
        {"name": "Manhattan Suites", "price": 180},
    ],

    "london": [
        {"name": "London Grand Hotel", "price": 83},
        {"name": "London Central Suites", "price": 480},
        {"name": "London Central Suites", "price": 381}
    ],
    "paris": [
        {"name": "Paris Budget Inn", "price": 164},
        {"name": "Paris Central Suites", "price": 149},
        {"name": "Paris Luxury Hotel", "price": 74}
    ],
    "new york": [
        {"name": "New York Grand Hotel", "price": 359},
        {"name": "New York Grand Hotel", "price": 436},
        {"name": "New York Budget Stay", "price": 92}
    ],
    "tokyo": [
        {"name": "Tokyo Grand Hotel", "price": 216},
        {"name": "Tokyo Central Suites", "price": 273},
        {"name": "Tokyo Budget Inn", "price": 137}
    ],
    "dubai": [
        {"name": "Dubai Grand Hotel", "price": 405},
        {"name": "Dubai Budget Stay", "price": 437},
        {"name": "Dubai Luxury Hotel", "price": 402}
    ],
    "sydney": [
        {"name": "Sydney Central Suites", "price": 281},
        {"name": "Sydney Grand Hotel", "price": 146},
        {"name": "Sydney Central Suites", "price": 416}
    ],
    "los angeles": [
        {"name": "Los Angeles Grand Hotel", "price": 363},
        {"name": "Los Angeles Budget Inn", "price": 142},
        {"name": "Los Angeles Central Suites", "price": 282}
    ],
    "berlin": [
        {"name": "Berlin Central Suites", "price": 292},
        {"name": "Berlin Grand Hotel", "price": 258},
        {"name": "Berlin Budget Stay", "price": 204}
    ],
    "mumbai": [
        {"name": "Mumbai Budget Stay", "price": 285},
        {"name": "Mumbai Grand Hotel", "price": 487},
        {"name": "Mumbai Luxury Hotel", "price": 490}
    ],
    "rome": [
        {"name": "Rome Luxury Hotel", "price": 134},
        {"name": "Rome Luxury Hotel", "price": 263},
        {"name": "Rome Grand Hotel", "price": 111}
    ],
    "singapore": [
        {"name": "Singapore Grand Hotel", "price": 328},
        {"name": "Singapore Central Suites", "price": 210},
        {"name": "Singapore Luxury Hotel", "price": 324}
    ],
    "madrid": [
        {"name": "Madrid Luxury Hotel", "price": 413},
        {"name": "Madrid Budget Stay", "price": 265},
        {"name": "Madrid Budget Stay", "price": 243}
    ],
    "amsterdam": [
        {"name": "Amsterdam Grand Hotel", "price": 438},
        {"name": "Amsterdam Grand Hotel", "price": 309},
        {"name": "Amsterdam Grand Hotel", "price": 151}
    ],
    "seoul": [
        {"name": "Seoul Budget Stay", "price": 359},
        {"name": "Seoul Grand Hotel", "price": 102},
        {"name": "Seoul Budget Stay", "price": 409}
    ],
    "bangkok": [
        {"name": "Bangkok Luxury Hotel", "price": 378},
        {"name": "Bangkok Grand Hotel", "price": 287},
        {"name": "Bangkok Budget Inn", "price": 359}
    ]
}

def extract_locations(text):
    # Simple regex-based extraction for demonstration
    cities = [
    "london", "paris", "tokyo", "dubai", "los angeles","mumbai", "rome", "singapore", "amsterdam", "seoul", "bangkok"
]

    found = []
    for city in cities:
        if city in text:
            found.append(city)
    return found

def extract_date(text):
    # Look for patterns like 'on May 20' or 'on 2025-05-20'
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    if date_match:
        return date_match.group(1)
    else:
        # Check for month-day phrases
        months = {
            'january': '01', 'february': '02', 'march': '03', 'april': '04', 'may': '05',
            'june': '06', 'july': '07', 'august': '08', 'september': '09', 'october': '10',
            'november': '11', 'december': '12'
        }
        for month in months.keys():
            if month in text:
                day_match = re.search(r'(\d{1,2})', text)
                if day_match:
                    day = day_match.group(1).zfill(2)
                    year = str(datetime.now().year)
                    return f"{year}-{months[month]}-{day}"
    # fallback today's date
    return datetime.now().strftime("%Y-%m-%d")

def find_flights(departure, destination, date):
    matches = []
    for flight in flights_db:
        if flight['from'] == departure and flight['to'] == destination and flight['date'] == date:
            matches.append(flight)
    return matches

def find_hotels(city, budget):
    available = []
    if city in hotels_db:
        for hotel in hotels_db[city]:
            if hotel['price'] <= budget:
                available.append(hotel)
    return available

def main():
    speak("Welcome to the advanced flight and hotel booking assistant. How can I help you today?")
    
    while True:
        user_text = listen()
        if not user_text:
            continue
        
        # Basic exit condition
        if any(phrase in user_text for phrase in ['exit', 'quit', 'stop']):
            speak("Goodbye! Have a nice day.")
            break
        
        # Extract locations
        locations = extract_locations(user_text)
        if len(locations) >= 2:
            departure = locations[0]
            destination = locations[1]
        else:
            speak("Please tell me your current city and destination.")
            user_text = listen()
            locations = extract_locations(user_text)
            if len(locations) >= 2:
                departure = locations[0]
                destination = locations[1]
            else:
                speak("Sorry, I couldn't get both locations. Please try again.")
                continue
        
        # Extract date
        date = extract_date(user_text)
        
        # Search flights
        flights = find_flights(departure, destination, date)
        if flights:
            speak(f"Found {len(flights)} flights from {departure} to {destination} on {date}:")
            for flight in flights:
                speak(f"Flight {flight['flight_no']} at {flight['time']}")
        else:
            speak(f"Sorry, no flights found from {departure} to {destination} on {date}.")
            continue
        
        # Ask for hotel booking
        speak(f"Do you want to book a hotel in {destination}? Please say yes or no.")
        answer = listen()
        if 'yes' in answer:
            speak("Please tell me your budget for the hotel in dollars.")
            budget_text = listen()
            budget_numbers = re.findall(r'\d+', budget_text)
            if budget_numbers:
                budget = int(budget_numbers[0])
            else:
                budget = 150  # default budget
            
            hotels = find_hotels(destination, budget)
            if hotels:
                speak(f"I found these hotels in {destination} within your budget:")
                for hotel in hotels:
                    speak(f"{hotel['name']} at ${hotel['price']} per night")
            else:
                speak(f"Sorry, no hotels found in {destination} within your budget.")
        else:
            speak("Okay, no hotel booking then.")
        
        speak("Is there anything else I can help you with? Otherwise Say exit to quit.")

if __name__ == "__main__":
    main()

# Book a flight from paris to tokyo on May 19
#My current city is New York, and my destination is London