import logging
from telegram.ext import Updater
from .logging_config import configure_logger
from .paths import token_file_path, default_rules_file_path
from .configuration.rules_parser import RulesParser
from .handlers.combined_handlers import CombinedConversationHandler
from .handlers.default_error_handler import handle_error


def start_bot():
    configure_logger()

    with open(token_file_path(), 'r') as token_file:
        bot_token = token_file.read().strip()

    rule_parser = RulesParser()
    rules_file_path = default_rules_file_path()
    logging.info('Reading and parsing rules file from %s', rules_file_path)
    rule_handlers = rule_parser.parse_file(rules_file_path)
    logging.info('Found %d rules', len(rule_handlers))
    conversation_handler = CombinedConversationHandler(rule_handlers)

    logging.info('Creating bot updater')
    updater = Updater(bot_token)
    updater.dispatcher.add_handler(conversation_handler)
    updater.dispatcher.add_error_handler(handle_error)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    logging.info('Moving the bot to idle mode to keep listening to updates')
    updater.idle()
