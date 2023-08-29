import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import yfinance as yf
from alice_blue import *
import  Config
import requests
import time as TT
import pandas as pd
from datetime import datetime, time
import traceback

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
    # while datetime.now().time() < time(23,30):
    #     try:
    #         subscribeSymbol()
    #     except Exception as e:
    #         traceback.print_exc()
    #         print(f'Error in Recheck list {e}')
    #     TT.sleep(5)
    
    # print('EOD')
    # telegram_bot_sendtext('alert ended')

# def event_handler_quote_update(message):
    
#     ltp = message['ltp']
#     timestamp = datetime.fromtimestamp(message['exchange_time_stamp']).isoformat()
#     expiry = message['instrument'].expiry
#     symbol =  message['instrument'].symbol
#     if datetime.now().second < 2:
#         print(timestamp, ltp , symbol  )
    
    
#     alertInfo = Config.ALERT_DF.loc[symbol]
    
#     alertTrigger = False
    
#     if alertInfo.CONDITION == 'GE' and  ltp >= alertInfo.VALUE:
#         alertTrigger =True
    
#     elif alertInfo.CONDITION == 'LE' and  ltp <= alertInfo.VALUE:
#         alertTrigger =True
        
#     elif alertInfo.CONDITION == 'G' and  ltp > alertInfo.VALUE:
#         alertTrigger =True
        
#     elif alertInfo.CONDITION == 'L' and  ltp < alertInfo.VALUE:
#         alertTrigger =True
    
#     if alertTrigger and str(alertInfo.STATUS) == '1':
#         print(f'alert trigger for {symbol}')
#         Config.ALICE_OBJ.unsubscribe(message['instrument'], LiveFeedType.COMPACT)
#         sendMessageAndUpdateFile(f"{timestamp} {symbol}  LTP {ltp} {alertInfo.CONDITION} Limit {alertInfo.VALUE}",symbol)

if __name__ == '__main__':
    main()
