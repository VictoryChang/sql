import mock
from sql import main, parse_query, Relation, SQL


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


def test_relation_instantiation():
    relation_object = Relation(name='test-relation')
    assert relation_object.name == 'test-relation'


def test_relation_without_attributes():
    relation_object = Relation(name='Movies')
    assert relation_object.name == 'Movies'
    assert relation_object.attributes is None


def test_relation_with_attributes():
    attributes = {
        'title': '',
        'year': '',
        'length': 0,
        'genre': ''
    }
    relation_object = Relation(name='Movies', attributes=attributes)
    assert relation_object.name == 'Movies'
    assert relation_object.attributes == attributes


@mock.patch('builtins.input')
def test_main_quit(mock_input):
    mock_input.return_value = 'quit'
    response = main()
    assert response == 'exit SQL'


def test_parse_query_create_table():
    query = 'CREATE TABLE Movies ();'
    operation, relation_name = parse_query(query)
    assert operation == 'CREATE'
    assert relation_name == 'Movies'


def test_parse_query_unsupported_operation():
    query = 'UNSUPPORTED-OP TABLE Movies ();'
    operation, relation_name = parse_query(query)
    assert operation is None
    assert relation_name is None


def test_parse_query_show_table():
    query = 'SHOW TABLES;'
    operation, relation_name = parse_query(query)
    assert operation == 'SHOW TABLES'
    assert relation_name is None