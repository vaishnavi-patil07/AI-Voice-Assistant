import pyttsx3
import speech_recognition as sr
import eel
import time
from gtts import gTTS

# Function to handle text-to-speech output
def speak(text):
    try:
        text = str(text)
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices') 
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 174)

        eel.DisplayMessage(text)  # Send message to frontend (for display)
        engine.say(text)  # Convert text to speech
        eel.receiverText(text)  # Send text to frontend (for further use)

        engine.runAndWait()  # Wait for speech to finish
    except Exception as e:
        print(f"Error in speak function: {e}")
        eel.DisplayMessage("Sorry, there was an error in speech synthesis.")

# Function to capture voice command from user
def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            eel.DisplayMessage("Sorry, I didn't hear anything. Please try again.")
            return "Sorry, I didn't hear anything."
        except sr.RequestError as e:
            print(f"Google Speech Recognition service error: {e}")
            eel.DisplayMessage("Sorry, there was an issue with the speech recognition service.")
            return "Sorry, there was an issue with the speech recognition service."
        except Exception as e:
            print(f"Error while listening: {e}")
            eel.DisplayMessage("Sorry, there was an error while listening. Please try again.")
            return "Sorry, there was an error while listening."

    try:
        print('recognizing...')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
        eel.DisplayMessage("Sorry, I couldn't understand what you said.")
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError as e:
        print(f"Google Speech Recognition service error: {e}")
        eel.DisplayMessage("Sorry, there was an issue with the speech recognition service.")
        return "Sorry, there was an issue with the speech recognition service."
    except Exception as e:
        print(f"Error recognizing: {str(e)}")
        eel.DisplayMessage("Sorry, I couldn't understand what you said.")
        return "Sorry, I couldn't understand what you said."

    return query.lower()

# Main function to handle commands and process recognized queries
@eel.expose
def allCommands(message=1):
    print(f"Received message: {message}")

    if message == 1:
        query = takecommand()
        if not query.strip():  # Check if the query is empty
            eel.DisplayMessage("Sorry, I couldn't understand anything.")
            return
        print(f"Recognized query: {query}")
        eel.senderText(query)  # Send recognized query to frontend
    else:
        query = message
        eel.senderText(query)

    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode you want to use: whatsapp or mobile?")
                preferance = takecommand()
                print(f"Preference for contact mode: {preferance}")

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("What message to send?")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again.")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("What message to send?")
                        query = takecommand()

                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'

                    whatsApp(contact_no, query, message, name)

        else:
            from engine.features import chatBot
            chatBot(query)

    except Exception as e:
        print(f"Error in allCommands: {str(e)}")  # Log the exception details
        eel.DisplayMessage("Sorry, an error occurred while processing your command.")
    
    eel.ShowHood()  # Optionally show the "hood" UI after completing command processing
