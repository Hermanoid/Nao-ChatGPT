#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: A Simple class to get & read FaceDetected Events"""

import qi
import time
import sys
import argparse
import json


class HumanGreeter(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(HumanGreeter, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.on_human_tracked)
        self.arrive_subscriber = self.memory.subscriber("PeoplePerception/JustArrived")
        self.arrive_subscriber.signal.connect(self.on_arrived)
        self.left_subscriber = self.memory.subscriber("PeoplePerception/JustLeft")
        self.left_subscriber.signal.connect(self.on_left)
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = session.service("ALTextToSpeech")
        self.face_detection = session.service("ALFaceDetection")
        self.face_detection.subscribe("HumanGreeter")
        self.got_face = False
        self.hold_for_response = False
        self.people_names = {}
        
    def wait_for_response(self, prompt):
        self.hold_for_response = True
        to_return = None
        with open("listen.txt", "w") as f:
            f.write(prompt)
        while True:
            with open("response.txt", "r") as f:
                result = f.read()
            if result != "":
                to_return = result
                with open("response.txt", "w") as f:
                    f.write("")
                break
            time.sleep(0.1)
        self.hold_for_response = False
        return to_return
        
    def on_arrived(self, value):
        print("Someone arrived: ", value)
        # print(event, id, sub_id)
        self.tts.say("Howdy, Stranger")
        if self.hold_for_response:
            return
        self.tts.say("What is your name?")
        response = self.wait_for_response("name")
        self.people_names[value] = response
        
        
        
    def on_left(self, value):
        if value in self.people_names:
            self.tts.say("Goodbye, " + self.people_names[value])
        else:
            self.tts.say("Goodbye, Stranger")
        
    

    def on_human_tracked(self, value):
        """
        Callback for event FaceDetected.
        """
        if value == []:  # empty value when the face disappears
            self.got_face = False
        elif not self.got_face:  # only speak the first time a face appears
            self.got_face = True
            print "I saw a face!"
            # self.tts.say("Hello, you!")
            # First Field = TimeStamp.
            timeStamp = value[0]
            # print "TimeStamp is: " + str(timeStamp)

            # Second Field = array of face_Info's.
            faceInfoArray = value[1]
            for j in range( len(faceInfoArray)-1 ):
                faceInfo = faceInfoArray[j]

                # First Field = Shape info.
                faceShapeInfo = faceInfo[0]

                # Second Field = Extra info (empty for now).
                faceExtraInfo = faceInfo[1]

                # print "Face Infos :  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
                # print "Face Infos :  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])
                # print "Face Extra Infos :" + str(faceExtraInfo)

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting HumanGreeter"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping HumanGreeter"
            self.face_detection.unsubscribe("HumanGreeter")
            app.stop()
            del self.memory
            del self.tts
            del self.face_detection
            del self.left_subscriber
            del self.arrive_subscriber
            del self.subscriber
            #stop
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="10.60.238.195",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["HumanGreeter", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    human_greeter = HumanGreeter(app)
    human_greeter.run()