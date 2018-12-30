import yaml
#import re
from pprint import pprint
from ruamel.yaml import YAML
from gramhopper.handlers.handler import Handler
from ..responses import Responses
from ..triggers import Triggers


#FUNCTION_REGEXP = '([\w\._]+)\((.*)\)'


triggers_mapping = {
    'text.has_exact_word': Triggers.text.has_exact_word,
    'text.has_substring': Triggers.text.has_substring,
}

response_mapping = {
    'preset.reply': Responses.preset.reply,
    'preset.message': Responses.preset.message,
}

def _parse_trigger_or_response(config, mapping):
    config_copy = dict(config)
    if 'name' in config_copy:
        config_copy.pop('name')

    trigger_or_response_class = mapping[config_copy['type']]
    config_copy.pop('type')

    return trigger_or_response_class(**config_copy)


def _parse_trigger(trigger_config):
    return _parse_trigger_or_response(trigger_config, triggers_mapping)

def _parse_response(response_config):
    return _parse_trigger_or_response(response_config, response_mapping)


def read_and_parse_rules(file_path):
    yaml = YAML()
    with open(file_path, 'r', encoding='utf-8') as stream:
        config = yaml.load(stream)

    global_triggers = {trigger['name']: _parse_trigger(trigger) for trigger in config['triggers']}
    global_responses = {response['name']: _parse_response(response) for response in config['responses']}
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
