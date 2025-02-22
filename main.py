import os
import telebot
import Classes.BusesData as BusesData
import Utils.BusUtils as BusUtils

# initializing data
bus_data  = BusesData.BusData()

# initializing bot
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# handeling 'start', 'hello' commands
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi, this is the bus bot. I can show you a list of buses that will go through a stop or list stops close to your location.")

# handeling 'help' command
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Use the command /stop to enter a stop code and see the line that will pass in the stop in the next 60 minutes.")
    bot.reply_to(message, "Use the command /location to enter your location and see close transit stopes.")

# handeling 'stop' command - the user willl enter a station code
@bot.message_handler(commands=['stop'])
def send_welcome(message):
    text="enter a stop code"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, stop_handler)

def stop_handler(message):
    stop_code: str= message.text
    display_text = BusUtils.get_stop_lines_text(bus_data,stop_code)
    bot.send_message(message.chat.id, display_text, parse_mode="Markdown")

# handeling 'location' command - the user will send it's location
@bot.message_handler(commands=['location'])
def send_welcome(message):
    text="please send your location"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, location_handler)

def location_handler(message):
    location= message.location
    display_text = BusUtils.get_adjacent_stops_text(bus_data,location)
    bot.send_message(message.chat.id, display_text, parse_mode="Markdown")

# handeling unknown commands
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Sorry, I don't know how to respond to " + message.text)

bot.infinity_polling()
