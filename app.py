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
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if not data or "message" not in data: return "OK", 200
    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"].get("text", "").lower().strip()

    if user_text == "/start":
        msg = ("🛡️ *ZeroThreat Intel: Premium Plug* 🔌\n\n"
               "Back-to-back drops! USA Numbers & FB Accounts ready.\n\n"
               "👉 /services - Price List\n"
               "👉 /tools - Free Download Links\n"
               "👉 /pay - Buy Now")
        send_tg_msg(chat_id, msg)

    elif user_text == "/services":
        msg = ("📦 *ZEROTHREAT STOCK LIST*\n\n"
               "✅ **USA SMS Activation** — $10\n"
               "✅ **Facebook Account** — $15\n"
               "✅ **Google Voice** — $20\n"
               "🔥 *Fast Delivery like DHL!* Type /pay to order.")
        send_tg_msg(chat_id, msg)

    elif user_text == "/tools":
        msg = ("🛠️ *ZEROTHREAT PREMIUM TOOLS*\n\n"
               "Download the tools to keep your numbers 100% active:\n\n"
               "📲 **Talkatone Pro:**\n"
               "👉 [Download Here](https://shrinkme.click/QQi309)\n\n"
               "📲 **TextPlus Fixed:**\n"
               "👉 [Download Here](https://shrinkme.click/O8nzKJ)\n\n"
               "🌐 **Proton VPN (US IP):**\n"
               "👉 [Download Here](https://shrinkme.click/4quG8w)\n\n"
               "⚠️ *Note: Bypass ads to reach the download.*")
        send_tg_msg(chat_id, msg)

    elif user_text == "/pay":
        msg = ("💳 *PAYMENT PORTAL*\n\n"
               "🏦 **OPAY:** `7066549677` (Chisom Emmanuel)\n"
               "☀️ **SOL:** `8dtuyskTtsB78DFDPWZszarvDpedwftKYCoMdZwjHbxy`\n"
               "💎 **ETH:** `0x20d2708acd360cd0fd416766802e055295470fc1`\n\n"
               "📸 *Send receipt to @Lona_trit immediately!*")
        send_tg_msg(chat_id, msg)

    return "OK", 200

@app.route('/')
def home(): return "Plug Online", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

