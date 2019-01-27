from boolean import boolean
from ruamel_yaml.comments import CommentedMap
from .boolean_operators import OPERATOR_TYPE_TO_FUNCTION
from .trigger_response import TriggerResponse
from .trigger_response_params import TriggerResponseParams


class RulesParsingHelper:

    @staticmethod
    def add_globals(config: CommentedMap, params: TriggerResponseParams) -> None:
        """
        Adds globals (a generic name for "global triggers" and "global responses")
        from *config* to *params.globals*.

        Globals are triggers and responses which are defined generally in the rules file,
        as opposed to those defined inside a specific rule.

        :param config: The configuration subroot from which the function reads the
        triggers/responses.
        :param params: The trigger/response parameters whose globals should be updated.
        :return: None
        """
        if params.plural_key in config:
            parsed = params.parser.parse_many(config[params.plural_key], params.globals)
            params.globals.update(parsed)

    @staticmethod
    def evaluate_boolean_expression(expr: boolean.Expression,
                                    params: TriggerResponseParams) -> TriggerResponse:
        # If the trigger/response here is just a name, look for it in the globals
        if isinstance(expr, boolean.Symbol):
            return params.globals[str(expr)]

        boolean_function = OPERATOR_TYPE_TO_FUNCTION[type(expr)]
        evaluated_args = [RulesParsingHelper.evaluate_boolean_expression(arg, params)
                          for arg
                          in expr.args]
        return boolean_function(*evaluated_args)

    @staticmethod
    def parse_rule_trigger_or_response(rule: CommentedMap,
                                       params: TriggerResponseParams) -> TriggerResponse:
        if isinstance(rule[params.singular_key], str):
            algebra = boolean.BooleanAlgebra()
            parsed_expr = algebra.parse(rule[params.singular_key])
            return RulesParsingHelper.evaluate_boolean_expression(parsed_expr, params)

        return params.parser.parse_single(rule[params.singular_key])
