import os
import telebot
import BusMain
import BusData
import Stop
import StopTimes

# initializing data
bus_main  = BusMain.BusMain()

# initializing bot
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi, this is the bus bot")

@bot.message_handler(commands=['stop'])
def send_welcome(message):
    text="enter a stop code"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, stop_handler)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Sorry, I don't know how to respond to " + message.text)

def stop_handler(message):
    stopCode: str= message.text
    if stopCode.isnumeric():
        stop: Stop = next((x for x in bus_main.stops if x.code == stopCode),None)
        if stop == None:
            displayText = f'stop {stopCode} not found'
        else:
            stop_lines = bus_main.get_stop_lines(stop.id)
            display_lines = ""
            for x in stop_lines:
                display_lines += f"\r\n{str(x)}"
            print(display_lines)
            displayText = f'stop {stopCode} is\r\n{str(stop)}' #.\r\nLines that pass here:{display_lines}'
        bot.send_message(message.chat.id, displayText, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, 'stop code must be numeric. Try again', parse_mode="Markdown")

bot.infinity_polling()
