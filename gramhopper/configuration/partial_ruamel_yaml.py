"""
This file is a dirty hack to handle ruamel_yaml import problem
In certain distributions, the module name is ruamel_yaml, while in others it's ruamel.yaml.
As you can easily understand, that made us very sad :(
A fallback import wasn't enough to solve it since the same imports were done in 3 different files,
so we decided to create this file, which is a *very* partial accessor to ruamel_yaml.
"""

try:
    from ruamel_yaml import YAML
    from ruamel_yaml.comments import CommentedMap
except ImportError:
    from ruamel.yaml import YAML
    from ruamel.yaml.comments import CommentedMap


YAML = YAML
CommentedMap = CommentedMap #pylint: disable=invalid-name
