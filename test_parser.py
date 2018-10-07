from parser import MySQL, parse_query


def test_parse_query():
    query_string = 'SHOW DATABASES;'
    op, level, name, attributes = parse_query(query_string)
    assert op == 'show'
    assert level == 'database'
    assert name is None

    query_string = 'CREATE DATABASE Movies;'
    op, level, name, attributes = parse_query(query_string)
    assert op == 'create'
    assert level == 'database'
    assert name == 'Movies'

    query_string = 'CREATE DATABASE Stars;'
    op, level, name, attributes = parse_query(query_string)
    assert op == 'create'
    assert level == 'database'
    assert name == 'Stars'

    query_string = 'USE Stars;'
    op, level, name, attributes = parse_query(query_string)
    assert op == 'use'
    assert level == 'database'
    assert name == 'Stars'

    query_string = 'DROP DATABASE Movies;'
    op, level, name, attributes = parse_query(query_string)
    assert op == 'drop'
    assert level == 'database'
    assert name == 'Movies'


def test_mysql_create_database():
    sql_object = MySQL()
    assert sql_object.databases == []

    response = sql_object.create_database('Movies')
    assert response == 'Query OK, 1 row affected (0.xx sec)'
    assert sql_object.databases == ['Movies']

    response = sql_object.create_database('Movies')
    assert response == "ERROR 1007 (HY000): Can't create database 'Movies'; database exists"
    assert sql_object.databases == ['Movies']


def test_mysql_drop_database():
    sql_object = MySQL()
    sql_object.databases = ['Movies']

    response = sql_object.drop_database('Movies')
    assert response == 'Query OK, 0 row affected (0.xx sec)'

    response = sql_object.drop_database('Movies')
    assert response == "ERROR 1008 (HY000): Can't drop database 'Movies'; database doesn't exists"


def test_create_table():
    query_string = 'CREATE TABLE table_name(column1 datatype,column2 datatype,column3 datatype);'
    op, level, name, attributes = parse_query(query_string)
    assert op == 'create'
    assert level == 'table'
    assert name == 'table_name'
    assert attributes == [
        {'name': 'column1', 'type': 'datatype'},
        {'name': 'column2', 'type': 'datatype'},
        {'name': 'column3', 'type': 'datatype'}]

    query_string = 'CREATE TABLE Persons(PersonID int,LastName varchar(255),FirstName varchar(255),Address varchar(255),City varchar(255));'
    op, level, name, attributes = parse_query(query_string)
    assert op == 'create'
    assert level == 'table'
    assert name == 'Persons'
    assert attributes == [
        {'name': 'PersonID', 'type': 'int'},
        {'name': 'LastName', 'type': 'varchar(255)'},
        {'name': 'FirstName', 'type': 'varchar(255)'},
        {'name': 'Address', 'type': 'varchar(255)'},
        {'name': 'City', 'type': 'varchar(255)'}]

    query_string = 'CREATE TABLE Tasks(task_id INTEGER);'
    op, level, name, attributes = parse_query(query_string)
    assert op == 'create'
    assert level == 'table'
    assert name == 'Tasks'
    assert attributes == [
        {'name': 'task_id', 'type': 'INTEGER'}]

    query_string = 'CREATE TABLE Tasks(task_id INTEGER,start_date DATE);'
    op, level, name, attributes = parse_query(query_string)
    assert op == 'create'
    assert level == 'table'
    assert level == 'table'
    assert name == 'Tasks'
    assert attributes == [
        {'name': 'task_id', 'type': 'INTEGER'},
        {'name': 'start_date', 'type': 'DATE'}]


def test_drop_table():
    query_string = 'DROP TABLE table_name;'
    op, level, name, attributes = parse_query(query_string)
    assert op == 'drop'
    assert level == 'table'
    assert name == 'table_name'
    assert attributes is None

    query_string = 'DROP TABLE Shippers;'
    op, level, name, attributes = parse_query(query_string)
    assert op == 'drop'
    assert level == 'table'
    assert name == 'Shippers'
    assert attributes is None



