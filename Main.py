import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

load_dotenv()

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

def start(update, context):
    update.message.reply_text("Hello! I'm your bot. Type /help to see available commands.")

def echo(update, context):
    update.message.reply_text("You said: " + update.message.text)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
