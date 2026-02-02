import os, telebot, requests, time, threading
from telebot import types
from flask import Flask

# ---It looks like when CONFIGURATION ---
TOKEN = os.environ.get('BOT_TOKEN')
SIM_TOKEN = os.environ you tried to copy and paste the code, Termux tried to run the Python code as if it were Bash commands. This happened.get('SIM_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID', because of the way `$PORT` and other variables were handled.

Let's fix this properly. We will do it '7033049440'))
CHANNEL_ID = os.environ.get('CHANNEL file by file with a **safe** method that won't cause "command not found" errors.

### 1. Fix_ID')
ADMIN_USER = os.environ.get('ADMIN_USERNAME', '@Lona_trit')

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Sovereign Shop is Live", 20 `main.py`
Run this command exactly. I have added quotes to `'EOF'` which tells Termux **not** to run the code, just save it.

```bash
cat <<'EOF' > main.py
0

def get_stock(filename):
    if not os.path.exists(filename): return None
    with openimport os, telebot, requests, time, threading
from telebot import types
from flask import Flask

#(filename, 'r') as f:
        lines = f.readlines()
    if not lines: return None
    item = lines[0].strip()
    with open(filename, 'w') as f:
        f.writelines(lines[1:])
    return item

def buy_num(prod):
     --- CONFIGURATION ---
TOKEN = os.environ.get('BOT_TOKEN')
SIM_TOKEN = os.environ.get('SIM_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID',url = f'https://5sim.net/v1/user/buy/activation/usa/any/{ '7033049440'))
CHANNEL_ID = os.environ.get('CHANNELprod}'
    headers = {'Authorization': f'Bearer {SIM_TOKEN}', 'Accept': 'application/json_ID')
ADMIN_USER = os.environ.get('ADMIN_USERNAME', '@Lona_trit'}
    try:
        r = requests.get(url, headers=headers, timeout=10)')

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Sovereign Shop is Live", 2
        return r.json()
    except: return None

def check_sms(oid):
    url = f'https://5sim.net/v1/user/check/{oid}'
    headers = {'Authorization': f'Bearer {SIM_TOKEN}', 'Accept': 'application/json'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return r.json().get('sms')
    except: return None

@bot.message_handler(commands=['start'])
def00

def get_stock(filename):
    if not os.path.exists(filename): return None
    with open(filename, 'r') as f:
        lines = f.readlines()
    if not lines: return None
    item = lines[0].strip()
    with open(filename, 'w welcome(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add') as f:
        f.writelines(lines[1:])
    return item

def buy_num(prod):
    url = f'https://5sim.net/v1/user/buy/activation/("🛍 Shop Services", "💳 Deposit")
    kb.add("👤 Profile", "📞 Support")
    bot.send_message(m.chat.id, "🐺 *Sovereign V15 Store* 🐺usa/any/{prod}'
    headers = {'Authorization': f'Bearer {SIM_TOKEN}', 'Accept': 'application/json'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return r.json()
    except: return None

def check_sms(oid\n\nAutomated USA Numbers & Aged Accounts.", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "🛍 Shop Services")
def shop(m):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add):
    url = f'https://5sim.net/v1/user/check/{oid}'
    headers = {'Authorization': f'Bearer {SIM_TOKEN}', 'Accept': 'application/json'}
    (types.InlineKeyboardButton("📲 WhatsApp USA - $10", callback_data="buy_wa"),
           try:
        r = requests.get(url, headers=headers, timeout=10)
        return r.json().get('sms')
    except: return None

@bot.message_handler(commands=['types.InlineKeyboardButton("👤 Facebook Aged - $15", callback_data="buy_fb"))
    botstart'])
def welcome(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
.send_message(m.chat.id, "🛒 *Select Product:*", parse_mode="Markdown",    kb.add("🛍 Shop Services", "💳 Deposit")
    kb.add("👤 Profile", "📞 Support")
    bot.send_message(m.chat.id, "🐺 *Sovereign V15 Store* 🐺\n\nAutomated USA Numbers & Aged Accounts.", parse_mode="Markdown", reply_ reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "💳 Deposit")
def deposit(m):
    bot.send_message(m.chat.id, f"💳 *PAYMENT*\n\n🏦 OPAY: `7066549677`\n\n📸 Send receipt screenshot here!")

@bot.message_handler(content_types=['photomarkup=kb)

@bot.message_handler(func=lambda m: m.text == "🛍 Shop Services")
def shop(m):
    kb = types.InlineKeyboardMarkup(row_width=1)
'])
def receipt(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Appr WhatsApp", callback_data=f"ap_wa_{m.chat.id}"),
           types.InlineKeyboardButton("✅ Appr Facebook", callback_data=f"ap_fb_{m.    kb.add(types.InlineKeyboardButton("📲 WhatsApp USA - $10", callback_data="buy_wa"),
           types.InlineKeyboardButton("👤 Facebook Aged - $15", callback_data="buy_fbchat.id}"))
    bot.forward_message(ADMIN_ID, m.chat.id, m"))
    bot.send_message(m.chat.id, "🛒 *Select Product:*", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(func=lambda m: m.message_id)
    bot.send_message(ADMIN_ID, "New Receipt! Release product?", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
.text == "💳 Deposit")
def deposit(m):
    bot.send_message(m.chat.id, f"💳 *PAYMENT*\n\n🏦 OPAY: `706654def handle_query(call):
    data = call.data.split('_')
    if data[0] == "ap":
        prod, uid = data[1], data[2]
        if prod == "wa":
            res = buy_num("whatsapp")
            if res and 'phone' in res:9677`\n\n📸 Send receipt screenshot here!")

@bot.message_handler(content_types=['photo'])
def receipt(m):
    kb = types.InlineKeyboardMarkup()
    kb.
                bot.send_message(uid, f"✅ *Appr!* Number: `{res['phone']}`\nWaiting for SMS...")
                for _ in range(15):
                    time.sleep(add(types.InlineKeyboardButton("✅ Appr WhatsApp", callback_data=f"ap_wa_{m.chat.id}"),
           types.InlineKeyboardButton("✅ Appr Facebook", callback_data=f"ap_10)
                    sms = check_sms(res['id'])
                    if sms:
                        bot.send_message(uid, f"📩 *CODE:* `{sms[0]['code']}`")
                        returnfb_{m.chat.id}"))
    bot.forward_message(ADMIN_ID, m.chat
                bot.send_message(uid, "❌ SMS Timeout. Contact Admin.")
        elif prod == "fb":.id, m.message_id)
    bot.send_message(ADMIN_ID, "New Receipt! Release product?", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    data = call.data.split('_')
    
            acc = get_stock("fb_stock.txt")
            if acc: bot.send_message(uid, f"✅ *Appr!* Login:\n`{acc}`")
            else: botif data[0] == "ap":
        prod, uid = data[1], data[2]
.send_message(uid, "❌ Stock Empty! Admin will send manually.")

def run_bot():
        if prod == "wa":
            res = buy_num("whatsapp")
            if res and 'phone    while True:
        try:
            bot.polling(none_stop=True, interval=2, timeout=20)
        except:
            time.sleep(5)

if __name__ == "__main' in res:
                bot.send_message(uid, f"✅ *Appr!* Number:__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int `{res['phone']}`\nWaiting for SMS...")
                for _ in range(15):
                    time.sleep(10)
                    sms = check_sms(res['id'])
                    if sms:(os.environ.get("PORT", 10000))
    app.run(host='
                        bot.send_message(uid, f"📩 *CODE:* `{sms[0]['code']}0.0.0.0', port=port)
