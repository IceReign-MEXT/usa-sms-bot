import os, telebot, requests, time, threading
from telebot import types
from flask import Flask

# --- CONFIG ---
TOKEN = os.environ.get('BOT_TOKEN')
SIM_TOKEN = os.environ.get('SIM_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '7033049440'))
ADMIN_USER = os.environ.get('ADMIN_USERNAME', '@Lona_trit')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def home(): return "Sovereign Mega-Store Live", 200

# --- UTILITIES ---
def get_stock(filename):
    if not os.path.exists(filename): return None
    with open(filename, 'r') as f:
        lines = f.readlines()
    if not lines: return None
    item = lines[0].strip()
    with open(filename, 'w') as f:
        f.writelines(lines[1:])
    return item

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

# --- BOT COMMANDS ---
@bot.message_handler(commands=['start'])
def start(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛍 Shop Services", "💳 Deposit")
    kb.add("👤 My Profile", "📞 Support")
    bot.send_message(m.chat.id, "🐺 *Sovereign Mega-Store* 🐺\n\nAutomated WhatsApp, Facebook & Premium VPN.", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(func=lambda m: True)
def text_handler(m):
    if "Shop" in m.text:
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(types.InlineKeyboardButton("📲 WhatsApp USA - $10", callback_data="buy_wa"),
               types.InlineKeyboardButton("👤 Facebook Aged - $15", callback_data="buy_fb"),
               types.InlineKeyboardButton("🌐 VPN Premium (30D) - $5", callback_data="buy_vpn"))
        bot.send_message(m.chat.id, "🛒 *Select Service:*", parse_mode="Markdown", reply_markup=kb)
    elif "Deposit" in m.text:
        bot.send_message(m.chat.id, f"💳 *PAYMENT*\n\n🏦 OPAY: `7066549677`\n\n📸 Send receipt screenshot here!")
    elif "Support" in m.text:
        bot.send_message(m.chat.id, f"📞 *Support:* Contact {ADMIN_USER}")

@bot.message_handler(content_types=['photo'])
def receipt_handler(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Appr WhatsApp", callback_data=f"ap_wa_{m.chat.id}"),
           types.InlineKeyboardButton("✅ Appr Facebook", callback_data=f"ap_fb_{m.chat.id}"),
           types.InlineKeyboardButton("✅ Appr VPN", callback_data=f"ap_vpn_{m.chat.id}"))
    bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    bot.send_message(ADMIN_ID, "New Receipt! Release which product?", reply_markup=kb)
    bot.send_message(m.chat.id, "⌛ *Payment received!* Admin is verifying...")

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    data = call.data.split('_')
    if data[0] == "ap":
        prod, uid = data[1], data[2]
        bot.answer_callback_query(call.id, "Releasing product...")
        
        if prod == "wa":
            res = buy_num("whatsapp")
            if res and 'phone' in res:
                bot.send_message(uid, f"✅ *Approved!* Number: `{res['phone']}`\nWaiting for SMS...")
                for _ in range(15):
                    time.sleep(10)
                    sms = check_sms(res['id'])
                    if sms:
                        bot.send_message(uid, f"📩 *CODE:* `{sms[0]['code']}`")
                        if CHANNEL_ID: bot.send_message(CHANNEL_ID, "🔥 *SALE:* USA WhatsApp Delivered!")
                        return
                bot.send_message(uid, "❌ SMS Timeout. Contact Admin.")
            else: bot.send_message(ADMIN_ID, "❌ 5SIM Balance Error!")
            
        elif prod == "fb":
            acc = get_stock("fb_stock.txt")
            if acc: bot.send_message(uid, f"✅ *Approved!* FB Login:\n`{acc}`")
            else: bot.send_message(uid, "❌ FB Stock Empty!")

        elif prod == "vpn":
            vpn = get_stock("vpn_stock.txt")
            if vpn: bot.send_message(uid, f"✅ *Approved!* WireGuard Config:\n\n`{vpn}`")
            else: bot.send_message(uid, "❌ VPN Stock Empty!")

# --- RUN ---
def run_bot():
    while True:
        try: bot.polling(none_stop=True, interval=2, timeout=20)
        except: time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
