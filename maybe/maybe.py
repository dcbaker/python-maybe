# Copyright © 2019 Dylan Baker
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing

class _Empty:

    """Singleton class that represents a lack of value.

    We don't use None here because None is python value, and could be passed
    intentionally. These are inherintly unorderable, and implement only
    equality to themselves, and a __repr__ method.
    """

    __slots__ = ()

    def __eq__(self, other) -> typing.Union[bool, 'NotImplemented']:
        return isinstance(other, type(self))

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __ge__(self, other):
        return False

    def __gt__(self, other):
        return False

    def __repr__(self):
        return '_Empty()'

    def __hash__(self):
        return hash('PYTHON MAYBE EMPTY')


EMPTY = _Empty()


class Maybe:

    """A container that may have a value in it.

    Maybe is a container that may or may not have a value. It uses a special
    sentinal value to track whether there is a value or not in the maybe.
    This makes it safe to use with falsy values like False and None.
    """

    __slots__= ('__value')

    def __init__(self, value) -> None:
        self.__value = value

    def __call__(self, *args, **kwargs) -> None:
        return self.__value(*args, **kwargs)

    def __getitem__(self, item):
        try:
            return Maybe(self.__value[item])
        except (IndexError, KeyError):
            return Maybe(getattr(self, item, EMPTY))

    def __getattr__(self, name: str):
        try:
            return Maybe(self.__getattribute__(name))
        except AttributeError:
            return Maybe(getattr(self.__value, name, EMPTY))

    def get_maybe(self):
        """Get the stored value out of the Maybe instance.

        If there is no value then EMPTY will be returned.
        """
        return self.__value

    def otherwise(self, fallback=None):
        """Get the value or fallback value.

        This provides either the internal value if that value is not EMPTY,
        if it is EMPTY then the fallback value will be returned.
        """
        if self.__value is EMPTY:
            return fallback
        return self.__value

    def is_something(self) -> bool:
        """Is the value not EMPTY?

        Returns True if the value is not EMPTY, otherwise False.
        """
        return self.__value is not EMPTY

    def __eq__(self, other):
        if isinstance(other, Maybe):
            return self.get_maybe() == other.get_maybe()
        return self.get_maybe() == other

    def __lt__(self, other):
        if isinstance(other, Maybe):
            return self.get_maybe() < other.get_maybe()
        return self.get_maybe() < other

    def __le__(self, other):
        if isinstance(other, Maybe):
            return self.get_maybe() <= other.get_maybe()
        return self.get_maybe() <= other

    def __ge__(self, other):
        if isinstance(other, Maybe):
            return self.get_maybe() >= other.get_maybe()
        return self.get_maybe() >= other

    def __gt__(self, other):
        if isinstance(other, Maybe):
            return self.get_maybe() > other.get_maybe()
        return self.get_maybe() > other

    def __str__(self):
        return str(self.__value)

    def __bytes__(self):
        return bytes(self.__value)

    def __int__(self):
        return int(self.__value)

    def __float__(self):
        return float(self.__value)

    def __repr__(self):
        return f'Maybe({repr(self.__value)})'

    def __format__(self, format_spec):
        return self.__value.__format__(format_spec)

    def __hash__(self):
        # This must return the hash of self.__value because it has an __eq__
        # method
        return hash(self.__value)
