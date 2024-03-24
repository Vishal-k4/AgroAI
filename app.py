from flask import Flask, render_template, request,jsonify
import requests
from dotenv import load_dotenv
import os
load_dotenv()
#API_URL = "https://api-inference.huggingface.co/models/benkimz/agbrain"
#headers = {"Authorization": "Bearer xxxxxxxxxxxxxxxxxxxx"}

API_URL = os.getenv("API_URL")
headers=os.getenv('headers')
app = Flask(__name__)


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

@app.route("/")
def home():
    return render_template("index.html")
@app.route('/query', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    output = query({"inputs": user_input})
    bot_response = output
    return jsonify({'bot_response': bot_response})
if __name__ == "__main__":
    app.run(debug=True)
