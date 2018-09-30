import mock
import pytest

from sql import DataType, main, parse_query, Relation, SQL


def test_sql_instantiation():
    sql_object = SQL()
    assert sql_object.relations == {}


def test_sql_create_table():
    sql_object = SQL()
    assert len(sql_object.relations) == 0
    sql_object.create_table('test-relation')
    assert len(sql_object.relations) == 1

    relation_object = sql_object.relations.get('test-relation')
    assert isinstance(relation_object, Relation)


def test_sql_create_table_attributes():
    sql_object = SQL()

    attributes = {
        'title': '',
        'year': '',
        'length': 0,
        'genre': ''
    }

    assert len(sql_object.relations) == 0
    sql_object.create_table('Movies', attributes)
    assert len(sql_object.relations) == 1

    relation_object = sql_object.relations.get('Movies')
    assert isinstance(relation_object, Relation)
    assert relation_object.attributes == attributes


def test_sql_drop_table():
    sql_object = SQL()
    assert len(sql_object.relations) == 0
    does_exist_and_removed = sql_object.drop_table('Non-existing Relation')
    assert not does_exist_and_removed

    sql_object.create_table('Movies')
    assert len(sql_object.relations) == 1
    does_exist_and_removed = sql_object.drop_table('Movies')
    assert does_exist_and_removed


def test_relation_without_attributes():
    relation_object = Relation(name='Movies')
    assert relation_object.name == 'Movies'
    assert relation_object.attributes == []
    assert relation_object.schema == 'Movies()'
    assert relation_object.schema_domain == 'Movies()'


def test_relation_with_attributes():
    attributes = [
            {
                'name': 'title',
                'type': DataType.CHAR
            },
            {
                'name': 'year',
                'type': DataType.INTEGER
            },
            {
                'name': 'length',
                'type': DataType.INTEGER
            },
            {
                'name': 'genre',
                'type': DataType.CHAR
            }
        ]

    relation_object = Relation(name='Movies', attributes=attributes)
    assert relation_object.name == 'Movies'
    assert relation_object.attributes == attributes

    representation = relation_object.__repr__()
    assert representation == 'Movies(title, year, length, genre)'

    assert relation_object.schema == relation_object.__repr__()
    assert relation_object.schema_domain == 'Movies(title:string, year:integer, length:integer, genre:string)'


@mock.patch('builtins.input')
def test_main_quit(mock_input):
    mock_input.return_value = 'quit'
    response = main()
    assert response == 'exit SQL'


@pytest.mark.parametrize(
    'query, operation, relation_name', [
        ('CREATE TABLE Movies ();', 'CREATE', 'Movies'),
        ('SHOW TABLES;', 'SHOW TABLES', None),
        ('DROP TABLE Movies;', 'DROP', 'Movies')
    ]
)
def test_parse_query(query, operation, relation_name):
    actual_operation, actual_relation_name = parse_query(query)
    assert actual_operation == operation
    assert actual_relation_name == relation_name


def test_parse_query_unsupported_operation():
    query = 'UNSUPPORTED-OP TABLE Movies ();'
    operation, relation_name = parse_query(query)
    assert operation is None
    assert relation_name is None
