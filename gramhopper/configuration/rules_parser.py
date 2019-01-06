from ruamel.yaml import YAML
from ruamel_yaml.comments import CommentedMap
from boolean import boolean
from .trigger_response import TriggerResponse
from .boolean_operators import OPERATOR_TYPE_TO_FUNCTION
from ..handlers.handler import Handler
from .triggers_reponses_parsers import TriggerParser, ResponseParser
from .trigger_response_params import TriggerResponseParams, TriggerParams, ResponseParams


class RulesParser:

    def __init__(self):
        self.yaml = YAML()
        self.global_triggers = {}
        self.global_responses = {}
        self.trigger_params = TriggerParams(globals=self.global_triggers)
        self.response_params = ResponseParams(globals=self.global_responses)

    def parse_globals(self, config: CommentedMap):
        if 'triggers' in config:
            self.global_triggers.update(TriggerParser.parse_many(config['triggers']))

        if 'responses' in config:
            self.global_responses.update(ResponseParser.parse_many(config['responses']))

    def _evaluate_boolean_expression(self, expr: boolean.Expression, params: TriggerResponseParams) -> TriggerResponse:
        # If the trigger/response here is just a name, look for it in the globals
        if isinstance(expr, boolean.Symbol):
            return params.globals[str(expr)]

        boolean_function = OPERATOR_TYPE_TO_FUNCTION[type(expr)]
        evaluated_args = [self._evaluate_boolean_expression(arg, params) for arg in expr.args]
        return boolean_function(*evaluated_args)

    def _parse_rule_trigger_or_response(self, rule: CommentedMap, params: TriggerResponseParams) -> TriggerResponse:
        if isinstance(rule[params.key], str):
            algebra = boolean.BooleanAlgebra()
            parsed_expr = algebra.parse(rule[params.key])
            return self._evaluate_boolean_expression(parsed_expr, params)

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
