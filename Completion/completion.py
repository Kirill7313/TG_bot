import telebot
import time
from func import *

auth()
token = ''
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, "Привет, это бот для заполнения списка мероприятий в нашей бот-афише! Для начала заполнения напишите /new");
    print ("/start от " + message.from_user.first_name + ' '  + message.from_user.last_name + '(https://t.me/' + message.from_user.username + ')')
@bot.message_handler(commands=['new'])
def new_header(message):
    bot.send_message(message.chat.id, "Напишите заголовок, который даст примерное описание вашего мероприятия: ")
    bot.register_next_step_handler(message, new_date)
def new_date(message):
    global header
    header = message.text
    bot.send_message(message.chat.id, "Отлично! Теперь отправьте дату проведения мероприятия в формате YYYY-MM-DD: ")
    bot.register_next_step_handler(message, new_time)
def new_time(message):
    global date
    date = message.text
    bot.send_message(message.chat.id, "Замечательно! Отправьте время проведения мероприятия: ")
    bot.register_next_step_handler(message, new_desc)
def new_desc(message):
    global time
    time = message.text
    bot.send_message(message.chat.id, "Финальный шаг! Напишите описание вашего мероприятия или ссылку на него: ")
    bot.register_next_step_handler(message, final)
def final(message):
    global desc
    global clm
    desc = message.text
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_save = telebot.types.InlineKeyboardButton(text="Все верно", callback_data='save_data')
    button_change = telebot.types.InlineKeyboardButton(text="Изменить", callback_data='change_data')
    keyboard.add(button_save, button_change)
    clm = message.from_user
    bot.send_message(message.chat.id, f"Прекрасно! Убедитесь, что данные введены верно\nЗаголовок: {header}\nДата: {date}\nВремя: {time}\nОписание: {desc}", reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def buttons(call):
    user = call.message.chat.id
    if (call.data == 'save_data'):
        insert(header, date, time, desc)
        print (f"Заголовок: {header}\nДата: {date}\nВремя: {time}\nОписание: {desc}\nОтправитель: " + clm.first_name + ' '  + clm.last_name + '(https://t.me/' + clm.username + ')')
        bot.send_message(user, "Ваше мероприятие зарегистрировано!")
    if (call.data == 'change_data'):
        new_header(call.message)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(1)
            print("ERROR")
