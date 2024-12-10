
import time
import qi
from naoqi import ALProxy
import sys
import re

tts = ALProxy

ip = "10.60.63.63"

# text to speech proxy
tts = ALProxy("ALTextToSpeech", ip, 9559)

# animated speech proxy
animated_speech = ALProxy("ALAnimatedSpeech", ip, 9559)

# posture proxy
posture_proxy = ALProxy("ALRobotPosture", ip, 9559)

tracker_proxy = ALProxy("ALTracker", ip, 9559)

session = qi.Session()
session.connect("tcp://" + ip + ":9559")
mood_service = session.service("ALMood")

current_posture = posture_proxy.getPosture()

text_old = ""

look_actions = {   
    "LOOK_AT_USER": [0, 0, 0.5],
    "LOOK_RIGHT": [0, -1, 0.5],
    "LOOK_LEFT": [0, 1, 0.5],
    "LOOK_UP": [1, 0, 3],
    "LOOK_DOWN": [1, 0, 0],
}

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
                segments_to_say = re.split("|".join(look_actions.keys()), text)
                look_commands = re.findall("|".join(look_actions.keys()), text)
                print(segments_to_say, look_commands)
                for i, segment in enumerate(segments_to_say):
                    segment = segment.strip()
                    # Remove punctuation at the start of the segment only
                    if len(segment)>0 and segment[0] in [".", ",", "!", "?"]:
                        segment = segment[1:]
                    if segment != "":
                        animated_speech.say(segment)
                    if i < len(look_commands):
                        look_location = look_actions[look_commands[i]]
                        print(look_location)
                        tracker_proxy.lookAt(look_location, 2, 0.4, False)
                print(text)
                text_old = text
                with open("listen.txt", "w") as f:
                    f.write("yes")
                
        time.sleep(LOOP_DELAY)
        
        if counter % MOOD_INTERVAL == 0:
            if len(mood_service.persons()) == 0:
                print("No one detected")
            else:
                print("Person detected, getting mood")
                curr_mood = mood_service.currentPersonState()
                mood_string = "\n".join([str(key) + ": " + str(value) for key, value in curr_mood.items()])
            
        counter += 1
        
    except Exception as e:
        print("An error occurred: ", e)
    
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
