from boolean import boolean
from ruamel_yaml.comments import CommentedMap
from .boolean_operators import OPERATOR_TYPE_TO_FUNCTION
from .trigger_response import TriggerResponse
from .trigger_response_params import TriggerResponseParams


class RulesParsingHelper:

    @staticmethod
    def _add_globals(config: CommentedMap, params: TriggerResponseParams):
        if params.plural_key in config:
            params.globals.update(params.parser.parse_many(config[params.plural_key]))

    @staticmethod
    def _evaluate_boolean_expression(expr: boolean.Expression, params: TriggerResponseParams) -> TriggerResponse:
        # If the trigger/response here is just a name, look for it in the globals
        if isinstance(expr, boolean.Symbol):
            return params.globals[str(expr)]

        boolean_function = OPERATOR_TYPE_TO_FUNCTION[type(expr)]
        evaluated_args = [RulesParsingHelper._evaluate_boolean_expression(arg, params) for arg in expr.args]
        return boolean_function(*evaluated_args)

    @staticmethod
    def _parse_rule_trigger_or_response(rule: CommentedMap, params: TriggerResponseParams) -> TriggerResponse:
        if isinstance(rule[params.singular_key], str):
            algebra = boolean.BooleanAlgebra()
            parsed_expr = algebra.parse(rule[params.singular_key])
            return RulesParsingHelper._evaluate_boolean_expression(parsed_expr, params)

        return params.parser.parse_single(rule[params.singular_key])
