import os
import requests
from flask import Flask, request

app = Flask(__name__)

# --- CONFIGURATION ---
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ADMIN_ID = "7033049440"
US_NUMBER = "+12056289755"

def send_tg_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

# --- TWILIO SMS WEBHOOK ---
@app.route('/sms', methods=['POST'])
def sms_reply():
    from_no = request.form.get('From')
    body = request.form.get('Body')
    msg = f"📩 *NEW USA SMS RECEIVED*\n\n📱 *From:* {from_no}\n💬 *Message:* {body}"
    send_tg_msg(ADMIN_ID, msg)
    return "OK", 200

# --- TELEGRAM COMMANDS WEBHOOK ---
@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            msg = "🇺🇸 *ICEGODS USA ACTIVATION*\n\nGet a private US number.\n💵 *Price:* $10 USDT / ~15,000 NGN\n\nType /pay for details."
            send_tg_msg(chat_id, msg)

        elif text == "/pay":
            pay_msg = ("💳 *PAYMENT METHODS*\n\n💰 *Amount:* $10\n"
                       "🏦 *OPAY:* `7066549677` (Chisom Emmanuel Boniface)\n"
                       "☀️ *SOL:* `8dtuyskTtsB78DFDPWZszarvDpedwftKYCoMdZwjHbxy`\n"
                       "💎 *ETH:* `0x20d2708acd360cd0fd416766802e055295470fc1`\n\n"
                       "✅ Send receipt to @Lona_trit to get your number.")
            send_tg_msg(chat_id, pay_msg)

        elif text == "/help":
            help_msg = "❓ *HELP*\n1. Pay $10.\n2. Message @Lona_trit with receipt.\n3. Use number `+1 205 628 9755`.\n4. Code appears here!"
            send_tg_msg(chat_id, help_msg)

        elif text == "/terms":
            terms_msg = "⚖️ *TERMS*\n- Payment for 1 successful code.\n- No refunds for banned social media accounts.\n- Support: @Lona_trit"
            send_tg_msg(chat_id, terms_msg)

    return "OK", 200

@app.route('/')
def home():
    return "IceGods Online", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

