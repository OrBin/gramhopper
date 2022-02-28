import abc
from typing import Dict, get_type_hints, Union, List, Any, Type
from inspect import isclass
from .partial_ruamel_yaml import CommentedMap, CommentedSeq
from .common_types import TriggerOrResponse, GlobalsDict
from .boolean_helper import BooleanHelper
from ..dict_enum import DictEnum


class TriggerOrResponseParser(abc.ABC):
    """ A common base parser for trigger/response configuration parsers"""

    def __init__(self, mapping_class: Type[DictEnum], element_base_class: Type[TriggerOrResponse]):
        self.__mapping_class = mapping_class
        self.__element_base_class = element_base_class

    @property
    def mapping_class(self) -> Type[DictEnum]:
        """ Returns the mapping class (`Triggers` or `Responses`)"""
        return self.__mapping_class

    @property
    def element_base_class(self) -> Type[TriggerOrResponse]:
        """ Returns the element base class (`BaseTrigger` or `BaseResponse`)"""
        return self.__element_base_class

    def parse_atomic(self, config: Dict[str, Any]) -> TriggerOrResponse:
        """
        Parses an atomic configuration subtree as a trigger/response
        :param config: A configuration subtree to parse
        :return: The trigger/response object created from the given configuration subtree
        """
        config_copy = dict(config)
        name = None
        if 'name' in config_copy:
            name = config_copy.pop('name')

        element = self.mapping_class[config_copy.pop('type')]

        # Some triggers (most of them) are classes and some are instances (mostly filter triggers).
        # This allows both cases to be used.
        # TODO: this comment does not seem to be correct any more. Try removing the case outside
        #  the "if" block; All triggers and responses seem to be classes.
        if isclass(element):
            trigger_or_response = element(**config_copy)
            if name:
                trigger_or_response.name = name
            return trigger_or_response
        return element

    def parse_single(self, config: Union[CommentedMap, str], global_elements: GlobalsDict) \
            -> TriggerOrResponse:
        """
        Recursively parses a single configuration subtree as a trigger/response
        :param config: A configuration subtree to parse
        :param global_elements: A dictionary with all triggers and responses configured globally
        :return: The trigger/response object created from the given configuration subtree
        """
        if isinstance(config, str):
            return BooleanHelper.parse_boolean_subrule(config, global_elements)

        config_copy = dict(config)
        parameters_to_parse = self.__find_parameters_to_parse_as_subelement(config)
        config.pop('type')

        for parameter in parameters_to_parse:
            config_copy[parameter] = self.parse_single(config[parameter], global_elements)

        return self.parse_atomic(config_copy)

    def parse_many(self, config: CommentedSeq, global_elements: GlobalsDict) \
            -> Dict[str, TriggerOrResponse]:
        """
        Parse all triggers/responses in a configuration
        :param config: A configuration subtree to config as a list of triggers/responses
        :param global_elements: A dictionary with all triggers and responses configured globally
        :return: A dictionary where keys are the original keys from the given configuration subtree
            and values are triggers/responses
        """
        return {
            element['name']: self.parse_single(element, global_elements)
            for element
            in config
        }

    def __find_parameters_to_parse_as_subelement(self, config: CommentedMap) -> List[str]:
        """
        Finds parameters in configuration which should be parsed as triggers/responses themselves
        (For example, when using a trigger/response that gets another trigger/response as a
        parameter).
        :param config: A configuration subtree to parse
        :return: List of the found parameter names
        """

        mapping_class_constructor = self.mapping_class[config['type']].__init__
        parameters_type_hints = get_type_hints(mapping_class_constructor)
        parameters_to_parse = []

        for parameter_name in config:

            # Meta-parameters to ignore
            if parameter_name in ['type', 'name']:
                continue

            # If this parameter has no type hint, we cannot check if it should be parsed or not
            if parameter_name not in parameters_type_hints:
                continue

            type_hint = parameters_type_hints[parameter_name]

            origin_type = getattr(type_hint, '__origin__', None)

            if origin_type is not None:
                if origin_type == Union:
                    if self.element_base_class in type_hint.__args__:
                        parameters_to_parse.append(parameter_name)
                else:
                    raise NotImplementedError(f'Origin type {origin_type} '
                                              f'is currently not supported')
            elif isclass(type_hint) and issubclass(type_hint, self.element_base_class):
                parameters_to_parse.append(parameter_name)

        return parameters_to_parse
