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
        pass

    @classmethod
    def parse_single(cls, config, globals):
        config_copy = dict(config)
        if 'name' in config_copy:
            config_copy.pop('name')

        mapping_cls = cls.mapping_class()
        element_cls = mapping_cls[config_copy.pop('type')]

        return element_cls(**config_copy)

    @classmethod
    def parse_many(cls, config, globals):
        return {
            element['name']: cls.parse_single(element, globals)
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
                    raise NotImplementedError(f'Origin type {origin_type} is currently not supported')
            elif isclass(type_hint) and issubclass(type_hint, BaseTrigger):
                parameters_to_parse.append(parameter_name)

        return parameters_to_parse


    @classmethod
    def parse_single(cls, config, globals):
        return BooleanHelper.parse_subrule_as_trigger_or_response(config,
                                                                  globals,
                                                                  cls.parse_single_recursively)
    @classmethod
    def parse_single_recursively(cls, config, globals):
        if isinstance(config, str):
            return globals[config]

        config_copy = dict(config)
        parameters_to_parse = cls.parameters_to_parse_as_trigger(config)
        config.pop('type')

        for parameter in parameters_to_parse:
            config_copy[parameter] = cls.parse_single(config[parameter], globals)

        return super().parse_single(config_copy, globals)


class ResponseParser(BaseParser):
    @staticmethod
    def mapping_class():
        return Responses
