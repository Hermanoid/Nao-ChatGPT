import time
import naoqi
from naoqi import ALProxy

tts = ALProxy

# text to speech proxy
tts = ALProxy("ALTextToSpeech", "10.60.198.90", 9559)

# animated speech proxy
animated_speech = ALProxy("ALAnimatedSpeech", "10.60.198.90", 9559)
text_old = ""

# posture proxy
posture_proxy = ALProxy("ALRobotPosture",  "10.60.198.90", 9559)

# Make NAO stand up
posture_proxy.goToPosture("StandInit", 1.0)

while True:
    try:
        with open("C:\\venvProjects\\projectIshani\\flask-server\\response.txt", "r") as f:
            text = f.read().replace('\n', ' ')

        # have the NAO speak ChatGPT's response
        if text != "":
            if text != text_old:
                animated_speech.say(text)
                print(text)
                text_old = text
                
        time.sleep(1)
    except Exception as e:
        print("An error occurred: ", e)
        time.sleep(1)
