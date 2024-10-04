
import time
import naoqi
import qi
from naoqi import ALProxy
import sys

tts = ALProxy

ip = "10.60.227.6"

# text to speech proxy
tts = ALProxy("ALTextToSpeech", ip, 9559)

# animated speech proxy
animated_speech = ALProxy("ALAnimatedSpeech", ip, 9559)

# posture proxy
posture_proxy = ALProxy("ALRobotPosture", ip, 9559)

session = qi.Session()
session.connect("tcp://" + ip + ":9559")
moodService = session.service("ALMood")

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

counter = 0
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
        
        if counter % MOOD_INTERVAL == 0:
            if len(moodService.persons()) == 0:
                print("No one detected")
            else:
                print("YOU ARE BEING PERCEIVED BY YOUR FUTURE AI OVERLORDS")
                curr_mood = moodService.currentPersonState()
                moooooood_string = "\n".join([str(key) + ": " + str(value) for key, value in curr_mood.items()])
            
            # with open("mood.txt", "w") as f:
            #     f.write(moooooood_string)
        counter += 1
        
    except Exception as e:
        print("An error occurred: ", e)
    
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
