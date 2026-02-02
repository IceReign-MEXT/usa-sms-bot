import os, telebot, requests, time, threading
from telebot import types
from flask import Flask

# --- CONFIGURATION ---
TOKEN = os.environ.get('BOT_TOKEN')
SIM_TOKEN = os.environ.get('SIM_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '7033049440'))
ADMIN_USER = os.environ.get('ADMIN_USERNAME', '@Lona_trit')

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Sovereign Shop is Live", 200

def get_stock(filename):
    if not os.path.exists(filename): return None
    with open(filename, 'r') as f:
        lines = f.readlines()
    if not lines: return None
    item = lines[0].strip()
    with open(filename, 'w') as f:
        f.writelines(lines[1:])
    return item

@bot.message_handler(commands=['start'])
def welcome(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛍 Shop Services", "💳 Deposit")
    kb.add("👤 Profile", "📞 Support")
    bot.send_message(m.chat.id, "🐺 *Sovereign V15 Store* 🐺\n\nAutomated USA Numbers & Aged Accounts.", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(func=lambda m: True)
def handle_all_messages(m):
    if "Shop" in m.text:
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(types.InlineKeyboardButton("📲 WhatsApp USA - $10", callback_data="buy_wa"),
               types.InlineKeyboardButton("👤 Facebook Aged - $15", callback_data="buy_fb"))
        bot.send_message(m.chat.id, "🛒 *Select Product:*", parse_mode="Markdown", reply_markup=kb)
    
    elif "Deposit" in m.text:
        bot.send_message(m.chat.id, f"💳 *PAYMENT*\n\n🏦 OPAY: `7066549677`\n\n📸 Send receipt screenshot here!")
    
    elif "Support" in m.text:
        bot.send_message(m.chat.id, f"📞 *Support:* Contact {ADMIN_USER}")

@bot.message_handler(content_types=['photo'])
def receipt(m):
    bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    bot.send_message(ADMIN_ID, f"New Receipt from {m.chat.id}. Use /approve {m.chat.id} to release.")
    bot.send_message(m.chat.id, "⌛ *Payment sent for verification!*")

def run_bot():
    while True:
        try:
            bot.polling(none_stop=True, interval=2, timeout=20)
        except:
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
