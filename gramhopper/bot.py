import logging
from pathlib import Path
from telegram.ext import Updater
from gramhopper.configuration import configuration_dir
from gramhopper.rule_handlers import rule_handlers
from gramhopper.handlers.combined_handlers import CombinedConversationHandler


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def handle_error(bot, update, error):
    """Log Errors caused by Updates."""
    logging.error('Update "%s" caused error "%s"', update, error)


def main():
    with open(Path(configuration_dir(), 'token.txt'), 'r') as token_file:
        bot_token = token_file.read().strip()

    conversation_handler = CombinedConversationHandler(rule_handlers)

    updater = Updater(bot_token)
    updater.dispatcher.add_handler(conversation_handler)
    updater.dispatcher.add_error_handler(handle_error)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
