import pytest
from pandas import DataFrame
from pydatamocker.api.schema import Schema
from pydatamocker.api.table import Table
from tests.util import assert_, eq, mismatch, order


def test_newTable():
    sch = Schema()
    sch.newTable('Table1', 10)
    assert_(sch.tables['Table1'], bool, lambda _: 'Table reference is not stored')
    assert_(sch.tables['Table1']._size, eq(10), mismatch(10))


def test_add():
    sch = Schema()
    sch.add(Table('Table1', 10))
    assert_(sch.tables['Table1'], bool, lambda _: 'Table reference is not stored')
    assert_(sch.tables['Table1']._size, eq(10), mismatch(10))


def test_delete():
    sch = Schema()
    sch.add(Table('Table1', 10))
    sch.delete('Table1')
    assert_(sch.tables.get('Table1'), lambda x: not x, lambda x: f'Reference to table {x} was removed')


def test_sample():
    sch = Schema()
    table1 = sch.add(Table('Table1', 10))
    table2 = sch.add(Table('Table2', 10))
    table1.field('Field1', {
        'const': 100
    })
    table1.field('Field2', {
        'const': 3232
    })
    table1.field('Field3', {
        'ref': (table1._name, 'Field1'),
    })

    table2.field('Field1', {
        'ref': (table1._name, 'Field2')
    })
    table2.field('Field2', {
        'ref': (table2._name, 'Field1')
    })
    sch.sample()

    df1: DataFrame = table1.getData()  # type: ignore
    t1_order = ['Field1', 'Field2', 'Field3']
    assert_(df1, lambda x: x is not None, lambda _: 'Data was not formed for Table1')
    assert_(df1.columns, order(t1_order), mismatch(t1_order))

    df2: DataFrame = table2.getData() # type: ignore
    t2_order = ['Field1', 'Field2']
    assert_(df2, lambda x: x is not None, lambda _: 'Data was notformed for Table2')
    assert_(df2.columns, order(t2_order), mismatch(t2_order))
