from pydatamocker.api.table import Table
from tests.util import assert_, eq, mismatch


table = Table('Test table', 1500)


def test_size():
    ssize = 1233
    table = Table('Test table', ssize)
    assert_(table._size, eq(ssize), mismatch(ssize))
    test_data = [
        ('TestField1', { 'const': 10 }),
        ('TestField2', { 'const': 20 })
    ]
    for name, val in test_data:
        table.field(name, val)
    assert_(len(table.fields), eq(2), mismatch(2))
    assert_(set(table.fields.keys()),
        eq({ name for name, _ in test_data }),
        mismatch({ name for name, _ in test_data })
    )


def test_invalid_size():
    for size in (0, -3):
        try:
            _ = Table('Test table', size)
        except ValueError:
            continue
        assert False, 'Size 0 did not raise an error'
