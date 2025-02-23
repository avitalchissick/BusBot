import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
import Classes.BusesData as BusesData
import Utils.BusUtils as BusUtils
import time

# Your bot token obtained from BotFather
TOKEN = os.environ.get('BOT_TOKEN')

# Initializing bus data
t0 = time.time()
bus_data  = BusesData.BusData()
t1 = time.time()
print (t1-t0)

# Define states for conversation
MENU, STOP_ASK, LOCATION_ASK = range(3)

# Set up logging for the bot
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logger = logging.getLogger(__name__)

# Start command handler
async def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("הצגת קווים לפי מספר תחנה", callback_data="stop")],
        [InlineKeyboardButton("הצגת תחנות קרובות", callback_data="location")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "ברוכים הבאים לבוט תחבורה, בחרו אחת מהאפשרויות הבאות:", reply_markup=reply_markup
    )
    return MENU

# Button click handler
async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "stop":
        await query.edit_message_text(text="הכניסו מספר תחנה")
        return STOP_ASK
    elif query.data == "location":
        await query.edit_message_text(text="שלחו מיקום")
        return LOCATION_ASK
    else:
        await query.edit_message_text(text="נבחרה אפשרות לא ידועה")
        return MENU

async def stop_handler(update: Update, context: CallbackContext) -> int:
    stop_code = update.message.text
    display_text = BusUtils.get_stop_lines_text(bus_data,stop_code)
    await update.message.reply_text(display_text)
    return MENU

async def location_handler(update: Update, context: CallbackContext) -> int:
    location= update.message.location
    display_text = BusUtils.get_adjacent_stops_text(bus_data,location)
    await update.message.reply_text(display_text)
    return MENU

# Main function to start the bot
def main():
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    # ConversationHandler to handle the state machine
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [CallbackQueryHandler(button)],
            STOP_ASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, stop_handler)],
            LOCATION_ASK: [MessageHandler(filters.LOCATION & ~filters.COMMAND, location_handler)]
        },
        fallbacks=[CommandHandler("start", start)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()