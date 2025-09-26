import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# -----------------------------
# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Replace with your own info
BOT_TOKEN = "8190987979:AAGqLQxym3_45oM0W1hhwfl2t0XTM4ZUOT4"
CHANNEL_ID = -1002678391495   # Your channel ID
ADMIN_ID = 7282835498         # Only you can use the bot

# States
ASK_TEXT, ASK_BTN_TEXT, ASK_BTN_URL = range(3)

# -----------------------------
# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("🚫 Access Denied! Only the channel admin can use this bot.")
        return ConversationHandler.END

    # Fake animation for verifying admin
    msg = await update.message.reply_text("🔐 Verifying admin...")
    await asyncio.sleep(1)
    await msg.edit_text("🔐 Verifying admin... ▓░░░")
    await asyncio.sleep(1)
    await msg.edit_text("🔐 Verifying admin... ▓▓░░")
    await asyncio.sleep(1)
    await msg.edit_text("🔐 Verifying admin... ▓▓▓░")
    await asyncio.sleep(1)
    await msg.edit_text("✅ Access granted! Welcome boss 😎")

    await asyncio.sleep(1)
    await update.message.reply_text("✍️ Send me the message text you want to post:")
    return ASK_TEXT

# -----------------------------
# Step 1 - Get message text
async def get_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["msg_text"] = update.message.text
    await update.message.reply_text("🔘 Now send me the button text:")
    return ASK_BTN_TEXT

# -----------------------------
# Step 2 - Get button text
async def get_button_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["btn_text"] = update.message.text
    await update.message.reply_text("🌐 Finally, send me the button URL:")
    return ASK_BTN_URL

# -----------------------------
# Step 3 - Get button URL and post to channel
async def get_button_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_text = context.user_data["msg_text"]
    btn_text = context.user_data["btn_text"]
    btn_url = update.message.text

    keyboard = [[InlineKeyboardButton(btn_text, url=btn_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send to channel
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=msg_text,
        reply_markup=reply_markup
    )

    await update.message.reply_text("✅ Posted to channel successfully!")
    return ConversationHandler.END

# -----------------------------
# Cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END

# -----------------------------
# Main
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_text)],
            ASK_BTN_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_button_text)],
            ASK_BTN_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_button_url)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)

    print("🤖 Bot started...")
    app.run_polling()

# -----------------------------
if __name__ == "__main__":
    main()
