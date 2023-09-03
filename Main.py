import telegram
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from dotenv import load_dotenv
import pandas as pd
import time as TT
import pandas as pd
from datetime import datetime, time
import csv
import yfinance as yf

load_dotenv()

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
UNINPUT_NAME_1,INPUT_NAME_1, UNINPUT_COND_2,INPUT_COND_2,INPUT_PRICE_3,FINAL_RESULT = range(6)

def csvupdater(result):
    df = pd.read_csv('alert_list.csv')
    x=df.shape[0]
    new_data =[ {'SYMBOL': result['stock_name'], 'Unnamed':x , 'EXCHANGE': 'BSE', 'CONDITION' : result['stock_cond'], 'VALUE' : result['stock_price'] , 'STATUS' : 0}]
    df = pd.DataFrame(new_data)
    df.to_csv('alert_list.csv', mode='a', header=False, index=False)
    print("Stock Added for tracking")

def csvupdater111(result):
    df = pd.read_csv('alert_list.csv')
    condition = df['SYMBOL'] == result
    df.loc[condition, 'STATUS'] = 1
    df.to_csv('alert_list.csv', index=False)

def notif(update,context):
    while datetime.now().time() < time(23,30):
        try:
            # subscribeSymbol()
            check(update,context)
            print(1)
        except Exception as e:
            # traceback.print_exc()
            print(f'Error in Recheck list {e}')
        TT.sleep(10)

def start(update, context):
    update.message.reply_text("Hello! I'm your bot. Type /track to start tracking a stock , /untrack to untrack a stock and /notify to start the notification process.")
    return INPUT_NAME_1

def uninput_name_1(update, context):
    update.message.reply_text("Please provide your Stock name first which you want to untrack:")
    return UNINPUT_COND_2

def uninput_cond_2(update, context):
    user_input_1 = context.user_data['stock_name'] = update.message.text
    csvupdater111(user_input_1)
    return ConversationHandler.END

def input_name_1(update, context):
    update.message.reply_text("Please provide your Stock name first:")
    return INPUT_COND_2

def input_cond_2(update, context):
    chat_id = update.message.chat_id
    # print(chat_id)
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

def check(update,context):
    chat_id = update.message.chat_id
    
    with open('alert_list.csv') as file_obj:
      
        reader_obj = csv.reader(file_obj)
        for row in reader_obj:
            # print(row)
            if row[0]=='SYMBOL' or row[5]=="1":
                # print("Not req")
                continue
            else:
                stk=row[0]
                ex=row[2]
                cond=row[3]
                flot= float(row[4])
                stok=stk+".BO"
                # print(stok)
                try:
                    stock_data = yf.Ticker(stok)
                    current_price = stock_data.history(period='1d')['Close'][-1]
                    current_price=float(current_price)
                    alert = False
                    if cond == 'GE' and  current_price >= flot:
                        alert =True
                    elif cond == 'LE' and  current_price <= flot:
                        alert =True
                    elif cond == 'G' and  current_price > flot:
                        alert =True
                    elif cond == 'L' and  current_price < flot:
                        alert =True
                    if alert==True:
                        message=f"You stock {stk} is now at your desired price  {current_price}   with condition of price {cond} than {flot} ."
                       
                        print(message)
                        context.bot.send_message(chat_id=chat_id, text=message)
                    
                except Exception as e:
                    print("Stock not listed")


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

    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('untrack', uninput_name_1)],
        states={
            UNINPUT_COND_2: [MessageHandler(Filters.text & ~Filters.command, uninput_cond_2)]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("notify", notif))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(conv_handler1)
    updater.start_polling()
    updater.idle()
    
    

if __name__ == '__main__':
    main()
