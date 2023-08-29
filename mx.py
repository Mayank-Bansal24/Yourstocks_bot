import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
import pandas as pd


# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TELEGRAM_TOKEN = '6504790425:AAGy1Uhjp5fzrEtJzrxaU-sLqu58blV_JNI'
INPUT_NAME_1, INPUT_COND_2,INPUT_PRICE_3,FINAL_RESULT = range(4)

def csvupdater(result):
    df = pd.read_csv('alert_list.csv')
    x=df.shape[0]
    new_data =[ {'SYMBOL': result['stock_name'], 'Unnamed':x , 'EXCHANGE': 'BSE', 'CONDITION' : result['stock_cond'], 'VALUE' : result['stock_price'] , 'STATUS' : 1}]
    df = pd.DataFrame(new_data)
    df.to_csv('alert_list.csv', mode='a', header=False, index=False)
    print("Stock Added for tracking")
def start(update, context):
    update.message.reply_text("Hello! I'm your bot. Type /track to start the process.")
    return INPUT_NAME_1

def input_name_1(update, context):
    update.message.reply_text("Please provide your Stock name first:")
    return INPUT_COND_2

def input_cond_2(update, context):
    user_input_1 = context.user_data['stock_name'] = update.message.text
    update.message.reply_text("Please provide your stock price condition (LE,L,GE,G):")
    return INPUT_PRICE_3

def input_price_3(update, context):
    user_input_2 = context.user_data['stock_cond'] = update.message.text
    update.message.reply_text("Please provide your stock price thresh:")
    return FINAL_RESULT

def final_result(update, context):
    user_input_3 = context.user_data['stock_price'] = update.message.text
    result = f"Stock_name: {context.user_data['stock_name']}\nStock_cond: {context.user_data['stock_cond']}\nStock_price: {context.user_data['stock_price']}"
    csvupdater(context.user_data)
    update.message.reply_text(f"Received inputs:\n{result}")
    return ConversationHandler.END

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('track', input_name_1)],
        states={
            INPUT_COND_2: [MessageHandler(Filters.text & ~Filters.command, input_cond_2)],
            INPUT_PRICE_3: [MessageHandler(Filters.text & ~Filters.command, input_price_3)],
            FINAL_RESULT: [MessageHandler(Filters.text & ~Filters.command, final_result)]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
