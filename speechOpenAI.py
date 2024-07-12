
import time
import multiprocessing
import speech_recognition as sr
from openai import OpenAI
import json
import os

# code to figure out the microphone indexes for multi-microphone use
'''
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f'{index}, {name}')
'''
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

chat_history = [{"role": "system", "content": "You are a NAO robot that provides appropiate gestures while answering my questions breifly. Provide the response in this example format: Say something ^start(animations/Stand/Gestures/Hey_1) Say something else. "}]
with open("C:\\venvProjects\\projectIshani\\flask-server\\history.txt", "w") as f:
	json.dump(chat_history,f)
	
def speak(mic,person):
	print(person, mic)
	while True:
		with sr.Microphone(device_index=mic) as source:

			r.adjust_for_ambient_noise(source)
			
			print("Listening...")
			audio = r.listen(source)
			print("Stop Listening")
			
			try:
				# using google to transcribe the audio file to text
				text = r.recognize_google(audio)
				print("mic " + str(mic) + " " + person + " said: " + text)

				# read current chat history
				with open("C:\\venvProjects\\projectIshani\\flask-server\\history.txt", "r") as f:
					chat_history = json.load(f)

				# keeps the chat history with ChatGPT
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
				with open("C:\\venvProjects\\projectIshani\\flask-server\\history.txt", "w") as f:
					json.dump(chat_history, f)

				with open("C:\\venvProjects\\projectIshani\\flask-server\\response.txt", "w") as f:
					f.write(response)

			except Exception as e:
				print(f"An error occurred: {e}")
				
		input("press enter to continue")
		print(person, mic)
