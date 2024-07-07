import telebot
from datetime import *
import sqlite3
from db_auth import *

token = ''
step=0

def For_week(user):
    d_now = date.today()
    d_end1=str(d_now + timedelta(days=6))
    d_next =str(d_now + timedelta(days=7))
    d_end2=str(d_now + timedelta(days=13))
    d_now=str(d_now)
    
    kb=telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton(text=f'Эта ({d_now[-2:]}-{d_end1[-2:]})', callback_data='current'))
    kb.add(telebot.types.InlineKeyboardButton(text=f'Следующая ({d_next[-2:]}-{d_end2[-2:]})', callback_data='next'))
    msg = bot.send_message(user, 'Какая неделя вас интересует?', reply_markup=kb)
    return msg.message_id
def For_day(user, days, msg_id=None):
    d_now = date.today() + timedelta(days=days)
    kb=telebot.types.InlineKeyboardMarkup()
    for i in range(7):
        d=str(d_now + timedelta(days=i))
        kb.add(telebot.types.InlineKeyboardButton(text=d,callback_data=d))
    if msg_id:
        bot.edit_message_text(chat_id=user, message_id=msg_id, text='Какой день?', reply_markup=kb)
    else:
        bot.send_message(user, 'Какой день?', reply_markup=kb)

auth('bot_db.db')
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(message):
    global step
    step=0
    kb=telebot.types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, 'Добро пожаловать а афишу Тольятти')
    kb.add(telebot.types.InlineKeyboardButton(text='Сторонние источники', callback_data='parser'))
    kb.add(telebot.types.InlineKeyboardButton(text='Редакционные', callback_data='redact'))
    bot.send_message(message.chat.id, 'Откуда хотите узнать информацию о событиях?', reply_markup=kb)
@bot.callback_query_handler(func=lambda call: True)
def user_source(call):
    global step
    user=call.message.chat.id
    if step==0:
        source=call.data
        global msg_id
        msg_id = For_week(user)
        print(f'Source: {source,user}')
    elif step==1:
        week=call.data
        if week=='current':
            For_day(user, 0, msg_id)
        else:
            For_day(user, 7, msg_id)
        print(f'Week: {week,user}')
    elif step==2:
        day=call.data
        print(f'Day: {day,user}')
        con = ret_con('bot_db.db')
        cur = ret_cur('bot_db.db')
        cur.execute('SELECT header FROM Events WHERE date = \'{day}\'')
        result = cur.fetchall()
        con.commit()
        con.close()
        for i in result:
            print(i)
    step+=1

bot.polling(none_stop=True)