import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import os
from PIL import ImageGrab
import wikipedia
import pywhatkit as pwk


engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    engine.setProperty('voice',voice.id)
engine.setProperty("rate",150)
engine.runAndWait()
    
  
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def command():
    content = " "
    while content == " ":   
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            
            audio = r.listen(source)    
            

        try:
            content = r.recognize_google(audio , language = 'en-in')
            print("You Said....." + content)
        except Exception as e:
            print("Please try again...")

    return content

def main_process():
    while True: 
        request = command().lower()
        if "hello" in request:
            speak("Hii sir. I am JARVIS your personal assistant, How can i assist you ")
        elif "how r u" in request:
            speak("I am fine. what about you")
            print("I am fine. what about you")
        elif "play music" in request:
            speak("Wait, i am Playing music")
            song = random.randint(1,3)
            if song == 1:
                webbrowser.open("https://www.youtube.com/watch?v=K4DyBUG242c&list=RDQMTgh66LaGkb4&start_radio=1")
            elif song == 2:
                webbrowser.open("https://www.youtube.com/watch?v=hA8MFZ76Jbc")
            elif song == 3:
                webbrowser.open("https://www.youtube.com/watch?v=WMa-1CQMWCk")
        elif "say time" in request:
            now_time = datetime.datetime.now().strftime("%H:%M")
            speak("Current time is " + str(now_time))
        elif "say date" in request:
            now_date = datetime.datetime.now().strftime("%d:%m")
            speak("Current date is " + str(now_date))
        elif "new task" in request:
            task = request.replace("new task", "")
            task = task.strip()
            if task != "":
                speak("Adding task : "+ task)
                with open ("todo.txt", "a") as file:
                    file.write(task + "\n")    
        elif "tell task" in request:
            with open ("todo.txt","r") as file:
                speak("Work we want to do today is : " + file.read())  
        elif "show work" in request:
            with open ("todo.txt", "r") as file:
                tasks = file.read()
            notification.notify(
                title = "Today's work",
                message = tasks
            )
        elif "delete task" in request:
            task_to_delete = request.replace("delete task", "").strip()
            if task_to_delete:
               if os.path.exists("todo.txt"):
                  with open("todo.txt", "r") as file:
                        tasks = file.readlines()
                  with open("todo.txt", "w") as file:
                        tasks_removed = False
                        for task in tasks:
                            if task.strip() != task_to_delete:
                               file.write(task)
                            else:
                               tasks_removed = True
                        if tasks_removed:
                           speak("Task deleted: " + task_to_delete)
                        else:
                           speak("Task not found: " + task_to_delete)
               else:
                     speak("No tasks found to delete.")
            else:
               speak("Please specify the task you want to delete.")

        elif "open youtube" in request:
            webbrowser.open("www.youtube.com")
            speak("Okay, Please Wait a minute")
        elif "open facebook" in request:
            webbrowser.open("www.facebook.com")
            speak("Okay, Please Wait a minute")
        elif "open instagram" in request:
            webbrowser.open("www.instagram.com")  
            speak("Okay, Please Wait a minute")
        elif "open whatsapp" in request:
            webbrowser.open("https://web.whatsapp.com/")   
            speak("Okay, Please Wait a minute")            


        elif "open" in request:
            query = request.replace("open", "")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")

    

        elif "wikipedia" in request:
            # request = request.replace("Jarvis", "")
            request = request.replace("search on wikipedia", "")
            print(request)
            speak("okay")
            result = wikipedia.summary(request, sentences=3) 
            print(result)
            speak(result)

            
        elif "google" in request:
            request = request.replace("jarvis ", "")
            request = request.replace("search on google ", "")
            print(request)
            speak("Wait a minute i am searching ")
            webbrowser.open("https://www.google.com/search?q=" + request)

        elif "send message" in request:
            pwk.sendwhatmsg("+917696269822", "Hiii, how are you!", 14, 32, 30)
            
 

main_process()