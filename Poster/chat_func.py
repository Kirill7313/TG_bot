import telebot
from datetime import *

def check_step(call,step,bot,user):
    if call=='back':
        return step-2, 'back'
    elif call=='start':
        return 0, ''
    else:
        return step, ''



def For_week(user,bot, msg_id=None):
    d_now = date.today()
    d_end1=str(d_now + timedelta(days=6))
    d_next =str(d_now + timedelta(days=7))
    d_end2=str(d_now + timedelta(days=13))
    d_now=str(d_now)
    
    kb=telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton(text=f'Эта ({d_now[-2:]}-{d_end1[-2:]})', callback_data='current'))
    kb.add(telebot.types.InlineKeyboardButton(text=f'Следующая ({d_next[-2:]}-{d_end2[-2:]})', callback_data='next'))
    kb.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))
    if msg_id:
        msg = bot.edit_message_text(chat_id=user, message_id=msg_id, text='Какая неделя вас интересует?', reply_markup=kb)
    else:
        msg = bot.send_message(user, 'Какая неделя вас интересует?', reply_markup=kb)
    return msg.message_id
def For_day(user,bot, days, msg_id=None):
    d_now = date.today() + timedelta(days=days)
    kb=telebot.types.InlineKeyboardMarkup()
    for i in range(7):
        d=str(d_now + timedelta(days=i))
        kb.add(telebot.types.InlineKeyboardButton(text=d,callback_data=d))
    kb.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))
    if msg_id:
        msg = bot.edit_message_text(chat_id=user, message_id=msg_id, text='Какой день?', reply_markup=kb)
    else:
        msg = bot.send_message(user, 'Какой день?', reply_markup=kb)
    return msg.message_id
def For_event(user,bot,headers, msg_id=None):
    kb=telebot.types.InlineKeyboardMarkup()
    if not headers:
        kb.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))
        if msg_id:
            msg = bot.edit_message_text(chat_id=user, message_id=msg_id, text=f'На этот день ничего нет', reply_markup=kb)
        else:
            msg = bot.send_message(user, f'На этот день ничего нет', reply_markup=kb)
    else:
        for i in headers:
            kb.add(telebot.types.InlineKeyboardButton(text=i[1], callback_data=i[0]))
        kb.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))
        if msg_id:
            msg = bot.edit_message_text(chat_id=user, message_id=msg_id, text='Список мероприятий:', reply_markup=kb)
        else:
            msg = bot.send_message(user, 'Список мероприятий:', reply_markup=kb)
    return msg.message_id
def Show_event(user,bot,info, msg_id=None):
    kb=telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))
    if msg_id:
        msg = bot.edit_message_text(chat_id=user, message_id=msg_id, text=f'{info[0]} \n\nДата: {info[1]}   Время: {info[2]} \n\n{info[3]}', reply_markup=kb)
    else:
        msg = bot.send_message(user, f'{info[0]} \n\nДата: {info[1]}   Время: {info[2]} \n\n{info[3]}', reply_markup=kb)
    return msg.message_id