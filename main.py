import os
import time
import eel

from engine.features import *
from engine.command import *
from engine.auth import recoganize

# Load user's name from users.txt
def get_user_name():
    try:
        with open('users.txt', 'r') as f:
            name = f.readline().strip()
            return name if name else "Sir"
    except:
        return "Sir"

# Initialize Eel
eel.init("www")

#playAssistantSound()

@eel.expose
def init():
    eel.hideLoader()
    speak("Ready for Face Authentication")

    flag = recoganize.AuthenticateFace()
    user_name = get_user_name()

    if flag == 1:
        eel.hideFaceAuth()
        speak("Face Authentication Successful")
        eel.hideFaceAuthSuccess()
        speak(f"Hello, Welcome {user_name}, How can I Help You")
        eel.hideStart()
        playAssistantSound()
    else:
        speak("Face Authentication Failed")
        time.sleep(6)
        eel.showFaceAuthFailMsg()

# Launch the app
os.system('start msedge.exe --app="http://localhost:8000/index.html"')

eel.start('index.html', mode=None, host='localhost', block=True)
