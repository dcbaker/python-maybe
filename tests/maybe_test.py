# Copyright Ǒ 2019 Dylan Baker
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import pytest

from maybe.maybe import Maybe, EMPTY


class TestMaybe:

    class TestProxy:

        def test_call(self):
            def foo() -> bool:
                return True

            v = Maybe(foo)
            assert v()

        def test_getitem(self):
            e = [1, 2, 3]
            v = Maybe(e)
            assert v[1] == 2

        def test_eq(self):
            e = {'a': 1, 'b': 2}
            v = Maybe(e)
            assert e == v

        def test_ne(self):
            e = {'a': 1, 'b': 2}
            v = Maybe(e)
            x = e.copy()
            x['a'] = 3
            assert e != x

        def test_gt(self):
            e = Maybe(1)
            assert 2 > e
            assert not 1 > e

        def test_lt(self):
            e = Maybe(4)
            assert 2 < e
            assert not 6 < e

        def test_le(self):
            e = Maybe(4)
            assert 2 <= e
            assert 4 <= e
            assert not 6 <= e

        def test_ge(self):
            e = Maybe(4)
            assert not 2 >= e
            assert 4 >= e
            assert 6 >= e

        def test_compare_maybe(self):
            # Compare maybes to each other
            e = Maybe(3)
            e2 = Maybe(5)
            assert e < e2
            assert e2 > e
            assert e != e2

        def test_str(self):
            e = Maybe(1)
            assert str(e) == '1'

        def test_bytes(self):
            e = Maybe(1)
            assert bytes(e) == bytes(1)

        def test_int(self):
            e = Maybe('3')
            assert int(e) == 3

        def test_float(self):
            e = Maybe(1)
            assert float(e) == 1.0

        def test_repr(self):
            e = Maybe(1)
            assert repr(e) == 'Maybe(1)'

        def test_hash(self):
            e = Maybe(1)
            e2 = Maybe(2)
            b = {e}
            b.add(e2)
            assert b == {e, e2}

        def test_unshable(self):
            e = Maybe([])
            with pytest.raises(TypeError):
                b = {e}

        class TestAttributes:

            class Foo:
                def __init__(self, a):
                    self.attr = a

            def test_get_attribute(self):
                b = self.Foo(None)
                a = self.Foo(b)

                m = Maybe(a)
                assert m.attr == b
                assert m['attr'] == b

            def test_chained_exists(self):
                c = self.Foo(None)
                b = self.Foo(c)
                a = self.Foo(b)
                m = Maybe(a)
                assert isinstance(m.attr.attr, Maybe)
                assert m.attr.attr == c

            def test_chained_not_exists(self):
                a = self.Foo(None)
                m = Maybe(a)
                assert m.attr.attr.get_maybe() is EMPTY

        class TestAttributeOrIndex:

            class _Tester:

                def __init__(self):
                    self.map = {}

                def __getitem__(self, name: str):
                    return self.map[name]

            def test_attribute_index_order(self):
                t = self._Tester()
                t.map['foo'] = 1
                assert t['foo'] == 1
                t.foo = 2
                assert t.foo == 2
                assert t.map['foo'] == 1


    class TestGetMaybe:

        def test_something(self):
            value = Maybe('1')
            assert value.get_maybe() == '1'

        def test_nothing(self):
            value = Maybe(EMPTY)
            assert value.get_maybe() is EMPTY

        def test_none(self):
            value = Maybe(None)
            assert value.get_maybe() is None


    class TestOtherwise:

        def test_nothing(self):
            value = Maybe(EMPTY)
            assert value.otherwise() is None

        def test_something(self):
            value = Maybe(1)
            assert value.otherwise() == 1

        def test_none(self):
            value = Maybe(None)
            assert value.otherwise(1) is None

        class Foo:
            def __init__(self, a):
                self.attr = a

        def test_chained_exists(self):
            c = self.Foo(None)
            b = self.Foo(c)
            a = self.Foo(b)
            m = Maybe(a)
            assert isinstance(m.attr.attr, Maybe)
            assert m.attr.attr.otherwise(None) == c


    class TestIsMethods:

        def test_something(self):
            value = Maybe('1')
            assert value.is_something()

        def test_nothing(self):
            value = Maybe(EMPTY)
            assert not value.is_something()

        def test_none(self):
            value = Maybe(None)
            assert value.is_something()
