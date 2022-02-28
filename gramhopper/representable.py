class Representable:
    """
    A "representable" interface for triggers and responses.
    The representation is the name of the trigger/response if given,
    or "inline <Type of trigger/response>" otherwise.
    """
    def __init__(self):
        self.__name = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def __str__(self):
        if self.__name:
            return self.__name

        return f'inline {self.__class__.__name__}'
