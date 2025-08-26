import logging
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import openai
import os

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- API Keys ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # set in Render/Railway
OPENAI_KEY = os.getenv("OPENAI_API_KEY")      # set in Render/Railway
openai.api_key = OPENAI_KEY

# --- Commands ---
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🤖 About Bot", callback_data="about"),
         InlineKeyboardButton("💖 Support Me", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "✨ *Welcome to your AI Assistant!* ✨\n\n"
        "Ask me *anything* and I’ll try my best to answer.\n\n"
        "Use the buttons below 👇"
    )
    update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)

def help_command(update, context):
    help_text = (
        "📌 *Commands*\n\n"
        "/start - Restart bot\n"
        "/help - Show help menu\n\n"
        "💬 Just send me any message, and I’ll reply with AI power!"
    )
    update.message.reply_text(help_text, parse_mode="Markdown")

# --- Inline button handler ---
def button(update, context):
    query = update.callback_query
    query.answer()

    if query.data == "about":
        query.edit_message_text("🤖 I am a smart AI-powered bot built with Python + OpenAI!")
    elif query.data == "support":
        query.edit_message_text("💖 You can support my creator by sharing this bot with friends!")

# --- AI Chat ---
def ai_chat(update, context):
    user_message = update.message.text

    try:
        # Show typing effect
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        time.sleep(1.5)

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_message,
            max_tokens=150,
            temperature=0.7
        )

        reply = response["choices"][0]["text"].strip()
        styled_reply = f"🤖💡 *AI says:*\n\n{reply}"
        update.message.reply_text(styled_reply, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error: {e}")
        update.message.reply_text("⚠️ Oops! Something went wrong. Try again later 🙏")

# --- Main ---
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ai_chat))

    # Start
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
