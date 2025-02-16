import os
import telebot
import BusMain
import Stop

# initializing data
bus_main  = BusMain.BusMain()

# initializing bot
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi, this is the bus bot. I can show you a list of buses that will go through a stop.")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Use the command /stop to enter a stop code and see the line that will pass in the stop in the next 60 minutes.")

@bot.message_handler(commands=['stop'])
def send_welcome(message):
    text="enter a stop code"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, stop_handler)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Sorry, I don't know how to respond to " + message.text)

def stop_handler(message):
    stop_code: str= message.text
    display_text = bus_main.get_stop_lines_text(stop_code)
    bot.send_message(message.chat.id, display_text, parse_mode="Markdown")

bot.infinity_polling()
