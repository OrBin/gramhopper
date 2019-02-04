from enum import Enum, EnumMeta


class DictEnumMeta(EnumMeta):
    def __getitem__(self, key):
        key_path = key.split('.')
        item = super().__getitem__(key_path.pop(0)).value

        if key_path:
            return item['.'.join(key_path)]

        return item


class DictEnum(Enum, metaclass=DictEnumMeta):
    pass
