import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ADMIN_ID = "7033049440"
CHANNEL_ID = "-1002622160373"
US_NUMBER = "+1 205 628 9755"

def send_tg_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if not data or "message" not in data: return "OK", 200
    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"].get("text", "").lower().strip()

    if user_text == "/start":
        msg = ("🛡️ *ZeroThreat Intel: The Reliable Plug* 🔌\n\n"
               "Back-to-back drops! USA/UK Numbers & FB Verification.\n\n"
               "👉 /services - See the Plug Menu\n"
               "👉 /pay - Get Account Details\n"
               "👉 /help - How to get your code")
        send_tg_msg(chat_id, msg)

    elif user_text == "/services":
        msg = ("📦 *ZEROTHREAT STOCK LIST*\n\n"
               "✅ **USA/UK SMS Drop** — $10\n"
               "✅ **Facebook Verification** — $15\n"
               "✅ **Google Voice (GV)** — $20\n"
               "✅ **Talkatone / TextPlus** — DM\n"
               "✅ **Premium eSIMs** — DM\n\n"
               "🔥 *Fast Delivery like DHL!* Type /pay to order.")
        send_tg_msg(chat_id, msg)

    elif user_text == "/pay":
        msg = ("💳 *PAYMENT PORTAL*\n\n"
               "🏦 **OPAY:** `7066549677` (Chisom Emmanuel Boniface)\n"
               "☀️ **SOLANA:** `8dtuyskTtsB78DFDPWZszarvDpedwftKYCoMdZwjHbxy`\n"
               "💎 **ETH:** `0x20d2708acd360cd0fd416766802e055295470fc1`\n\n"
               "📸 *Send receipt to @Lona_trit immediately!*")
        send_tg_msg(chat_id, msg)

    return "OK", 200

@app.route('/')
def home(): return "Plug Online", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

