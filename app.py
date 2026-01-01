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
        print(f"Error sending message: {e}")

# --- TWILIO SMS WEBHOOK ---
@app.route('/sms', methods=['POST'])
def sms_reply():
    from_no = request.form.get('From')
    body = request.form.get('Body')

    # Send to YOU
    admin_msg = f"📩 *NEW USA SMS RECEIVED*\n\n📱 *From:* {from_no}\n💬 *Message:* {body}"
    send_tg_msg(ADMIN_ID, admin_msg)

    # Send Proof to Channel
    channel_msg = f"✅ *SUCCESSFUL ACTIVATION*\n📱 *Number:* {US_NUMBER}\n💬 *Status:* Code delivered to user."
    send_tg_msg(CHANNEL_ID, channel_msg)

    return "OK", 200

# --- TELEGRAM COMMANDS WEBHOOK ---
@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "OK", 200

    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"].get("text", "").lower().strip()

    if user_text == "/start":
        msg = (f"🛡️ *ZeroThreat Intel: USA SMS System*\n\n"
               f"Welcome! We provide premium US numbers for verification.\n\n"
               f"💵 *Price:* $10 USDT / ~15,500 NGN\n\n"
               f"👉 Use /pay for account details\n"
               f"👉 Use /help for instructions")
        send_tg_msg(chat_id, msg)

    elif user_text == "/pay":
        pay_msg = ("💳 *PAYMENT METHODS (ZeroThreat)*\n\n"
                   "🏦 **OPAY (Naira):** `7066549677` \n"
                   "👤 **Name:** Chisom Emmanuel Boniface\n\n"
                   "☀️ **SOLANA (USDT):** \n`8dtuyskTtsB78DFDPWZszarvDpedwftKYCoMdZwjHbxy`\n\n"
                   "💎 **ETH (USDT):** \n`0x20d2708acd360cd0fd416766802e055295470fc1`\n\n"
                   "✅ *Send receipt to @Lona_trit to receive your number.*")
        send_tg_msg(chat_id, pay_msg)

    elif user_text == "/help":
        help_msg = (f"❓ *HOW TO USE THE SYSTEM*\n\n"
                    f"1. Type /pay and choose a method.\n"
                    f"2. Pay $10 and DM receipt to @Lona_trit.\n"
                    f"3. Use number: `{US_NUMBER}` in your app.\n"
                    f"4. The 6-digit code will appear in this chat.")
        send_tg_msg(chat_id, help_msg)

    elif user_text == "/terms":
        terms_msg = ("⚖️ *TERMS OF SERVICE*\n\n"
                     "• Each payment covers one successful code.\n"
                     "• Numbers are private and high-quality.\n"
                     "• Support: @Lona_trit\n"
                     "• Updates: @ZeroThreatIntel")
        send_tg_msg(chat_id, terms_msg)

    return "OK", 200

@app.route('/')
def home():
    return "ZeroThreat Pro Online", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

