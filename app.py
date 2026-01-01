import os
import requests
from flask import Flask, request, send_from_directory

app = Flask(__name__)

# --- CONFIGURATION ---
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ADMIN_ID = "7033049440"
CHANNEL_ID = "-1002622160373"
US_NUMBER = "+1 205 628 9755"

def send_tg_msg(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if keyboard:
        payload["reply_markup"] = keyboard
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

# Serve the Game (index.html)
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Handle Incoming SMS from Twilio
@app.route('/sms', methods=['POST'])
def sms_reply():
    from_no = request.form.get('From')
    body = request.form.get('Body')

    # Alert Admin
    admin_msg = f"📩 *NEW USA SMS RECEIVED*\n\n📱 *From:* {from_no}\n💬 *Message:* {body}"
    send_tg_msg(ADMIN_ID, admin_msg)

    # Alert Channel
    channel_msg = f"✅ *NEW ACTIVATION*\n📱 *Number:* {US_NUMBER}\n💬 *Status:* Code delivered to user."
    send_tg_msg(CHANNEL_ID, channel_msg)

    return "OK", 200

# Handle Telegram Commands
@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "OK", 200

    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"].get("text", "").lower().strip()

    if user_text == "/start" or user_text == "/play":
        msg = ("🐺 *ZeroThreat Wolf Clicker* 🐺\n\n"
               "Tap the wolf, complete tasks, and earn a *FREE USA NUMBER*!\n\n"
               "👇 Click the button below to start playing!")

        keyboard = {
            "inline_keyboard": [[
                {"text": "🎮 Play & Earn", "web_app": {"url": "https://usa-sms-bot.onrender.com/"}}
            ]]
        }
        send_tg_msg(chat_id, msg, keyboard)

    elif user_text == "/services":
        msg = ("📦 *ZEROTHREAT STOCK LIST*\n\n"
               "✅ **USA SMS Activation** — $10\n"
               "✅ **Facebook Account** — $15\n"
               "✅ **Google Voice** — $20\n\n"
               "🔥 *Fast Delivery like DHL!* Type /pay to order.")
        send_tg_msg(chat_id, msg)

    elif user_text == "/tools":
        msg = ("🛠️ *ZEROTHREAT PREMIUM TOOLS*\n\n"
               "Download tools to stay active:\n\n"
               "📲 **Talkatone:** [Download](https://shrinkme.click/QQi309)\n"
               "📲 **TextPlus:** [Download](https://shrinkme.click/O8nzKJ)\n"
               "🌐 **VPN:** [Download](https://shrinkme.click/4quG8w)\n\n"
               "⚠️ *Bypass ads to reach download.*")
        send_tg_msg(chat_id, msg)

    elif user_text == "/pay":
        msg = ("💳 *PAYMENT PORTAL*\n\n"
               "🏦 **OPAY:** `7066549677` (Chisom Emmanuel)\n"
               "☀️ **SOL:** `8dtuyskTtsB78DFDPWZszarvDpedwftKYCoMdZwjHbxy`\n"
               "💎 **ETH:** `0x20d2708acd360cd0fd416766802e055295470fc1`\n\n"
               "📸 *Send receipt to @Lona_trit!*")
        send_tg_msg(chat_id, msg)

    return "OK", 200

if __name__ == "__main__":
    # Ensure port is handled for Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

