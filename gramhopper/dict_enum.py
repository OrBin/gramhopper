from enum import Enum, EnumMeta


class DictEnumMeta(EnumMeta):
    """Metaclass for DictEnum"""

    def __getitem__(cls, key):
        key_path = key.split('.')
        item = super().__getitem__(key_path.pop(0)).value

        if key_path:
            return item['.'.join(key_path)]

        return item


class DictEnum(Enum, metaclass=DictEnumMeta):
    """
    A subscriptable enum class: An enum where elements can be accessed using the subscription
    operator.
    While regular enum values can only be accessed like `EnumName.value_name`, subscriptable enum
    values can also be access like `EnumName['value_name']`.
    The subscription key can be used to concatenate subscriptions, for example: `EnumName['x.y']`
    is equivalent to `EnumName['x']['y']`, as well as to `EnumName.x.y`.
    """
