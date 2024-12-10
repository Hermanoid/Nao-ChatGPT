Interactive NAO for Physical Therapy

By: Lucas Niewohner, Alyssa Hanson, Mindy Garner, and Eddie Voss

---

This code runs an interactive loop on the Nao Robot (in python2) that plays animations and takes in data, which is consumed by ChatGPT (in python3) to generate a response. This is specialized for physical therapy exercises. To run, complete these steps:

- Install the Scaption example animation on the robot by opening it in Choregraphe and install the application onto the robot (using the installation button in the lower-right corner).
- Create a python2 environment set up with the Nao SDK (no easy task, but it's documented online reasonably well). Then, run the python2 code on the robot with `python2 nao_tts.py`
- Create a python3 environment with SpeechRecognition, PyAudio, and openai (install with `pip install SpeechRecognition PyAudio openai`). Then, run the python3 code on your local machine with `python3 speechOpenAI.py`

This will run an example interaction where the robot talks to the user and asks if they are up for an exercise - and if so, demonstrates it for them.