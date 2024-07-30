import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import subprocess

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

SSID, PASSWORD = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Hi! I can help you connect to a Wi-Fi network. Please send me the SSID.')
    return SSID

async def ssid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['ssid'] = update.message.text
    await update.message.reply_text('Got it! Now, please send me the password.')
    return PASSWORD

async def password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['password'] = update.message.text
    ssid = context.user_data['ssid']
    password = context.user_data['password']
    
    # Verify and connect to Wi-Fi
    if verify_and_connect(ssid, password):
        await update.message.reply_text(f'Successfully connected to {ssid}!')
    else:
        await update.message.reply_text(f'Failed to connect to {ssid}. Please check your credentials and try again.')

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def verify_and_connect(ssid, password):
    try:
        # Verify SSID
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], capture_output=True, text=True)
        available_ssids = result.stdout.split('\n')
        if ssid not in available_ssids:
            return False
        
        # Connect to Wi-Fi
        result = subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        logger.error(f'Error connecting to Wi-Fi: {e}')
        return False

def main():
    # Replace 'YOUR_API_TOKEN' with your bot's API token
    application = Application.builder().token('7485708002:AAEy-gCr1lG9ZX6AXxpJdbo6GjA6xtJ5L5U').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SSID: [MessageHandler(filters.TEXT & ~filters.COMMAND, ssid)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()