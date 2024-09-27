
import time
import naoqi
from naoqi import ALProxy

tts = ALProxy

ip = "10.60.210.179"

# text to speech proxy
tts = ALProxy("ALTextToSpeech", ip, 9559)

# animated speech proxy
animated_speech = ALProxy("ALAnimatedSpeech", ip, 9559)

# posture proxy
posture_proxy = ALProxy("ALRobotPosture", ip, 9559)

moodService = ALProxy("ALMood", ip, 9559)

current_posture = posture_proxy.getPosture()

text_old = ""


if current_posture != "Stand":
    # Make NAO stand up
    posture_proxy.goToPosture("StandInit", 1.0)

with open("listen.txt", "w") as f:
    f.write("no")

with open("response.txt", "w") as f:
    f.write(" ")

MOOD_INTERVAL = 4
LOOP_DELAY = 0.25

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
                
        time.sleep(LOOP_DELAY)
        
        moooooood = moodService.currentPersonState()
        moooooood_string = "\n".join([str(key) + ": " + str(value) for key, value in moooooood.items()])
        
        with open("mood.txt", "w") as f:
            f.write(moooooood_string)
        
    except Exception as e:
        print("An error occurred: ", e)
        time.sleep(1)
