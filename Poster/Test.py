import telebot
import time
from func import *
from chat_func import *

token = ''

step=0
source=None
week=None
day=None
event=None
msg_id=None
data={'source':None,'week':None,'day':None,'event':None}
for_data={0:'source',1:'week',2:'day',3:'event'}

bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(message):
    global step,msg_id
    step=0
    kb=telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton(text='Начать', callback_data='start'))
    msg = bot.send_message(message.chat.id, 'Добро пожаловать а афишу Тольятти', reply_markup=kb)
    msg_id = msg.message_id
@bot.callback_query_handler(func=lambda call: True)
def user_source(call):
    global step, msg_id,data,for_data,msg_id
    user=call.message.chat.id
    check=check_step(call.data,step,bot,user)#chat_func.py
    if check[1]=='back':
        data[for_data[check[0]]]=None
    step=check[0]
    
    if step==0:
        kb=telebot.types.InlineKeyboardMarkup()
        kb.add(telebot.types.InlineKeyboardButton(text='Сторонние источники', callback_data='parser'))
        kb.add(telebot.types.InlineKeyboardButton(text='Редакционные', callback_data='redact'))
        if msg_id:
            msg = bot.edit_message_text(chat_id=user, message_id=msg_id, text='Откуда хотите узнать информацию о событиях?', reply_markup=kb)
        else:
            msg = bot.send_message(user, 'Откуда хотите узнать информацию о событиях?', reply_markup=kb)
        msg_id = msg.message_id
        step=1    
    elif step==1:
        if data['source']==None:
            data['source']=call.data
        msg_id = For_week(user,bot,msg_id)#chat_func.py
        step=2 
    elif step==2:
        if data['week']==None:
            data['week']=call.data
        if data['week']=='current':
            msg_id = For_day(user,bot, 0,msg_id)#chat_func.py
        else:
            msg_id = For_day(user,bot, 7,msg_id)#chat_func.py
        step=3
    elif step==3:
        if data['day']==None:
            data['day']=call.data
        headers=get_headers(data['day'])#func.py
        msg_id = For_event(user,bot,headers,msg_id)#chat_func.py
        step=4
    elif step==4:
        data['event']=call.data
        info=get_info(data['event'])#func.py
        msg_id = Show_event(user,bot,info,msg_id)#chat_func.py
        step=5
    print(f'{data}, User:{user}')
    
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)    
