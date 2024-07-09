import telebot

BOT_TOKEN = '7485708002:AAEy-gCr1lG9ZX6AXxpJdbo6GjA6xtJ5L5U'
GROUP_CHAT_ID = -4218196722

bot = telebot.TeleBot(BOT_TOKEN)

def send_to_telegram_group(message):
    bot.send_message(GROUP_CHAT_ID, message)