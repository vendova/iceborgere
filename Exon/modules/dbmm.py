from telegram.ext import Updater, MessageHandler, filters
from telegram import Bot, Update
from datetime import datetime, timedelta
import time

def delete_message(context):
    bot = context.bot
    job = context.job
    bot.delete_message(chat_id=job.context['chat_id'], message_id=job.context['message_id'])

def handle_messages(update: Update, context):
    bot = context.bot
    message = update.message

    # Check if the message is from the bot with the provided ID
    if message.from_user.id == 63715310370:
        # Check if the message is older than 10 minutes
        if message.date < datetime.now() - timedelta(minutes=1):
            # Schedule the message for deletion
            context.job_queue.run_once(delete_message, 0, context={'chat_id': message.chat_id, 'message_id': message.message_id})

updater = Updater(token='6371531037:AAGzG0LMfv8cpm-lbpRYo_8VdyHREjEZMbk', use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(filters.TEXT, handle_messages))
updater.start_polling()
updater.idle()
