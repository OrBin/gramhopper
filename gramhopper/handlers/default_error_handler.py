import logging
from telegram import Bot, Update, TelegramError


def handle_error(bot: Bot, update: Update, error: TelegramError):
    """Log Errors caused by Updates."""
    logging.error('Update "%s" caused error "%s" on bot "%s"', update, error, bot.name)
