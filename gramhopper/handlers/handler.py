import logging
import random
from telegram import Update, Bot
from ..responses.basic_responses import BaseResponse
from ..triggers.basic_triggers import BaseTrigger


class Handler():
    def __init__(self,
                 trigger_checker: BaseTrigger,
                 responder: BaseResponse,
                 probability: float = 1):
        self.trigger_checker = trigger_checker
        self.responder = responder

        self.handler_repr = f'{self.trigger_checker} -> {self.responder}'
        self.handler_repr = f'{self.handler_repr:70}'

        if probability > 1 or probability <= 0:
            raise ValueError(f'Parameter \'probability\' should be in range (0, 1], '
                             f'but {probability} was given')

        self.probability_to_respond = probability

    def handle(self, bot: Bot, update: Update):
        logging.debug('[%s] Received update %s', self.handler_repr, update.update_id)
        trigger_result = self.trigger_checker.check_trigger(update)
        if trigger_result.should_respond:
            logging.info('[%s] Bot should respond to update %s with a probability of %f',
                         self.handler_repr,
                         update.update_id,
                         self.probability_to_respond)
            if random.random() <= self.probability_to_respond:
                logging.info('[%s] Responding to update %s', self.handler_repr, update.update_id)
                self.responder.respond(bot, update, trigger_result.response_payload)
