
import time
import naoqi
from naoqi import ALProxy

tts = ALProxy

ip = "10.60.238.195"

# text to speech proxy
tts = ALProxy("ALTextToSpeech", ip, 9559)

# animated speech proxy
animated_speech = ALProxy("ALAnimatedSpeech", ip, 9559)

# posture proxy
posture_proxy = ALProxy("ALRobotPosture", ip, 9559)

current_posture = posture_proxy.getPosture()

text_old = ""


if current_posture != "Stand":
    # Make NAO stand up
    posture_proxy.goToPosture("StandInit", 1.0)

with open("listen.txt", "w") as f:
    f.write("no")

with open("response.txt", "w") as f:
    f.write(" ")

while True:
    try:
        with open("response.txt", "r") as f:
            text = f.read().replace('\n', ' ')

        # have the NAO speak ChatGPT's response
        if text != "":
            if text != text_old:
                animated_speech.say(text)
                print(text)
                text_old = text
                with open("listen.txt", "w") as f:
                    f.write("yes")
                
        time.sleep(1)
    except Exception as e:
        print("An error occurred: ", e)
        time.sleep(1)
