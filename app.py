from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Credentials from Render's Environment Variables
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

@app.route("/", methods=['GET'])
def home():
    return "<h1>USA Business System is Online.</h1><p>Ready to receive codes.</p>"

@app.route("/sms", methods=['POST'])
def sms_webhook():
    sender = request.form.get('From', 'Unknown')
    body = request.form.get('Body', 'No Content')
    
    # This is what you see in Telegram
    alert = f"🇺🇸 **NEW USA CODE!**\n\n📱 **From:** {sender}\n💬 **Message:** {body}"
    send_to_telegram(alert)
    
    return "<Response></Response>", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
