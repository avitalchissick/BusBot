import os
import time

import telebot

from Classes import buses_data
from Utils import bus_utils

# initializing data
t0 = time.time()
bus_data = buses_data.bus_data()
t1 = time.time()
print(t1-t0)

# initializing bot
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


# handling 'start', 'hello' 'help' commands
@bot.message_handler(commands=['start', 'hello', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi, this is the bus bot. I can show you a list of buses that will go through a stop or list stops close to your location.")
    bot.reply_to(message, "Use the command /stop to enter a stop code and see the line that will pass in the stop in the next 60 minutes.")
    bot.reply_to(message, "Use the command /location to enter your location and see close transit stopes.")


# handling 'stop' command - the user willl enter a station code
@bot.message_handler(commands=['stop'])
def send_welcome(message):
    text="enter a stop code"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, stop_handler)


def stop_handler(message):
    stop_code: str= message.text
    display_text = bus_utils.get_stop_lines_text(bus_data,stop_code)
    bot.send_message(message.chat.id, display_text, parse_mode="Markdown")


# handling 'location' command - the user will send it's location
@bot.message_handler(commands=['location'])
def send_welcome(message):
    text="please send your location"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, location_handler)


def location_handler(message):
    location = message.location
    display_text = bus_utils.get_adjacent_stops_text(bus_data,location)
    bot.send_message(message.chat.id, display_text, parse_mode="Markdown")


# handling unknown commands
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Sorry, I don't know how to respond to " + message.text)


bot.infinity_polling()
