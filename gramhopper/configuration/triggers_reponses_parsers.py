import abc
import typing
from inspect import isclass
from gramhopper.triggers.basic_triggers import BaseTrigger
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
    def parse_single(cls, config, globals):
        if isinstance(config, str):
            return globals[config]

        config_copy = dict(config)

        trigger_class = Triggers[config['type']]

        if config['type'] == Triggers.event_streak.name:


            parameters_type_hints = typing.get_type_hints(trigger_class.__init__)
            config.pop('type')

            for parameter_name in config:

                # Meta-parameters to ignore
                if parameter_name in ['type', 'name']:
                    continue

                should_parse_parameter = False
                type_hint = parameters_type_hints[parameter_name]
                origin_type = getattr(type_hint, '__origin__', None)

                if origin_type is not None:
                    if origin_type == typing.Union:
                        if BaseTrigger in type_hint.__args__:
                            should_parse_parameter = True
                    else:
                        raise NotImplementedError(f'Origin type {origin_type} is currently not supported')

                elif isclass(type_hint) and issubclass(type_hint, BaseTrigger):
                    should_parse_parameter = True

                if should_parse_parameter:
                    print(parameter_name)
                    config_copy[parameter_name] = cls.parse_single(config[parameter_name], globals)

        return super().parse_single(config_copy, globals)


class ResponseParser(BaseParser):
    @staticmethod
    def mapping_class():
        return Responses
