import abc
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

        if config['type'] == Triggers.event_streak.name:
            if 'counting_event_trigger' in config:
                config_copy['counting_event_trigger'] = cls.parse_single(config['counting_event_trigger'], globals)

            if 'resetting_event_trigger' in config:
                config_copy['resetting_event_trigger'] = cls.parse_single(config['resetting_event_trigger'], globals)


        return super().parse_single(config_copy, globals)


class ResponseParser(BaseParser):
    @staticmethod
    def mapping_class():
        return Responses
