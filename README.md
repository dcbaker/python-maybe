# Python-maybe

python-maybe is a python3 only maybe implementation.


## What is it?

It implements as close to a maybe pattern as can probably be done in python,
it is similar to the null object pattern, except that it treats all values
except one special value (`EMPTY`) as valid values. The idea is to simplify
cases where a value is optional, making code easier to understand but without
sacrificing correctness.

Given an arbitrarily deep attribute list one normally ends up with really
ugly None checks:

```python
class A:

    def __init__(self, v: typing.Optional[typing.Union[A, B]] = None):
        self.v = v


class B:

    def __init__(self, a: str):
        self.a = a


def fun() -> str:
    f = A(A(A(B('foo'))))

    if f.v and f.v.v and f.v.v.v
        return f.v.v.v.a
    return 'Unknown value'
```

With the maybe pattern we can simplify that:

```python
def fun() -> str:
    f = Maybe(A(A(A(B('foo')))))

    return f.v.v.v.a.otherwise('Unknown value')
```


## What about pymaybe?

I was inspired by pymaybe, and I've used it a fair bit. There are a couple of
things. One is I don't care about python 2, at all. The second is that it
uses None as it's sentinel value, which means that cases where you actually
want None cannot be distinguished from cases where pymaybe has used None to
represent a lack of value.

Cases like:

```python
from pymaybe import maybe

maybe([None])[0].is_none() == True
```

python-maybe doesn't have this problem, because it uses a unique sentinel value:

```python
from maybe.maybe import Maybe

Maybe([None])[0].is_something() == True
```

Be aware that python-maybe doesn't have an equivalent to is_none, is only has is_something()
