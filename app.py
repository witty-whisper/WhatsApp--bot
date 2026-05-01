import os
from flask import Flask, request

app = Flask(__name__)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Meta verification: check token and return challenge
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        return "Forbidden", 403
    
    if request.method == 'POST':
        # Handle incoming WhatsApp messages
        data = request.get_json()
        print(data)  # You can remove this later
        return "OK", 200
