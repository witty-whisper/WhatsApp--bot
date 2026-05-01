from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "marvellous2026"
WHATSAPP_TOKEN = "EAActT6o6XZA4BRYdZAsDCCLoZAD8uKZCWrAFr4iGZBngQUYbXJYapTagz8rGJz7ZBldnHZARSdGTO6m2sR4ZAJbDuoKXYuDQOI6F0Mo82JTbmtZA6BvyOvDBDGFsaDQYoVLbZBG5tLyAjd5Sh7ZA1TIMa486NscUzmT60g0TEdOUqJNZBQZAlISS0wqnmUSpwZAiRXQmBAviVktNzLGG5n7HkvI2t5bjhpj7pqTsLhKZCSZAuDnQmG54zX5CuSMytxRBkNhD3UpDMYD9fZBnQwUnwC6ou6cDGtgZDZD" 
PHONE_NUMBER_ID = "1049313231604664"
def verify():
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if verify_token == VERIFY_TOKEN:
        return challenge
    return "Invalid", 403


@app.route('/webhook', methods=['POST'])
def webhook():
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
