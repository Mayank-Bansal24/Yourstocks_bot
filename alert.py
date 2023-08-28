from alice_blue import *
import  Config
import requests
import time as TT
import pandas as pd
from datetime import datetime, time
import traceback


def login():
    access_token = AliceBlue.login_and_get_access_token(username=Config.USERNAME, password=Config.PASSWORD, twoFA=Config.YOB,api_secret=Config.SECRET_KEY,app_id=Config.APP_ID)
    #access_token = '8B9r1zbmMsbGfqde6gZZXzBLYy7pdolrY8sT_eQVexo.xh-UP-JD2WXu5UoHEDlkodrbOWwtkZ_yBTj3-gm3Bwk'
    Config.ALICE_OBJ= AliceBlue(username=Config.USERNAME, password=Config.PASSWORD, access_token=access_token, master_contracts_to_download=['NSE','NFO','CDS','MCX'])


def telegram_bot_sendtext(bot_message):
    try:
        bot_message = bot_message.replace('&','')
        send_text = 'https://api.telegram.org/bot' + Config.BOT_TOKEN + '/sendMessage?chat_id=' + Config.BOT_CHAT_ID + '&parse_mode=HTML&text=' + bot_message
        res = requests.get(send_text)
        #print(f'Telegram response : {res.json()}')
    except Exception as e:
        print(f'Error in sending Telegram msg {e}')

def sendMessageAndUpdateFile(msg,symbol,):
    print(msg)
    telegram_bot_sendtext(msg)
    for i in range(0,2):
        try:
            alertDf = getResetAlertList()
            alertDf.loc[symbol,'STATUS'] = 0
            alertDf.to_csv('alert_list.csv')
            print('CSV file updated')
            break
        except Exception as e:
            traceback.print_exc()
            print(f'Error in updating file {e}')
        TT.sleep(1)

def getResetAlertList():
    Config.ALERT_DF = pd.read_csv('alert_list.csv')
    Config.ALERT_DF.set_index('SYMBOL',inplace =True)
    return Config.ALERT_DF

def subscribeSymbol():
    alice = Config.ALICE_OBJ
    listedInstrument = alice.get_all_subscriptions()
    print(listedInstrument.keys())
    alertDf = getResetAlertList()
    for i in alertDf.index : 
        alertRow =alertDf.loc[i] 
        inst = alice.get_instrument_by_symbol(alertRow.EXCHANGE, i)
        if str(alertRow.STATUS) == '1' and inst not in listedInstrument:
            alice.subscribe(alice.get_instrument_by_symbol(alertRow.EXCHANGE, i), LiveFeedType.COMPACT)
        
        elif str(alertRow.STATUS) != '1' and inst  in listedInstrument:
            alice.unsubscribe(alice.get_instrument_by_symbol(alertRow.EXCHANGE, i), LiveFeedType.COMPACT)



socket_opened = False
def event_handler_quote_update(message):
    
    ltp = message['ltp']
    timestamp = datetime.fromtimestamp(message['exchange_time_stamp']).isoformat()
    expiry = message['instrument'].expiry
    symbol =  message['instrument'].symbol
    if datetime.now().second < 2:
        print(timestamp, ltp , symbol  )
    
    
    alertInfo = Config.ALERT_DF.loc[symbol]
    
    alertTrigger = False
    
    if alertInfo.CONDITION == 'GE' and  ltp >= alertInfo.VALUE:
        alertTrigger =True
    
    elif alertInfo.CONDITION == 'LE' and  ltp <= alertInfo.VALUE:
        alertTrigger =True
        
    elif alertInfo.CONDITION == 'G' and  ltp > alertInfo.VALUE:
        alertTrigger =True
        
    elif alertInfo.CONDITION == 'L' and  ltp < alertInfo.VALUE:
        alertTrigger =True
    
    if alertTrigger and str(alertInfo.STATUS) == '1':
        print(f'alert trigger for {symbol}')
        Config.ALICE_OBJ.unsubscribe(message['instrument'], LiveFeedType.COMPACT)
        sendMessageAndUpdateFile(f"{timestamp} {symbol}  LTP {ltp} {alertInfo.CONDITION} Limit {alertInfo.VALUE}",symbol)
    
    
def open_callback():
    global socket_opened
    socket_opened = True
    print('socket opened')



if __name__ == "__main__":
    telegram_bot_sendtext('alert started')
    login()
    
    Config.ALICE_OBJ.start_websocket(subscribe_callback=event_handler_quote_update,
                        socket_open_callback=open_callback,
                        run_in_background=True)
    while(socket_opened==False):
        pass
    
    while datetime.now().time() < time(23,30):
        try:
            subscribeSymbol()
        except Exception as e:
            traceback.print_exc()
            print(f'Error in Recheck list {e}')
        TT.sleep(5)
    
    print('EOD')
    telegram_bot_sendtext('alert ended')