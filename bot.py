from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
    CallbackQueryHandler
)

# States
TEXT, BUTTON_TEXT, BUTTON_URL, CONFIRM = range(4)

# Your private channel ID
CHANNEL_ID = -1002678391495  

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✍️ Send me the main message text:")
    return TEXT

def get_text(update: Update, context: CallbackContext):
    context.user_data['message_text'] = update.message.text
    update.message.reply_text("🔘 Now send the inline button text:")
    return BUTTON_TEXT

def get_button_text(update: Update, context: CallbackContext):
    context.user_data['button_text'] = update.message.text
    update.message.reply_text("🌐 Finally, send the URL for the button:")
    return BUTTON_URL

def get_button_url(update: Update, context: CallbackContext):
    context.user_data['button_url'] = update.message.text

    # Preview message with button
    keyboard = [[InlineKeyboardButton(context.user_data['button_text'], url=context.user_data['button_url'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        text="👀 Preview of your post:\n\n" + context.user_data['message_text'],
        reply_markup=reply_markup
    )

    # Ask for confirmation
    confirm_keyboard = [
        [InlineKeyboardButton("✅ Yes, post it", callback_data="yes"),
         InlineKeyboardButton("❌ No, cancel", callback_data="no")]
    ]
    confirm_markup = InlineKeyboardMarkup(confirm_keyboard)

    update.message.reply_text("Do you want to post this to your channel?", reply_markup=confirm_markup)

    return CONFIRM

def confirm(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "yes":
        # Send to channel
        keyboard = [[InlineKeyboardButton(context.user_data['button_text'], url=context.user_data['button_url'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=context.user_data['message_text'],
            reply_markup=reply_markup
        )
        query.edit_message_text("✅ Message posted to your channel!")

    else:
        query.edit_message_text("❌ Cancelled. Nothing was posted.")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END

def main():
    TOKEN = "8190987979:AAGqLQxym3_45oM0W1hhwfl2t0XTM4ZUOT4"  # Replace with your bot token
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TEXT: [MessageHandler(Filters.text & ~Filters.command, get_text)],
            BUTTON_TEXT: [MessageHandler(Filters.text & ~Filters.command, get_button_text)],
            BUTTON_URL: [MessageHandler(Filters.text & ~Filters.command, get_button_url)],
            CONFIRM: [CallbackQueryHandler(confirm)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()