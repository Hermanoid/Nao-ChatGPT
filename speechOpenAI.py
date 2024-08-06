
import time
import speech_recognition as sr
from openai import OpenAI
import json
import os

# code to figure out the microphone indexes for multi-microphone use
'''
microphones = sr.Microphone.list_microphone_names()
for index, name in enumerate(microphones):
  print(f"Microphone with index {index} and name \"{name}\" found")
'''

openAIKey = os.environ.get("OPENAI_API_KEY")

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the OpenAI client
client = OpenAI(api_key=openAIKey)
MODEL = "gpt-4o"

command = ["python2", "nao_tts.py"]

chat_history = [{"role": "system", "content": "You are a NAO robot that provides appropiate gestures while answering my questions breifly. Provide the response in this example format: Say something ^start(animations/Stand/Gestures/Hey_1) Say something else. "}]


with open("C:\\path\\to\\your\\folder\\history.txt", "w") as f:
	json.dump(chat_history,f)


	
def speak(mic,person):
	while True:
		with sr.Microphone(device_index=mic) as source:
			r.adjust_for_ambient_noise(source)
			print("Listening...")
			audio = r.listen(source)
			print("Stop Listening")
			try:
				text = r.recognize_google(audio)
				print("mic " + str(mic) + " " + person + " said: " + text)

				# read current chat history
				with open("C:\\path\\to\\your\\folder\\history.txt", "r") as f:
					chat_history = json.load(f)


				chat_history.append({'role': 'user', 'content': text})


				completion = client.chat.completions.create(
					model= MODEL,
					messages= chat_history
				)

				response = completion.choices[0].message.content

				print("Assistant: " + response)

				# Add the assistant's response to the chat history
				chat_history.append({"role": "assistant", "content": response})

				# Save the updated chat history back to the file
				with open("C:\\path\\to\\your\\folder\\history.txt", "w") as f:
					json.dump(chat_history, f)

				with open("C:\\path\\to\\your\\folder\\response.txt", "w") as f:
					f.write(response)

				result = subprocess.run(command, capture_output=True, text=True)

			except Exception as e:
				print(f"An error occurred: {e}")
		time.sleep(1)


speak(1,"Human")


