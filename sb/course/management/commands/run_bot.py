from django.core.management.base import BaseCommand, CommandError
from course.models import Course
from pl.settings import TBOT_KEY

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Bot

import time
from random import randrange

HELLO_MESSAGES = [
    'Привет! Меня зовут Дмитрий Жариков и я автор сайта <a href="https://webmonstr.com">webmonstr.com</a>',
    'Я долгое время программировал на таких языках как PHP, Python, Javascript.',
    'И у меня достаточно опыта чтобы научить тебя как создавать самы разные веб-сайты.'
    'Я преподаю как онлайн так и оффлайн и все курсы у меня записаны и готовы к просмотру.',
    'В данный момент активны следующие курсы:'
]

bot = Bot(token=TBOT_KEY)

def start(update: Updater, context: CallbackContext):
    print("Start command!")
    username = update.message.from_user['username']
    room_id = update.message.chat_id 
    for message in HELLO_MESSAGES:
        bot.send_message(chat_id=room_id, text=message,parse_mode='HTML') 
        time.sleep(randrange(3,8))
    for course in Course.objects.all():
        mes = '<a href="https://webmonstr.com%s">%s</a>' % (course.get_absolute_url(),course.name)
        bot.send_message(chat_id=room_id, text=mes,parse_mode='HTML') 
        time.sleep(3)  
    time.sleep(4)  
    bot.send_message(chat_id=room_id, text='Буду рад помочь!',parse_mode='HTML')

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print('Running bot')
        start_handler = CommandHandler('start', start)
        updater = Updater(token=TBOT_KEY, use_context=True)
        updater.dispatcher.add_handler(start_handler)
        updater.start_polling() 