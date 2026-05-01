handler = app import os
import requests
from flask import Flask, request

app = Flask(__name__)

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

@app.route("/", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/", methods=["POST"])
def webhook():
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
            if msg.get("type") == "text":
                from_number = msg["from"]
                text_body = msg["text"]["body"]
                
                url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
                headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
                payload = {
                    "messaging_product": "whatsapp", 
                    "to": from_number, 
                    "text": {"body": f"You said: {text_body}"}
                }
                r = requests.post(url, headers=headers, json=payload)
                print("WhatsApp API response:", r.status_code, r.text) # <-- this is for debugging
    except Exception as e:
        print("Error:", str(e))
    return "ok"

if __name__ == "__main__":
    app.run()
handler = app
