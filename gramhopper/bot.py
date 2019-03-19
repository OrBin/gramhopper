import logging
from telegram.ext import Updater
from .configuration import token_file_path, rules_file_path
from .configuration.rules_parser import RulesParser
from .handlers.combined_handlers import CombinedConversationHandler
from .handlers.default_error_handler import handle_error


def start_bot():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    with open(token_file_path(), 'r') as token_file:
        bot_token = token_file.read().strip()

    rule_parser = RulesParser()
    rule_handlers = rule_parser.parse_file(rules_file_path())
    conversation_handler = CombinedConversationHandler(rule_handlers)

    updater = Updater(bot_token)
    updater.dispatcher.add_handler(conversation_handler)
    updater.dispatcher.add_error_handler(handle_error)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
