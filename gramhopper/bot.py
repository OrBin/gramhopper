import logging
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional

from telegram.ext import Updater
from .logging_config import configure_logger
from .paths import TOKEN_FILE_PATH, DEFAULT_RULES_FILE_PATH
from .configuration.rules_parser import RulesParser
from .handlers.combined_handlers import CombinedConversationHandler
from .handlers.default_error_handler import handle_error


def _get_rules_file_path(config_path_input: Optional[str]):
    if config_path_input:
        config_path = os.path.expanduser(os.path.expandvars(config_path_input))
        if os.access(config_path, os.R_OK):
            return Path(config_path)

        logging.warning(f'Cannot read {config_path}, defaulting to {DEFAULT_RULES_FILE_PATH}')

    return DEFAULT_RULES_FILE_PATH


def start_bot():
    """ Configures and runs the bot """
    configure_logger()

    parser = ArgumentParser(description='A rule-based Telegram bot engine, no coding required')
    parser.add_argument('--config', action='store', type=str, help='specify configuration file')
    args = parser.parse_args()
    logging.debug(f'Parsed arguments: {args}')

    bot_token = TOKEN_FILE_PATH.read_text().strip()

    rule_parser = RulesParser()

    rules_file_path = _get_rules_file_path(args.config)
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
