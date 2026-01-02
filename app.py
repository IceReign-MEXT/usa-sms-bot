import os
import requests
import threading
import time
from flask import Flask, request, send_from_directory

app = Flask(__name__)

# --- CONFIGURATION ---
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ADMIN_ID = "7033049440" 
CHANNEL_ID = "-1002622160373"

def send_tg_msg(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if keyboard: 
        payload["reply_markup"] = keyboard
    try:
        requests.post(url, json=payload)
    except:
        pass

# --- AUTO-BROADCASTER (Runs in background) ---
def auto_broadcaster():
    messages = [
        "🔥 *ZeroThreat Intel is ACTIVE!* \nNeed a US Number for WhatsApp? \n👉 Type /pay to order now! 🔌",
        "🎰 *Feeling Lucky?* \nPlay the Wolf Roulette and win a FREE activation! \n👉 Type /play to start.",
        "📦 *STOCK UPDATE:* \nFresh US Facebook Accounts (Aged) just landed! \nDM @Lona_trit to secure yours. 🚀",
        "🛠️ *FREE TOOLS:* \nDon't forget to check /tools for the latest VPN and Talkatone fixes!"
    ]
    i = 0
    while True:
        # Initial wait before the first message
        time.sleep(300) 
        try:
            send_tg_msg(CHANNEL_ID, messages[i % len(messages)])
            i += 1
        except:
            pass

# --- ROUTES ---
@app.route('/')
def home():
    # This serves your Roulette Game (index.html)
    return send_from_directory('.', 'index.html')

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if not data or "message" not in data: 
        return "OK", 200

    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"].get("text", "").lower().strip()

    if user_text == "/start" or user_text == "/play":
        msg = ("🐺 *ZeroThreat Wolf Roulette* 🐺\n\nWin a *FREE USA NUMBER* activation right now!\n\n👇 Click the button below to spin the wheel!")
        keyboard = {
            "inline_keyboard": [[
                {"text": "🎰 Spin to Win", "web_app": {"url": "https://usa-sms-bot.onrender.com/"}}
            ]]
        }
        send_tg_msg(chat_id, msg, keyboard)

    elif user_text == "/services":
        msg = ("📦 *ZEROTHREAT STOCK LIST*\n\n✅ **USA SMS Activation** — $10\n✅ **Facebook Account** — $15\n✅ **Google Voice** — $20\n\n🔥 *Fast Delivery like DHL!* Type /pay to order.")
        send_tg_msg(chat_id, msg)

    elif user_text == "/tools":
        msg = ("🛠️ *ZEROTHREAT PREMIUM TOOLS*\n\n📲 [Talkatone Pro](https://shrinkme.click/QQi309)\n📲 [TextPlus Fixed](https://shrinkme.click/O8nzKJ)\n🌐 [Proton VPN US](https://shrinkme.click/4quG8w)\n\n⚠️ *Bypass ads to reach the download.*")
        send_tg_msg(chat_id, msg)

    elif user_text == "/pay":
        msg = ("💳 *PAYMENT PORTAL*\n\n🏦 **OPAY:** `7066549677` (Chisom Emmanuel)\n☀️ **SOL:** `8dtuyskTtsB78DFDPWZszarvDpedwftKYCoMdZwjHbxy`\n\n📸 *Send receipt to @Lona_trit immediately!*")
        send_tg_msg(chat_id, msg)

    return "OK", 200

if __name__ == "__main__":
    # Start the broadcaster in a separate thread so the bot stays online
    threading.Thread(target=auto_broadcaster, daemon=True).start()
    
    # Run the app on the port provided by Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

