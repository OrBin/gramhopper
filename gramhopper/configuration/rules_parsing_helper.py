from .partial_ruamel_yaml import CommentedMap
from .boolean_helper import BooleanHelper
from .common_types import TriggerOrResponse
from .trigger_or_response_params import TriggerOrResponseParams


class RulesParsingHelper:

    @staticmethod
    def add_globals(config: CommentedMap, params: TriggerOrResponseParams) -> None:
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
            parsed = params.parser.parse_many(config[params.plural_key], params.global_elements)
            params.global_elements.update(parsed)

    @staticmethod
    def parse_rule_trigger_or_response(rule: CommentedMap,
                                       params: TriggerOrResponseParams) -> TriggerOrResponse:

        subrule = rule[params.singular_key]

        if isinstance(subrule, str):
            return BooleanHelper.parse_boolean_subrule(subrule, params.global_elements)

        return params.parser.parse_single(subrule, params.global_elements)
