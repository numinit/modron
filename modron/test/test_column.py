import pytest

from modron import column


def test_create():
    c1 = column.Column(42, 'answer')
    assert c1.idx == 42
    assert c1.name == 'answer'
    assert c1.expected_type == object
    assert c1.actual_types == {}

    c2 = column.Column(43, 'not the answer', int)
    assert c2.idx == 43
    assert c2.name == 'not the answer'
    assert c2.expected_type == int


def test_clone():
    c1 = column.Column(42, 'answer', int, {int: 99, object: 1})
    c2 = c1.clone()
    assert c1 == c2
    assert id(c1) != id(c2)


def test_add_type_counts():
    c1 = column.Column(42, 'answer', int)
    c1.add_type_counts(int, 1)
    assert c1.actual_types[int] == 1
    c2 = column.Column(43, 'not the answer', int)
    c2.add_type_counts(int, 42)
    assert c2.actual_types[int] == 42
    with pytest.raises(ValueError):
        c2.add_type_counts(int, 0)
    with pytest.raises(ValueError):
        c2.add_type_counts(int, -1)
