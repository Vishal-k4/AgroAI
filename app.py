from flask import Flask, render_template, request,jsonify
import requests
from deep_translator import GoogleTranslator
#from dotenv import load_dotenv
from langdetect import detect
import os
#load_dotenv()
#API_URL = "https://api-inference.huggingface.co/models/benkimz/agbrain"
#headers = {"Authorization": "Bearer xxxxxxxxxxxxxxxxxxxx"}
API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b-it"
headers = {"Authorization": "Bearer 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"}

#API_URL = os.getenv("API_URL")
#headers=os.getenv('headers')
app = Flask(__name__)
translator = GoogleTranslator(source='auto', target='en')




def translate_text_with_special_chars(text, target_language):
    # Replace special characters with unique placeholders
    special_chars = {'\n': '||newline||'}  # You can add more special characters as needed
    for char, placeholder in special_chars.items():
        text = text.replace(char, placeholder)

    # Translate text
    translation = translator.translate(text, target_language=target_language)

    # Restore special characters
    for char, placeholder in special_chars.items():
        translation = translation.replace(placeholder, char)

    return translation

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def get_response_from_chatbot(text):
    #user_language = detect(text)
    #translator = GoogleTranslator(source='auto', target=user_language)
    user_input_en = translate_text_with_special_chars(text, target_language='en')
    output = query({"inputs": user_input_en})
    bot_response = output[0]['generated_text']
    #bot_response = translator.translate(bot_response_en, target_language=user_language)

    bot_response = bot_response.replace('**', '<b>')
    bot_response = bot_response.replace('**', '</b>')  # Closing tag
    bot_response = bot_response.replace('*', ' ')
    return bot_response

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    user_language = detect(user_input)
    translator = GoogleTranslator(source='auto', target=user_language)
    user_input_en = translate_text_with_special_chars(user_input, target_language='en')
    output = query({"inputs": user_input_en})
    bot_response_en = output[0]['generated_text']
    bot_response = translator.translate(bot_response_en, target_language=user_language)
    return jsonify({'bot_response': bot_response})
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
       import speech_recognition as sr

       def recognize_speech():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)

                #Capture the audio input from the user
                audio = recognizer.listen(source,timeout=10)

            try:
                print("Recognizing speech...")
                recognized_text = recognizer.recognize_google(audio)
                print("Speech recognized:", recognized_text)
                return recognized_text
            except sr.UnknownValueError:
                print("Speech could not be understood")
                return None
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return None

        # Call the function to recognize speech and get the recognized text

       recognized_text = recognize_speech()
       bot_response = get_response_from_chatbot(recognized_text)  # Call your chatbot function
       return jsonify({'bot_response': bot_response})
    except Exception as e:
        print('Error during speech-to-text:', str(e))
        return jsonify({'bot_response': 'Sorry i could not catch up, can you please say again'})
if __name__ == "__main__":
    app.run(debug=True)
