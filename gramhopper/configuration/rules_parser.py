import logging
from os import PathLike
from typing import Union, List
from ruamel.yaml import YAML
from ruamel.yaml import CommentedMap
from .rules_parsing_helper import RulesParsingHelper
from ..handlers.rules_handler import RuleHandler
from .trigger_or_response_params import TriggerParams, ResponseParams


class RulesParser:

    def __init__(self):
        self.yaml = YAML()
        self.global_triggers = {}
        self.global_responses = {}
        self.trigger_params = TriggerParams(global_elements=self.global_triggers)
        self.response_params = ResponseParams(global_elements=self.global_responses)

    def parse_globals(self, config: CommentedMap) -> None:
        RulesParsingHelper.add_globals(config, self.trigger_params)
        RulesParsingHelper.add_globals(config, self.response_params)

    def parse_single_rule(self, rule: CommentedMap) -> RuleHandler:
        trigger = RulesParsingHelper.parse_rule_trigger_or_response(rule, self.trigger_params)
        response = RulesParsingHelper.parse_rule_trigger_or_response(rule, self.response_params)
        probability = rule['probability'] if 'probability' in rule else 1
        handler = RuleHandler(trigger, response, probability=probability)
        logging.info('Parsed %s', handler.handler_repr)
        return handler

    def parse_file(self, file_path: Union[PathLike, str, bytes]) -> List[RuleHandler]:
        with open(file_path, 'r', encoding='utf-8') as stream:
            config = self.yaml.load(stream)

        logging.info('Parsing globals from %s', file_path)
        self.parse_globals(config)

        logging.info('Parsing rules from %s', file_path)
        return [self.parse_single_rule(rule) for rule in config['rules']]
