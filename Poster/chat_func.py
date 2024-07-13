import telebot
from datetime import *

def check_step(call,step,bot,user,message):
    if call=='back':
        bot.delete_message(user,message-1)
        bot.delete_message(user,message)
        return step-2, 'back'
    else:
        return step, ''



def For_week(user,bot):
    d_now = date.today()
    d_end1=str(d_now + timedelta(days=6))
    d_next =str(d_now + timedelta(days=7))
    d_end2=str(d_now + timedelta(days=13))
    d_now=str(d_now)
    
    kb=telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton(text=f'Эта ({d_now[-2:]}-{d_end1[-2:]})', callback_data='current'))
    kb.add(telebot.types.InlineKeyboardButton(text=f'Следующая ({d_next[-2:]}-{d_end2[-2:]})', callback_data='next'))
    kb.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))
    msg = bot.send_message(user, 'Какая неделя вас интересует?', reply_markup=kb)
def For_day(user,bot, days):
    d_now = date.today() + timedelta(days=days)
    kb=telebot.types.InlineKeyboardMarkup()
    for i in range(7):
        d=str(d_now + timedelta(days=i))
        kb.add(telebot.types.InlineKeyboardButton(text=d,callback_data=d))
    kb.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))
    bot.send_message(user, 'Какой день?', reply_markup=kb)
def For_event(user,bot,headers):
    kb=telebot.types.InlineKeyboardMarkup()
    if not headers:
        bot.send_message(user, f'На этот день ничего нет', reply_markup=kb)
        kb.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))
    else:
        for i in headers:
            kb.add(telebot.types.InlineKeyboardButton(text=i[1], callback_data=i[0]))
        kb.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))
        bot.send_message(user, 'Список мероприятий:', reply_markup=kb)
    
def Show_event(user,bot,info):
    kb=telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))
    bot.send_message(user, f'{info[0]} \n\nДата: {info[1]}   Время: {info[2]} \n\n{info[3]}', reply_markup=kb)