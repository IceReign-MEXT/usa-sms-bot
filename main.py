import os, telebot, requests, time, threading, random
from telebot import types
from flask import Flask

TOKEN = os.environ.get('BOT_TOKEN')
SIM_TOKEN = os.environ.get('SIM_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '7033049440'))
ADMIN_USER = os.environ.get('ADMIN_USERNAME', '@Lona_trit')
CHANNEL_ID = os.environ.get('CHANNEL_ID', '-1002622160373')

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def home(): return "Sovereign Mega-Store Live", 200

# --- AUTO-POSTER (THE NEWSPAPER) ---
def channel_broadcaster():
    news_updates = [
        "📰 *SOVEREIGN DAILY:* \n🔥 USA Aged Facebook Accounts (2021) back in stock! \n💰 Price: $15 \n👉 Order: @Sovereign_Guard_Bot",
        "⚡️ *FLASH SALE:* \nPremium VPN (30 Days) - High Speed. \n🛡 Protect your privacy for only $5! \n👉 Buy: @Sovereign_Guard_Bot",
        "📲 *WHATSAPP PLUG:* \nGet your USA number for WhatsApp instantly. \n✅ 100% Automated. \n👉 Type /start to begin.",
        "📊 *MARKET UPDATE:* \nTrust is our priority. 🤝 \nOver 100+ accounts delivered this week! \nContact @Lona_trit for bulk deals.",
        "🛠 *TOOL BOX:* \nUpdated VPN configs and Google Voice fixes just added! \nCheck /shop now."
    ]
    
    while True:
        try:
            msg = random.choice(news_updates)
            bot.send_message(CHANNEL_ID, msg, parse_mode="Markdown")
            # POST EVERY 30 MINUTES (1800 seconds)
            time.sleep(1800) 
        except:
            time.sleep(60)

# --- UTILITIES ---
def get_stock(filename):
    if not os.path.exists(filename): return None
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        if not lines: return None
        item = lines[0].strip()
        with open(filename, 'w') as f:
            f.writelines(lines[1:])
        return item
    except: return None

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
def start(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛍 Shop Services", "💳 Deposit")
    kb.add("👤 My Profile", "📞 Support")
    bot.send_message(m.chat.id, "🐺 *Sovereign Mega-Store* 🐺\n\nAutomated USA Numbers & Aged Accounts.", parse_mode="Markdown", reply_markup=kb)

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
    kb.add(types.InlineKeyboardButton("✅ Appr WA", callback_data=f"ap_wa_{m.chat.id}"),
           types.InlineKeyboardButton("✅ Appr FB", callback_data=f"ap_fb_{m.chat.id}"),
           types.InlineKeyboardButton("✅ Appr VPN", callback_data=f"ap_vpn_{m.chat.id}"))
    bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    bot.send_message(ADMIN_ID, f"New Receipt from {m.chat.id}! Release product?", reply_markup=kb)
    bot.send_message(m.chat.id, "⌛ *Payment received!* Admin is verifying...")

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    data = call.data.split('_')
    if data[0] == "ap":
        prod, uid = data[1], data[2]
        bot.answer_callback_query(call.id, "Releasing...")
        if prod == "wa":
            res = buy_num("whatsapp")
            if res and 'phone' in res:
                bot.send_message(uid, f"✅ *Approved!* Number: `{res['phone']}`\nWaiting for SMS...")
                for _ in range(15):
                    time.sleep(10)
                    sms = check_sms(res['id'])
                    if sms:
                        bot.send_message(uid, f"📩 *CODE:* `{sms[0]['code']}`")
                        return
                bot.send_message(uid, "❌ SMS Timeout.")
        elif prod == "fb":
            acc = get_stock("fb_stock.txt")
            if acc: bot.send_message(uid, f"✅ *Approved!* FB:\n`{acc}`")
            else: bot.send_message(uid, "❌ FB Stock Empty!")
        elif prod == "vpn":
            vpn = get_stock("vpn_stock.txt")
            if vpn: bot.send_message(uid, f"✅ *Approved!* VPN Config:\n\n`{vpn}`")
            else: bot.send_message(uid, "❌ VPN Stock Empty!")

if __name__ == "__main__":
    threading.Thread(target=channel_broadcaster, daemon=True).start()
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
