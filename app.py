from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "marvellous2026"
WHATSAPP_TOKEN = "EAActT6oXZA4BRYdZAsDCCLoZAD"
PHONE_NUMBER_ID = "1049313231604664"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Meta verification
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if verify_token == VERIFY_TOKEN:
            return challenge, 200
        return "Invalid verify token", 403
    
    # POST = incoming WhatsApp messages
    data = request.json
    if data.get('object') == 'whatsapp_business_account':
        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                if change.get('field') == 'messages':
                    msg = change['value']['messages'][0]
                    sender = msg['from']
                    text = msg['text']['body']
                    requests.post(
                        f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages",
                        headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"},
                        json={"messaging_product": "whatsapp", "to": sender, "text": {"body": f"Echo: {text}"}}
                    )
    return 'OK', 200
