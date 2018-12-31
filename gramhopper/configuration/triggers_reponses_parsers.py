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
    def parse_single(cls, config):
        config_copy = dict(config)
        if 'name' in config_copy:
            config_copy.pop('name')

        mapping_cls = cls.mapping_class()
        element_cls = mapping_cls[config_copy.pop('type')]

        return element_cls(**config_copy)

    @classmethod
    def parse_many(cls, config):
        return {
            element['name']: cls.parse_single(element)
            for element
            in config
        }


class TriggerParser(BaseParser):
    @staticmethod
    def mapping_class():
        return Triggers


class ResponseParser(BaseParser):
    @staticmethod
    def mapping_class():
        return Responses
