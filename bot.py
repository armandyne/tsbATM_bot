# -*- coding: utf-8 -*-
import settings
import DatabaseHelper
import telebot
from flask import Flask, request
import os

server = Flask(__name__)
bot = telebot.AsyncTeleBot(settings.BOT_TOKEN)

@bot.message_handler(commands=["start", "help"])
def start_handler(message):
    help_message = '''{}, Я помогу найти ближайший банкомат Цеснабанка.
Отправь мне свое местоположение 📎, или выбери точку на карте.'''

    print(message)
    bot.send_message(message.chat.id, help_message.format(message.from_user.first_name)).wait()

@bot.message_handler(content_types=["location"])
def send_nearest_atm(message):
    print(message)
    bot.send_chat_action(message.chat.id, "typing").wait()
    db = DatabaseHelper.DatabaseHelper(settings.DATABASE_NAME, settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_HOST, settings.DATABASE_PORT)
    result = db.select_atms(message.location.longitude, message.location.latitude)
    if len(result) == 0:
        result = db.select_atms(message.location.longitude, message.location.latitude, 6000)
    db.close()
     
    if len(result) == 0:
        bot.send_message(message.chat.id, "К сожалению, поблизости нет банкоматов.").wait()
    else:
        bot.send_location(message.chat.id, result[0][3], result[0][2]).wait()
        descr_text = '''Ближайший банкомат :
Адрес:{}
{}
Расстояние: {} м.'''.format(result[0][0], result[0][1], result[0][4])
        bot.send_message(message.chat.id, descr_text).wait()
        
@server.route('/' + settings.BOT_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "POST", 200

@server.route("/")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url=settings.HEROKU_APP_URL + settings.BOT_TOKEN)
    return "CONNECTED", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5002))  
