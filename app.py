from flask import Flask, render_template, request,jsonify
import requests

#API_URL = "https://api-inference.huggingface.co/models/benkimz/agbrain"
#headers = {"Authorization": "Bearer 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"}


API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b-it"
headers = {"Authorization": "Bearer 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"}
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
