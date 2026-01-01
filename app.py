import os
import requests
from flask import Flask, request

app = Flask(__name__)

# --- CONFIGURATION ---
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ADMIN_ID = "7033049440"
CHANNEL_ID = "-1002622160373"
US_NUMBER = "+1 205 628 9755"

def send_tg_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Error: {e}")

@app.route('/sms', methods=['POST'])
def sms_reply():
    from_no = request.form.get('From')
    body = request.form.get('Body')
    admin_msg = f"📩 *NEW USA SMS RECEIVED*\n\n📱 *From:* {from_no}\n💬 *Message:* {body}"
    send_tg_msg(ADMIN_ID, admin_msg)
    channel_msg = f"✅ *NEW ACTIVATION*\n📱 *Number:* {US_NUMBER}\n💬 *Status:* Code delivered."
    send_tg_msg(CHANNEL_ID, channel_msg)
    return "OK", 200

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "OK", 200

    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"].get("text", "").lower().strip()

    if user_text == "/start":
        msg = ("🛡️ *ZeroThreat Intel System*\n\n"
               "Premium US Numbers & Facebook Accounts.\n\n"
               "👉 /services - View Price List\n"
               "👉 /pay - How to Buy\n"
               "👉 /help - How to use")
        send_tg_msg(chat_id, msg)

    elif user_text == "/services":
        msg = ("🛒 *ZEROTHREAT SERVICES*\n\n"
               "1️⃣ **USA SMS Activation** — $10\n"
               "   _For WhatsApp, TG, or Google._\n\n"
               "2️⃣ **Fresh US Facebook Account** — $15\n"
               "   _Made with US IP + US Number._\n\n"
               "3️⃣ **Aged FB Account (2018-2021)** — $30\n"
               "   _High trust for Ads/Marketplace._\n\n"
               "👉 Type /pay to order.")
        send_tg_msg(chat_id, msg)

    elif user_text == "/pay":
        msg = ("💳 *PAYMENT METHODS*\n\n"
               "🏦 **OPAY:** `7066549677` (Chisom Emmanuel Boniface)\n"
               "☀️ **SOLANA:** `8dtuyskTtsB78DFDPWZszarvDpedwftKYCoMdZwjHbxy`\n"
               "💎 **ETH:** `0x20d2708acd360cd0fd416766802e055295470fc1`\n\n"
               "✅ *Send receipt to @Lona_trit*")
        send_tg_msg(chat_id, msg)

    elif user_text == "/help":
        msg = (f"❓ *HOW IT WORKS*\n\n"
               f"1. Choose a service in /services\n"
               f"2. Pay and DM receipt to @Lona_trit\n"
               f"3. For SMS: Use `{US_NUMBER}`\n"
               f"4. For FB: We send you login details.")
        send_tg_msg(chat_id, msg)

    return "OK", 200

@app.route('/')
def home():
    return "ZeroThreat Pro Active", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

