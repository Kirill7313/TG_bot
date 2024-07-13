import telebot
from func import *
from chat_func import *
token = ''

step=0
source=None
week=None
day=None
event=None
data={'source':None,'week':None,'day':None,'event':None}
for_data={0:'source',1:'week',2:'day',3:'event'}
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(message):
    global step
    step=0
    kb=telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton(text='Начать', callback_data='start'))
    bot.send_message(message.chat.id, 'Добро пожаловать а афишу Тольятти', reply_markup=kb)
@bot.callback_query_handler(func=lambda call: True)
def user_source(call):
    global step, msg_id,data,for_data
    user=call.message.chat.id
    check=check_step(call.data,step,bot,user,call.message.message_id)#chat_func.py
    if check[1]=='back':
        data[for_data[check[0]]]=None
    step=check[0]
    
    if step==0:
        kb=telebot.types.InlineKeyboardMarkup()
        kb.add(telebot.types.InlineKeyboardButton(text='Сторонние источники', callback_data='parser'))
        kb.add(telebot.types.InlineKeyboardButton(text='Редакционные', callback_data='redact'))
        bot.send_message(user, 'Откуда хотите узнать информацию о событиях?', reply_markup=kb)
        step=1    
    elif step==1:
        if data['source']==None:
            data['source']=call.data
        msg_id = For_week(user,bot)#func.py
        step=2 
    elif step==2:
        if data['week']==None:
            data['week']=call.data
        if data['week']=='current':
            For_day(user,bot, 0)#chat_func.py
        else:
            For_day(user,bot, 7)#chat_func.py
        step=3
    elif step==3:
        if data['day']==None:
            data['day']=call.data
        headers=get_headers(data['day'])#func.py
        For_event(user,bot,headers)#chat_func.py
        step=4
    elif step==4:
        data['event']=call.data
        info=get_info(data['event'])#func.py
        Show_event(user,bot,info)#chat_func.py
        step=5
    print(f'{data}, User:{user}')
bot.polling(none_stop=True)