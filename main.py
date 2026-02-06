import os
import requests
import telebot
from telebot import types
from flask import Flask, request
import pg8000.native

app = Flask(__name__)

# --- CONFIG ---
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SMM_API_KEY = os.environ.get("SMM_API_KEY")
SMM_API_URL = "https://morethanpanel.com/api/v2"
ADMIN_ID = 7033049440
CHANNEL_ID = -1002622160373

bot = telebot.TeleBot(TOKEN, threaded=False)

# DATABASE - In a real scenario, we'd save IDs to a file/DB. 
# Here we use the Gazette for broad marketing.

@bot.message_handler(commands=['start'])
def start(m):
    # Log user for marketing (logic placeholder)
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 Market", "🚀 SMM Boost", "💳 My Wallet", "📰 Newsroom")
    bot.send_message(m.chat.id, "👑 *SOVEREIGN EMPIRE V3.1*\nYour Elite Assets are ready for deployment.", 
                     parse_mode='Markdown', reply_markup=markup)

# --- MARKETING BROADCAST ENGINE ---
@bot.message_handler(commands=['mass'])
def mass_broadcast(m):
    """Allows Admin to send a direct message to the channel with 'HOT' stock alerts"""
    if m.from_user.id != ADMIN_ID: return

    text = m.text.replace("/mass ", "")
    if not text or text == "/mass":
        bot.reply_to(m, "❌ Usage: `/mass [Your Marketing Message]`")
        return

    marketing_msg = (
        "🚨 *URGENT ASSET ALERT*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"{text}\n\n"
        "⚡ *Action:* Use /start to buy now.\n"
        "📡 *Source:* @ZeroThreatIntel"
    )
    bot.send_message(CHANNEL_ID, marketing_msg, parse_mode='Markdown')
    bot.reply_to(m, "🚀 Marketing blast sent to Channel!")

@bot.message_handler(func=lambda m: m.text == "📰 Newsroom")
def professional_news(m):
    if m.from_user.id != ADMIN_ID: return
    # This is designed to look like a high-end Bloomberg/Reuters terminal
    gazette = (
        "🏙️ *SOVEREIGN DAILY GAZETTE - INTEL REPORT*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 *MARKET SENTIMENT:* BULLISH\n"
        "🔥 *HOT STOCK:* 2014 Aged FB Accounts (Limited 5 units)\n\n"
        "🚀 *SMM UPDATE:* TikTok Viral Engine now at 100% capacity.\n"
        "🛡️ *SECURITY:* All customer data encrypted via Python 3.11.\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📡 *LIVE FEED:* New business opportunities detected in West Africa/US.\n\n"
        "🔗 *OFFICIAL CHANNEL:* @ZeroThreatIntel"
    )
    bot.send_message(CHANNEL_ID, gazette, parse_mode='Markdown')
    bot.reply_to(m, "✅ Gazette Dispatched.")

@bot.message_handler(func=lambda m: m.text == "🚀 SMM Boost")
def smm_marketing_view(m):
    # Marketing-heavy view to encourage sales
    text = (
        "🚀 *ELITE SMM ACCELERATOR*\n"
        "Boost your social presence with zero drop risk.\n\n"
        "💎 *Premium Rates:* \n"
        "• IG Followers: $2.50\n"
        "• TG Members: $3.00\n"
        "• FB Likes: $1.80\n\n"
        "⚠️ *PROMO:* Deposit $50+ into wallet and get +10% bonus!"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 Buy Credits", callback_data="buy_credits"))
    markup.add(types.InlineKeyboardButton("📈 Place Order", callback_data="order_smm"))
    bot.send_message(m.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return 'ok', 200

@app.route('/')
def index(): return "Marketing Engine V3.1 Live", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
