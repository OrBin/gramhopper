from ruamel.yaml import YAML
from gramhopper.handlers.handler import Handler
from ..responses import Responses
from ..triggers import Triggers


def _parse_trigger_or_response(config, mapping_cls):
    config_copy = dict(config)
    if 'name' in config_copy:
        config_copy.pop('name')

    trigger_or_response_class = mapping_cls[config_copy['type']]
    config_copy.pop('type')

    return trigger_or_response_class(**config_copy)


def _parse_trigger(trigger_config):
    return _parse_trigger_or_response(trigger_config, Triggers)

def _parse_response(response_config):
    return _parse_trigger_or_response(response_config, Responses)

def _parse_triggers_or_responses(config, mapping_cls):
    return {element['name']: _parse_trigger_or_response(element, mapping_cls) for element in config}


def read_and_parse_rules(file_path):
    yaml = YAML()
    with open(file_path, 'r', encoding='utf-8') as stream:
        config = yaml.load(stream)

    global_triggers = _parse_triggers_or_responses(config['triggers'], Triggers)
    global_responses = _parse_triggers_or_responses(config['responses'], Triggers)
    rule_handlers = []

    for rule in config['rules']:
        if isinstance(rule['trigger'], str):
            trigger = global_triggers[rule['trigger']]
        else:
            trigger = _parse_trigger(rule['trigger'])

        if isinstance(rule['response'], str):
            response = global_responses[rule['response']]
        else:
            response = _parse_response(rule['response'])

        probability = rule['probability'] if 'probability' in rule else 1

        rule_handlers.append(Handler(trigger, response, probability=probability))

    return rule_handlers
