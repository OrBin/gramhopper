import logging
from telegram import Update
from telegram.ext import CallbackContext


def handle_error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logging.error('Update "%s" caused error "%s" on bot "%s"', update, context.error, context.bot.name)
