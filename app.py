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
if __name__ == "__main__":
    app.run(debug=True)
