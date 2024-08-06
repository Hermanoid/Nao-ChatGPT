import time
import naoqi
from naoqi import ALProxy


tts = ALProxy

ip = "10.60.198.90"

# text to speech proxy
tts = ALProxy("ALTextToSpeech", ip, 9559)

# animated speech proxy
animated_speech = ALProxy("ALAnimatedSpeech", ip, 9559)


# posture proxy
posture_proxy = ALProxy("ALRobotPosture",  ip, 9559)

current_posture = posture_proxy.getPosture()

if current_posture != "Stand":
    # Make NAO stand up
    posture_proxy.goToPosture("StandInit", 1.0)

try:
    with open("C:\\path\\to\\your\\folder\\response.txt", "r") as f:
        text = f.read().replace('\n', ' ')
    animated_speech.say(text)
except Exception as e:
    print("An error ocurred: ", e)
