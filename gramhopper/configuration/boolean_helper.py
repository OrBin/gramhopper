from typing import Union, Callable
from boolean import boolean
from .partial_ruamel_yaml import CommentedMap
from .globals_dict import GlobalsDict
from .boolean_operators import OPERATOR_TYPE_TO_FUNCTION
from .trigger_response import TriggerResponse


class BooleanHelper:
    """
    A helper class for parsing boolean algebra expressions.
    """

    ParsingFunction = Callable[[Union[CommentedMap, str], GlobalsDict],
                               TriggerResponse]

    @staticmethod
    def evaluate_boolean_expression(expr: boolean.Expression,
                                    global_elements: GlobalsDict) -> TriggerResponse:
        """
        Convert a boolean expression into a `BaseTrigger`/`BaseResponse` object
        :param expr: A boolean expression parsed from a subrule (a configuration subtree)
        :param global_elements: A dictionary with all triggers and responses configured globally
        :return: The trigger/response object created from the given boolean expression
        """
        # If the trigger/response here is just a name, look for it in the globals
        if isinstance(expr, boolean.Symbol):
            return global_elements[str(expr)]

        boolean_function = OPERATOR_TYPE_TO_FUNCTION[type(expr)]
        evaluated_args = [BooleanHelper.evaluate_boolean_expression(arg, global_elements)
                          for arg
                          in expr.args]
        return boolean_function(*evaluated_args)

    @staticmethod
    def parse_subrule_as_trigger_or_response(subrule: Union[CommentedMap, str],
                                             global_elements: GlobalsDict,
                                             parsing_func: ParsingFunction) -> TriggerResponse:
        """
        Convert a subrule (a configuration subtree) into a `BaseTrigger`/`BaseResponse` object
        :param subrule: A subrule (a configuration subtree)
        :param global_elements: A dictionary with all triggers and responses configured globally
        :param parsing_func: A specific parsing function (for the specific subrule type to parse)
        :return: The trigger/response object created from the given subrule
        """
        if isinstance(subrule, str):
            algebra = boolean.BooleanAlgebra()
            parsed_expr = algebra.parse(subrule)
            return BooleanHelper.evaluate_boolean_expression(parsed_expr, global_elements)

        return parsing_func(subrule, global_elements)
