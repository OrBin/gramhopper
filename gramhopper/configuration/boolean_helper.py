from typing import Dict, Union, Callable
from boolean import boolean
from ruamel_yaml.comments import CommentedMap
from .boolean_operators import OPERATOR_TYPE_TO_FUNCTION
from .trigger_response import TriggerResponse

class BooleanHelper:

    @staticmethod
    def evaluate_boolean_expression(expr: boolean.Expression,
                                    globals: Dict[str, TriggerResponse]) -> TriggerResponse:
        # If the trigger/response here is just a name, look for it in the globals
        if isinstance(expr, boolean.Symbol):
            return globals[str(expr)]

        boolean_function = OPERATOR_TYPE_TO_FUNCTION[type(expr)]
        evaluated_args = [BooleanHelper.evaluate_boolean_expression(arg, globals)
                          for arg
                          in expr.args]
        return boolean_function(*evaluated_args)

    @staticmethod
    def parse_subrule_as_trigger_or_response(subrule: Union[CommentedMap, str],
                                             globals: Dict[str, TriggerResponse],
                                             parsing_func: Callable[[Union[CommentedMap, str], Dict[str, TriggerResponse]], TriggerResponse]) -> TriggerResponse:
        if isinstance(subrule, str):
            algebra = boolean.BooleanAlgebra()
            parsed_expr = algebra.parse(subrule)
            return BooleanHelper.evaluate_boolean_expression(parsed_expr, globals)

        return parsing_func(subrule, globals)
