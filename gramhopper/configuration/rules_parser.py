from ruamel.yaml import YAML
from ruamel_yaml.comments import CommentedMap

from .params_manager import ParamsManager
from .rules_parsing_helper import RulesParsingHelper
from ..handlers.handler import Handler
#from .trigger_response_params import TriggerParams, ResponseParams


class RulesParser:

    def __init__(self):
        self.yaml = YAML()
        #self.global_triggers = {}
        #self.global_responses = {}
        self.trigger_params = ParamsManager.get_trigger_params() # TriggerParams(globals={})
        self.response_params = ParamsManager.get_response_params() # ResponseParams(globals={})

    def parse_globals(self, config: CommentedMap):
        RulesParsingHelper.add_globals(config, self.trigger_params)
        RulesParsingHelper.add_globals(config, self.response_params)

    def parse_single_rule(self, rule: CommentedMap):
        trigger = RulesParsingHelper.parse_rule_trigger_or_response(rule, self.trigger_params)
        response = RulesParsingHelper.parse_rule_trigger_or_response(rule, self.response_params)
        probability = rule['probability'] if 'probability' in rule else 1
        return Handler(trigger, response, probability=probability)

    def parse_file(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as stream:
            config = self.yaml.load(stream)

        self.parse_globals(config)

        return [self.parse_single_rule(rule) for rule in config['rules']]
