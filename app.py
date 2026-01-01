import os
import requests
from flask import Flask, request

app = Flask(__name__)

# --- CONFIGURATION ---
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ADMIN_ID = "7033049440"  # Your ID from @userinfobot
US_NUMBER = "+12056289755"

# --- TWILIO SMS WEBHOOK ---
@app.route('/sms', methods=['POST'])
def sms_reply():
    from_no = request.form.get('From')
    body = request.form.get('Body')

    # Sends the incoming USA SMS directly to your Telegram
    payload = {
        "chat_id": ADMIN_ID,
        "text": f"📩 *NEW USA SMS RECEIVED*\n\n📱 *From:* {from_no}\n💬 *Message:* {body}",
        "parse_mode": "Markdown"
    }
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json=payload)
    return "OK", 200

# --- TELEGRAM COMMANDS WEBHOOK ---
@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            msg = (
                "🇺🇸 *ICEGODS USA ACTIVATION*\n\n"
                "Get a private US number for WhatsApp/Telegram.\n"
                "💵 *Price:* $10 USDT (or equivalent Naira)\n\n"
                "Type /pay to get payment details."
            )
            send_tg_msg(chat_id, msg)

        elif text == "/pay":
            pay_msg = (
                "💳 *PAYMENT METHODS*\n\n"
                "💰 *Amount:* $10 USDT\n"
                "--------------------------\n"
                "🏦 *OPAY (Naira):* `7066549677` \n"
                "👤 *NAME:* Chisom Emmanuel Boniface\n\n"
                "☀️ *SOLANA (USDT):* \n`8dtuyskTtsB78DFDPWZszarvDpedwftKYCoMdZwjHbxy`\n\n"
                "💎 *ETH (USDT):* \n`0x20d2708acd360cd0fd416766802e055295470fc1`\n"
                "--------------------------\n\n"
                "✅ *After payment, send your receipt to @Lona_trit to receive your number.*"
            )
            send_tg_msg(chat_id, pay_msg)

    return "OK", 200

def send_tg_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

@app.route('/')
def home():
    return "IceGods Sales Bot is Online", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

