import abc
from typing import Dict, get_type_hints, Union, List, Any, Type
from inspect import isclass
from .partial_ruamel_yaml import CommentedMap, CommentedSeq
from .common_types import TriggerResponse, GlobalsDict
from .boolean_helper import BooleanHelper
from ..dict_enum import DictEnum
from ..triggers.basic_triggers import BaseTrigger
from ..responses.basic_responses import BaseResponse
from ..responses import Responses
from ..triggers import Triggers


class BaseParser(abc.ABC):
    """ A common base parser for trigger/response configuration parsers s"""

    @staticmethod
    @abc.abstractmethod
    def mapping_class() -> Type[DictEnum]:
        """ Returns the mapping class (`Triggers` or `Responses`)"""
        raise NotImplementedError()

    @staticmethod
    @abc.abstractmethod
    def element_base_class() -> Type[TriggerResponse]:
        """ Returns the element base class (`BaseTrigger` or `BaseResponse`)"""
        raise NotImplementedError()

    @classmethod
    def parse_atomic(cls,
                     config: Dict[str, Any],
                     global_elements: GlobalsDict) -> TriggerResponse:  # pylint: disable=unused-argument
        """
        Parses an atomic configuration subtree as a trigger/response
        :param config: A configuration subtree to parse
        :param global_elements: A dictionary with all triggers and responses configured globally
        :return: The trigger/response object created from the given configuration subtree
        """
        config_copy = dict(config)
        name = None
        if 'name' in config_copy:
            name = config_copy.pop('name')

        mapping_class = cls.mapping_class()
        element = mapping_class[config_copy.pop('type')]

        # Some triggers (most of them) are classes and some are instances (mostly filter triggers).
        # This allows both cases to be used.
        if isclass(element):
            trigger_or_response = element(**config_copy)
            if name:
                trigger_or_response.name = name
            return trigger_or_response
        return element

    @classmethod
    def parse_single(cls, config: Dict[str, Any], global_elements: GlobalsDict) \
            -> TriggerResponse:
        """
        Parses a single configuration subtree as a trigger/response
        :param config: A configuration subtree to parse
        :param global_elements: A dictionary with all triggers and responses configured globally
        :return: The trigger/response object created from the given configuration subtree
        """
        return BooleanHelper.parse_subrule_as_trigger_or_response(config,
                                                                  global_elements,
                                                                  cls._parse_single_recursively)

    @classmethod
    def parse_many(cls, config: CommentedSeq, global_elements: GlobalsDict) \
            -> Dict[str, TriggerResponse]:
        """
        Parse all triggers/responses in a configuration
        :param config: A configuration subtree to config as a list of triggers/responses
        :param global_elements: A dictionary with all triggers and responses configured globally
        :return: A dictionary where keys are the original keys from the given configuration subtree
            and values are triggers/responses
        """
        return {
            element['name']: cls.parse_single(element, global_elements)
            for element
            in config
        }

    @classmethod
    def parameters_to_parse_as_subelement(cls, config: CommentedMap) -> List[str]:
        """
        Finds parameters in configuration which should be parsed as triggers/responses themselves
        (For example, when using a trigger/response that gets another trigger/response as a
        parameter).
        :param config: A configuration subtree to parse
        :return: List of the found parameter names
        """
        mapping_class = cls.mapping_class()
        element_base_class = cls.element_base_class()

        mapping_class_constructor = mapping_class[config['type']].__init__
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
                    if element_base_class in type_hint.__args__:
                        parameters_to_parse.append(parameter_name)
                else:
                    raise NotImplementedError(f'Origin type {origin_type} '
                                              f'is currently not supported')
            elif isclass(type_hint) and issubclass(type_hint, element_base_class):
                parameters_to_parse.append(parameter_name)

        return parameters_to_parse

    @classmethod
    def _parse_single_recursively(cls, config: CommentedMap, global_elements: GlobalsDict) \
            -> TriggerResponse:
        """
        Recursively parses a single configuration subtree as a trigger/response
        :param config: A configuration subtree to parse
        :param global_elements: A dictionary with all triggers and responses configured globally
        :return: The trigger/response object created from the given configuration subtree
        """
        if isinstance(config, str):
            return global_elements[config]

        config_copy = dict(config)
        parameters_to_parse = cls.parameters_to_parse_as_subelement(config)
        config.pop('type')

        for parameter in parameters_to_parse:
            config_copy[parameter] = cls.parse_single(config[parameter], global_elements)

        return cls.parse_atomic(config_copy, global_elements)


class TriggerParser(BaseParser):
    """ A parser for trigger configuration """

    @staticmethod
    def mapping_class() -> Type[DictEnum]:
        return Triggers

    @staticmethod
    def element_base_class() -> Type[TriggerResponse]:
        return BaseTrigger


class ResponseParser(BaseParser):
    """ A parser for response configuration """

    @staticmethod
    def mapping_class() -> Type[DictEnum]:
        return Responses

    @staticmethod
    def element_base_class() -> Type[TriggerResponse]:
        return BaseResponse
