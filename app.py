import os
from flask import Flask, request
import requests

PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
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
        data = request.get_json()
        handle_message(data)
        return "ok", 200

def handle_message(data):
    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value.get("messages", [])
        if messages:
            msg = messages[0]
            from_number = msg["from"]
            text_body = msg["text"]["body"]
            url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
            headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
            payload = {"messaging_product": "whatsapp", "to": from_number, "text": {"body": f"You said: {text_body}"}}
            requests.post(url, headers=headers, json=payload)
    eexcept Exception as e:
        print("Error:", str(e))
        return "ok"
