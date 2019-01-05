from typing import NamedTuple, Dict, Type
from ruamel.yaml import YAML
from ruamel_yaml.comments import CommentedMap
from ..handlers.handler import Handler
from .triggers_reponses_parsers import TriggerParser, ResponseParser, BaseParser


class RulesParser:

    class TriggerOrResponseParams(NamedTuple):
        key: str
        globals: Dict
        parser: Type[BaseParser]

    def __init__(self):
        self.yaml = YAML()
        self.global_triggers = {}
        self.global_responses = {}
        self.trigger_params = RulesParser.TriggerOrResponseParams(key='trigger',
                                                                  globals=self.global_triggers,
                                                                  parser=TriggerParser)
        self.response_params = RulesParser.TriggerOrResponseParams(key='response',
                                                                   globals=self.global_responses,
                                                                   parser=ResponseParser)

    def parse_globals(self, config: CommentedMap):
        if 'triggers' in config:
            self.global_triggers.update(TriggerParser.parse_many(config['triggers']))

        if 'responses' in config:
            self.global_responses.update(ResponseParser.parse_many(config['responses']))

    def _parse_rule_trigger_or_response(self, rule: CommentedMap, params: TriggerOrResponseParams):
        # If the trigger/response here is just a name, look for it in the globals
        if isinstance(rule[params.key], str):
            return params.globals[rule[params.key]]

        return params.parser.parse_single(rule[params.key])

    def parse_single_rule(self, rule: CommentedMap):
        trigger = self._parse_rule_trigger_or_response(rule, self.trigger_params)
        response = self._parse_rule_trigger_or_response(rule, self.response_params)
        probability = rule['probability'] if 'probability' in rule else 1
        return Handler(trigger, response, probability=probability)

    def parse_file(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as stream:
            config = self.yaml.load(stream)

        self.parse_globals(config)

        return [self.parse_single_rule(rule) for rule in config['rules']]
