import os
import requests
from flask import Flask, request

app = Flask(__name__)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Forbidden", 403

    if request.method == "POST":
        data = request.get_json()
        print("Incoming:", data)
        
        try:
            # Extract sender number and message text
            entry = data["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]
            if "messages" in value:
                message = value["messages"][0]
                from_number = message["from"]
                msg_body = message["text"]["body"]
                print(f"Message from {from_number}: {msg_body}")
                
                # Send reply back
                send_message(from_number, f"You said: {msg_body}")
        except Exception as e:
            print("Error:", e)
        
        return "OK", 200

def send_message(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    app.run(debug=True)
