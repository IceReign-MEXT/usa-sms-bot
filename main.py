import os, telebot, requests, time, threading
from telebot import types
from flask import Flask

# --- CONFIGURATION ---
TOKEN = os.environ.get('BOT_TOKEN')
SIM_TOKEN = os.environ.get('SIM_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '7033049440'))
CHANNEL_ID = os.environ.get('CHANNEL_ID')
ADMIN_USER = os.environ.get('ADMIN_USERNAME', '@Lona_trit')

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- WEB SERVER (Required for Render) ---
@app.route('/')
def health_check():
    return "Sovereign Shop is Live", 200

# --- STOCK LOGIC ---
def get_stock(filename):
    if not os.path.exists(filename): return None
    with open(filename, 'r') as f:
        lines = f.readlines()
    if not lines: return None
    item = lines[0].strip()
    with open(filename, 'w') as f:
        f.writelines(lines[1:])
    return item

# --- 5SIM LOGIC ---
def buy_num(prod):
    url = f'https://5sim.net/v1/user/buy/activation/usa/any/{prod}'
    headers = {'Authorization': f'Bearer {SIM_TOKEN}', 'Accept': 'application/json'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return r.json()
    except: return None

def check_sms(oid):
    url = f'https://5sim.net/v1/user/check/{oid}'
    headers = {'Authorization': f'Bearer {SIM_TOKEN}', 'Accept': 'application/json'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return r.json().get('sms')
    except: return None

# --- BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def welcome(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛍 Shop Services", "💳 Deposit")
    kb.add("👤 Profile", "📞 Support")
    bot.send_message(m.chat.id, "🐺 *Sovereign V15 Store* 🐺\n\nAutomated USA Numbers & Aged Accounts.", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "🛍 Shop Services")
def shop(m):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("📲 WhatsApp USA - $10", callback_data="buy_wa"),
           types.InlineKeyboardButton("👤 Facebook Aged - $15", callback_data="buy_fb"))
    bot.send_message(m.chat.id, "🛒 *Select Product:*", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "💳 Deposit")
def deposit(m):
    bot.send_message(m.chat.id, f"💳 *PAYMENT*\n\n🏦 OPAY: \n\n📸 Send receipt screenshot here!")

@bot.message_handler(content_types=['photo'])
def receipt(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Appr WhatsApp", callback_data=f"ap_wa_{m.chat.id}"),
           types.InlineKeyboardButton("✅ Appr Facebook", callback_data=f"ap_fb_{m.chat.id}"))
    bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    bot.send_message(ADMIN_ID, "New Receipt! Release product?", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    data = call.data.split('_')
    if data[0] == "ap":
        prod, uid = data[1], data[2]
        if prod == "wa":
            res = buy_num("whatsapp")
            if res and 'phone' in res:
                bot.send_message(uid, f"✅ *Appr!* Number: \nWaiting for SMS...")
                for _ in range(15):
                    time.sleep(10)
                    sms = check_sms(res['id'])
                    if sms:
                        bot.send_message(uid, f"📩 *CODE:* ")
                        return
                bot.send_message(uid, "❌ SMS Timeout. Contact Admin.")
        elif prod == "fb":
            acc = get_stock("fb_stock.txt")
            if acc: bot.send_message(uid, f"✅ *Appr!* Login:\n")
            else: bot.send_message(uid, "❌ Stock Empty! Admin will send manually.")

# --- RUNNER ---
def run_bot():
    while True:
        try:
            bot.polling(none_stop=True, interval=2, timeout=20)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    # Start bot in background
    threading.Thread(target=run_bot, daemon=True).start()
    # Start web server
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
