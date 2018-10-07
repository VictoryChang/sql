import pytest

from sql.table import parse_query

@pytest.mark.parametrize(
    'query, projection, table_name', [
        ('SELECT * FROM table_name;', '*', 'table_name'),
        ('SELECT * FROM Customers;', '*', 'Customers'),
        ('SELECT column1, column2 FROM table_name;', 'column1, column2', 'table_name'),
        ('SELECT Country FROM Customers;', 'Country', 'Customers'),
        ('SELECT CustomerName, City FROM Customers;', 'CustomerName, City', 'Customers'),
    ])
def test_select(query, projection, table_name):
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == projection
    assert result['table_name'] == table_name
    assert result['condition'] is None
    assert result['order_by'] is None
    assert result['order_by_sort'] == 'ASC'


@pytest.mark.parametrize(
    'query, projection, table_name', [
        ('SELECT DISTINCT column1, column2 FROM table_name;', 'column1, column2', 'table_name'),
        ('SELECT DISTINCT Country FROM Customers;', 'Country', 'Customers')
    ])
def test_select_distinct(query, projection, table_name):
    result = parse_query(query)
    assert result['is_distinct']
    assert result['projection'] == projection
    assert result['table_name'] == table_name
    assert result['condition'] is None
    assert result['order_by'] is None
    assert result['order_by_sort'] == 'ASC'


def test_alternatives():
    query = 'SELECT COUNT(DISTINCT Country) FROM Customers;'
    '''
    SELECT * FROM Customers
    ORDER BY Country ASC, CustomerName DESC;
    '''

@pytest.mark.parametrize(
    'query, projection, table_name, condition', [
        ('SELECT column1, column2 FROM table_name WHERE condition;', 'column1, column2', 'table_name', 'condition'),
        ('SELECT * FROM Customers WHERE Country="Mexico"', '*', 'Customers', 'Country="Mexico"'),
        ('SELECT * FROM Customers WHERE CustomerID=1;', '*', 'Customers', 'CustomerID=1')
    ])
def test_where_clause(query, projection, table_name, condition):
    query = 'SELECT column1, column2 FROM table_name WHERE condition;'
    result = parse_query(query)
    assert result['order_by'] is None
    assert result['order_by_sort'] == 'ASC'


@pytest.mark.parametrize(
    'query, projection, table_name, condition', [
        ('SELECT * FROM Customers WHERE Country="Germany" AND City="Berlin";', '*', 'Customers' ,'Country="Germany" AND City="Berlin"'),
        ('SELECT * FROM Customers WHERE City="Berlin" OR City="München";', '*', 'Customers', 'City="Berlin" OR City="München"'),
        ('SELECT * FROM Customers WHERE NOT Country="Germany";', '*', 'Customers', 'NOT Country="Germany"'),
        ('SELECT * FROM Customers WHERE Country="Germany" AND (City="Berlin" OR City="München");', '*', 'Customers', 'Country="Germany" AND (City="Berlin" OR City="München")'),
        ('SELECT * FROM Customers WHERE NOT Country="Germany" AND NOT Country="USA";', '*', 'Customers', 'NOT Country="Germany" AND NOT Country="USA"')
    ])
def test_where_clause_and_or_not(query, projection, table_name, condition):
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == projection
    assert result['table_name'] == table_name
    assert result['condition'] == condition
    assert result['order_by'] is None
    assert result['order_by_sort'] == 'ASC'


@pytest.mark.parametrize(
    'query, projection, table_name, order_by, order_by_sort', [
        ('SELECT * FROM Customers ORDER BY Country;', '*', 'Customers', 'Country', 'ASC'),
        ('SELECT * FROM Customers ORDER BY Country DESC;', '*', 'Customers', 'Country', 'DESC'),
        ('SELECT * FROM Customers ORDER BY Country ASC;', '*', 'Customers', 'Country', 'ASC'),
        ('SELECT * FROM Customers ORDER BY Country, CustomerName;', '*', 'Customers', 'Country, CustomerName', 'ASC')
    ])
def test_order_by(query, projection, table_name, order_by, order_by_sort):
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == projection
    assert result['table_name'] == table_name
    assert result['condition'] is None
    assert result['order_by'] == order_by
    assert result['order_by_sort'] == order_by_sort
