

# TELEGRAM_BOT_TOKEN = '7485708002:AAEy-gCr1lG9ZX6AXxpJdbo6GjA6xtJ5L5U'


from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your bot's API token
TELEGRAM_BOT_TOKEN = '7485708002:AAEy-gCr1lG9ZX6AXxpJdbo6GjA6xtJ5L5U'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Please send me the SSID and password in the format: SSID,PASSWORD')

async def validate_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    try:
        ssid, password = user_input.split(',')
        if len(ssid) > 0 and len(password) > 0:
            await update.message.reply_text(f"SSID: {ssid}\nPassword: {password}\n\nPlease go to your device's WiFi settings and connect to the network manually.")
        else:
            await update.message.reply_text("Invalid input. SSID and password cannot be empty.")
    except ValueError:
        await update.message.reply_text("Invalid format. Please send the SSID and password in the format: SSID,PASSWORD")

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add the start command handler
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    # Add the message handler for validating input
    validate_input_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, validate_input)
    application.add_handler(validate_input_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()