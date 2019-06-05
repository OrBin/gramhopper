import abc
import typing
from inspect import isclass
from .boolean_helper import BooleanHelper
from ..triggers.basic_triggers import BaseTrigger
from ..responses import Responses
from ..triggers import Triggers


class BaseParser(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def mapping_class():
        """ Returns the mapping class (`Triggers` or `Responses`)"""

    @classmethod
    def parse_single(cls, config, global_elements):  # pylint: disable=unused-argument
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
    def parse_many(cls, config, global_elements):
        return {
            element['name']: cls.parse_single(element, global_elements)
            for element
            in config
        }


class TriggerParser(BaseParser):
    @staticmethod
    def mapping_class():
        return Triggers

    @classmethod
    def parameters_to_parse_as_trigger(cls, config):
        trigger_class = Triggers[config['type']]
        parameters_type_hints = typing.get_type_hints(trigger_class.__init__)
        parameters_to_parse = []

        for parameter_name in config:

            # Meta-parameters to ignore
            if parameter_name in ['type', 'name']:
                continue

            # If this parameter has not type hint, we cannot check if it's a trigger or not
            if parameter_name not in parameters_type_hints:
                continue

            type_hint = parameters_type_hints[parameter_name]

            origin_type = getattr(type_hint, '__origin__', None)

            if origin_type is not None:
                if origin_type == typing.Union:
                    if BaseTrigger in type_hint.__args__:
                        parameters_to_parse.append(parameter_name)
                else:
                    raise NotImplementedError(f'Origin type {origin_type} '
                                              f'is currently not supported')
            elif isclass(type_hint) and issubclass(type_hint, BaseTrigger):
                parameters_to_parse.append(parameter_name)

        return parameters_to_parse

    @classmethod
    def parse_single(cls, config, global_elements):
        return BooleanHelper.parse_subrule_as_trigger_or_response(config,
                                                                  global_elements,
                                                                  cls.parse_single_recursively)

    @classmethod
    def parse_single_recursively(cls, config, global_elements):
        if isinstance(config, str):
            return global_elements[config]

        config_copy = dict(config)
        parameters_to_parse = cls.parameters_to_parse_as_trigger(config)
        config.pop('type')

        for parameter in parameters_to_parse:
            config_copy[parameter] = cls.parse_single(config[parameter], global_elements)

        return super().parse_single(config_copy, global_elements)


class ResponseParser(BaseParser):
    @staticmethod
    def mapping_class():
        return Responses
