class Representable:

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def __str__(self):
        try:
            return self.__name
        except AttributeError:
            return f'inline {self.__class__.__name__}'
