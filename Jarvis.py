"""JAVIS the Iron Man's Assistant."""
import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import openai

# Configure OpenAI API
load_dotenv()
openai.api_key = os.getenv('API_KEY')  # Replace API_KEY to your own.

# Initialize the recognizer
r = sr.Recognizer()


def SpeakText(command):
    """Initialize the engine."""
    engine = pyttsx3.init("nsss")
    engine.setProperty('rate', 125)
    engine.say(command)
    engine.runAndWait()


def record_text():
    """Loop the case of errors."""
    while (True):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)

                print("I'm listening...")

                audio2 = r.listen(source2)
                myText = r.recognize_google(audio2)
                return myText

        except sr.RequestError as e:
            print(f"Could not request results; {e}")

        except sr.UnknownValueError:
            print("Unknow error occurred")


def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    """Send the message to ChatGPT."""
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message


messages = []
send_to_chatGPT(messages)

while (True):
    text = record_text()
    print("You : " + text)
    if (text.lower() == "exit"):
        print("Bye!")
        exit()

    messages.append({"role": "user", "content": text})
    response = send_to_chatGPT(messages)
    print("J.A.V.I.S. : " + response)
    SpeakText(response)
