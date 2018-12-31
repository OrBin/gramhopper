from ruamel.yaml import YAML
from gramhopper.handlers.handler import Handler
from .triggers_reponses_parsers import TriggerParser, ResponseParser


class RuleParser:

    def __init__(self):
        self.yaml = YAML()

    def parse_globals(self, config):
        if 'triggers' in config:
            self.global_triggers = TriggerParser.parse_many(config['triggers'])

        if 'responses' in config:
            self.global_responses = ResponseParser.parse_many(config['responses'])

    def _parse_rule_trigger_or_response(self, rule, key, globals, parser):
        if isinstance(rule[key], str):
            return globals[rule[key]]
        else:
            return parser.parse_single(rule[key])

    _parse_rule_trigger = lambda self, rule: self._parse_rule_trigger_or_response(rule, 'trigger', self.global_triggers, TriggerParser)
    _parse_rule_response = lambda self, rule: self._parse_rule_trigger_or_response(rule, 'response', self.global_responses, ResponseParser)

    def parse_single_rule(self, rule):
        trigger = self._parse_rule_trigger(rule)
        response = self._parse_rule_response(rule)
        probability = rule['probability'] if 'probability' in rule else 1
        return Handler(trigger, response, probability=probability)

    def parse_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as stream:
            config = self.yaml.load(stream)

        self.parse_globals(config)

        return [self.parse_single_rule(rule) for rule in config['rules']]
