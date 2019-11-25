# Copyright © 2019 Dylan Baker
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import enum
import typing

class _Empty:

    """Singleton class that represents a lack of value.

    We don't use None here because None is python value, and could be passed
    intentionally. These are inherintly unorderable, and implement only
    equality to themselves, and a __repr__ method.
    """

    __slots__: typing.List[str] = []

    def __eq__(self, other) -> typing.Union[bool, 'NotImplemented']:
        return isinstance(other, type(self))

    def __repr__(self):
        return 'EMPTY'

    def __hash__(self):
        return hash('PYTHON MAYBE EMPTY')


EMPTY = _Empty()


def _nothing() -> 'Maybe':
    """internal helper for an empty Maybe()."""
    return Maybe(EMPTY)


@enum.unique
class AsMaybe(enum.Enum):

    """Enum to provide maybe() wrappers for dunder methods accessed by type
    casts.
    """

    STR = enum.auto()
    BYTES = enum.auto()
    INT = enum.auto()
    FLOAT = enum.auto()
    BOOL = enum.auto()
    HASH = enum.auto()


class Maybe:

    """A container that may have a value in it.

    Maybe is a container that may or may not have a value. It uses a special
    sentinal value to track whether there is a value or not in the maybe.
    This makes it safe to use with falsy values like False and None.

    This class is meant to be transparent as much as possible, but also
    maximize chaining. To that end calls that are meant to return a specfic
    type will always do so if possible, or error.

    >>> bytes(Maybe(None))
    Traceback (most recent call last):
        ...
    TypeError: cannot convert 'NoneType' object to bytes

    Duner methods that are not expected to return a specific type will return
    a value wrapped in another `Maybe`, for example:

    >>> Maybe(int)("0")
    Maybe(0)
    >>> Maybe(int)("foo")
    Maybe(EMPTY)

    An `as_maybe` function is provided to allow accessing type specific
    dunder methods in a Maybe() safe way.

    >>> Maybe(None).as_maybe(AsMaybe.INT)
    Maybe(EMPTY)
    >>> Maybe("0").as_maybe(AsMaybe.INT)
    Maybe(0)

    Additionally there are methods for testing whether a `Maybe` contains a value or not:
    >>> Maybe(EMPTY).is_nothing()
    True
    >>> Maybe(EMPTY).is_something()
    False
    >>> Maybe(None).is_nothing()
    False
    >>> Maybe(None).is_something()
    True
    """

    __slots__ = ['__value']

    def __init__(self, value) -> None:
        self.__value = value

    def __call__(self, *args, **kwargs):
        """Try to call the wrapped value with the given args.

        It returns another `Maybe` with the value of the call, or if the call
        fails for any reason it will contain `Empty`. Be aware that this can
        hide failures caused by passing invalid values, but allows better chaining.

        >>> Maybe(int)("foo").otherwise(0)
        0
        """
        try:
            return Maybe(self.__value(*args, **kwargs))
        except Exception:
            return _nothing()

    def __getitem__(self, item):
        try:
            return Maybe(self.__value[item])
        except (IndexError, KeyError, TypeError):
            return Maybe(getattr(self, item, EMPTY))

    def __getattr__(self, name: str):
        try:
            return Maybe(self.__getattribute__(name))
        except AttributeError:
            return Maybe(getattr(self.__value, name, EMPTY))

    def just(self):
        """Get the stored value out of the Maybe instance.

        If there is no value then EMPTY will be returned.

        >>> Maybe(1).just()
        1
        >>> Maybe(EMPTY).just()
        EMPTY
        """
        return self.__value

    def otherwise(self, fallback=None):
        """Get the value or fallback value.

        This provides either the internal value if that value is not EMPTY,
        if it is EMPTY then the fallback value will be returned.

        >>> Maybe(1).otherwise(0)
        1
        >>> Maybe(EMPTY).otherwise(0)
        0
        """
        if self.is_nothing():
            return fallback
        return self.__value

    def is_something(self) -> bool:
        """Is the value not EMPTY?

        Returns True if the value is not EMPTY, otherwise False.

        >>> Maybe(False).is_something()
        True
        >>> Maybe(EMPTY).is_something()
        False
        """
        return self.__value is not EMPTY

    def is_nothing(self) -> bool:
        """Is the value not EMPTY?

        Returns True if the value is not EMPTY, otherwise False.

        >>> Maybe(False).is_nothing()
        False
        >>> Maybe(EMPTY).is_nothing()
        True
        """
        return self.__value is EMPTY

    def as_maybe(self, dunder: AsMaybe) -> 'Maybe':
        """Get dunders wrapped in Maybes.

        Python-maybe does not wrap most dunders in maybes, becuase those are
        generally called by type changing functions, `__str__` is called by
        `str` for example. If python-maybe wrapped the result of `str` in a
        `Maybe` it would break the assumption of the caller that they're
        getting a `str` instance. Since is however useful to get
        type-changing dunders wrapped in `Maybe`s python-maybe provides the
        `as_maybe` method. This takes a single argument from the `AsMaybe`
        enum for the dunder and returns a `Maybe` with the output or a
        `Maybe` containing `EMPTY`.

        >>> Maybe('1').as_maybe(AsMaybe.INT)
        Maybe(1)
        >>> Maybe(None).as_maybe(AsMaybe.BYTES)
        Maybe(EMPTY)
        >>> Maybe(EMPTY).as_maybe(AsMaybe.STR)
        Maybe(EMPTY)
        """
        if self.is_nothing():
            return _nothing()

        if dunder is AsMaybe.STR:
            f = str  # type: typing.Callable[[typing.Any], typing.Any]
        elif dunder is AsMaybe.BYTES:
            f = bytes
        elif dunder is AsMaybe.INT:
            f = int
        elif dunder is AsMaybe.FLOAT:
            f = float
        elif dunder is AsMaybe.BOOL:
            f = bool
        elif dunder is AsMaybe.HASH:
            f = hash
        else:
            raise RuntimeError('Unsupported dunder {!r}'.format(dunder))

        try:
            return Maybe(f(self.__value))
        except TypeError:
            return _nothing()

    def __eq__(self, other):
        if isinstance(other, Maybe):
            return self.just() == other.just()
        return self.just() == other

    def __lt__(self, other):
        if isinstance(other, Maybe):
            return self.just() < other.just()
        return self.just() < other

    def __le__(self, other):
        if isinstance(other, Maybe):
            return self.just() <= other.just()
        return self.just() <= other

    def __ge__(self, other):
        if isinstance(other, Maybe):
            return self.just() >= other.just()
        return self.just() >= other

    def __gt__(self, other):
        if isinstance(other, Maybe):
            return self.just() > other.just()
        return self.just() > other

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

    def __bool__(self):
        return bool(self.__value)

    def __hash__(self):
        # This must return the hash of self.__value because it has an __eq__
        # method
        return hash(self.__value)
