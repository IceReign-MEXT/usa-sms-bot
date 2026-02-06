import os
import requests
from flask import Flask, request
import telebot
from telebot import types

app = Flask(__name__)

# Config from Render Environment Variables
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SMM_API_KEY = os.environ.get("SMM_API_KEY")
ADMIN_ID = "YOUR_TELEGRAM_ID"  # Replace with your actual Telegram ID
CHANNEL_ID = "@your_channel_username" # Your channel username
PAYMENT_ADDRESS = "Your_Wallet_Address_Here"

bot = telebot.TeleBot(TOKEN, threaded=False)

# --- KEYBOARDS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🚀 SMM Services", "👤 Buy Accounts", "💰 My Balance", "📞 Support")
    return markup

def account_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Facebook Accounts", callback_data="buy_fb"))
    markup.add(types.InlineKeyboardButton("WhatsApp Accounts", callback_data="buy_wa"))
    markup.add(types.InlineKeyboardButton("Telegram Accounts", callback_data="buy_tg"))
    return markup

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Welcome to *IceGods Sovereign Store*", 
                     parse_mode='Markdown', reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "🚀 SMM Services")
def smm_section(m):
    bot.reply_to(m, "Use `/boost [ID] [Link] [Qty]` to order SMM services.")

@bot.message_handler(func=lambda m: m.text == "👤 Buy Accounts")
def account_section(m):
    bot.send_message(m.chat.id, "Select account type:", reply_markup=account_menu())

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def handle_purchase(call):
    product = call.data.replace("buy_", "").upper()
    msg = f"💳 *Payment for {product} Account*\n\n"
    msg += f"Please send payment to:\n`{PAYMENT_ADDRESS}`\n\n"
    msg += "After sending, message @YourUsername with a screenshot."
    bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, parse_mode='Markdown')

# Admin command to post to channel
@bot.message_handler(commands=['post'])
def post_to_channel(m):
    if str(m.from_user.id) == ADMIN_ID:
        content = m.text.replace("/post ", "")
        bot.send_message(CHANNEL_ID, f"📢 *NEW UPDATE:*\n\n{content}", parse_mode='Markdown')
        bot.reply_to(m, "Posted to channel!")

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return 'ok', 200

@app.route('/')
def index():
    return "Store Online", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
