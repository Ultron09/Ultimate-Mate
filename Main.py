import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from env1 import GeminiKey
genai.configure(api_key=GeminiKey)
from roles import Characters 
from roles import RamayanaCharacters
Role = Characters.Financial_Advisor

def create_chat():
   
    model = genai.GenerativeModel("gemini-1.5-pro")
    chat = model.start_chat(history=[
        {"role": "user", "parts": [Role]}
    ])
    return chat


chat = create_chat()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_with_gemini():
    global chat
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    response = chat.send_message(user_message)
    return jsonify({"reply": response.text})

@app.route('/update_instruction', methods=['POST'])
def update_instruction():
    global instruction, chat
    instruction = request.json.get("instruction", "")
    chat = create_chat()
    return jsonify({"message": "Instruction updated successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
