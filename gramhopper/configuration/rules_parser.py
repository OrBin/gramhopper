from typing import Union, Callable
from operator import or_ as or_operator, and_ as and_operator
from ruamel.yaml import YAML
from ruamel_yaml.comments import CommentedMap
from boolean import boolean
from ..responses.basic_responses import BaseResponse
from ..triggers.basic_triggers import BaseTrigger
from ..handlers.handler import Handler
from .triggers_reponses_parsers import TriggerParser, ResponseParser
from .trigger_response_params import TriggerResponseParams


class RulesParser:

    # Type definitions for type hints
    TriggerOrResponse = Union[BaseTrigger, BaseResponse]
    MergeFunction = Callable[[TriggerOrResponse, TriggerOrResponse], TriggerOrResponse]

    def __init__(self):
        self.yaml = YAML()
        self.algebra = boolean.BooleanAlgebra()
        self.global_triggers = {}
        self.global_responses = {}
        self.trigger_params = TriggerResponseParams(key='trigger',
                                                    globals=self.global_triggers,
                                                    parser=TriggerParser)
        self.response_params = TriggerResponseParams(key='response',
                                                     globals=self.global_responses,
                                                     parser=ResponseParser)

    def parse_globals(self, config: CommentedMap):
        if 'triggers' in config:
            self.global_triggers.update(TriggerParser.parse_many(config['triggers']))

        if 'responses' in config:
            self.global_responses.update(ResponseParser.parse_many(config['responses']))

    def _parse_and_or_expression(self,
                                 expr: Union[boolean.AND, boolean.OR],
                                 merge_function: MergeFunction,
                                 params: TriggerResponseParams) -> TriggerOrResponse:
        args = list(expr.args)
        merged = self._parse_boolean_expression(args.pop(0), params)
        for arg in args:
            other = self._parse_boolean_expression(arg, params)
            merged = merge_function(merged, other)
        return merged

    def _parse_boolean_expression(self, expr: boolean.Expression, params: TriggerResponseParams) -> TriggerOrResponse:
        if isinstance(expr, boolean.AND):
            return self._parse_and_or_expression(expr, and_operator, params)
        elif isinstance(expr, boolean.OR):
            return self._parse_and_or_expression(expr, or_operator, params)
        elif isinstance(expr, boolean.NOT):
            return ~self._parse_boolean_expression(expr.args[0], params)
        elif isinstance(expr, boolean.Symbol):
            # If the trigger/response here is just a name, look for it in the globals
            return params.globals[str(expr)]

    def _parse_rule_trigger_or_response(self,
                                        rule: CommentedMap,
                                        params: TriggerResponseParams) -> TriggerOrResponse:
        if isinstance(rule[params.key], str):
            parsed_expr = self.algebra.parse(rule[params.key])
            if isinstance(parsed_expr, boolean.Symbol):
                # If the trigger/response here is just a name, look for it in the globals
                return params.globals[rule[params.key]]
            else:
                return self._parse_boolean_expression(parsed_expr, params)

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
