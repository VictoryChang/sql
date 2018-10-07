import pytest

from sql.table import parse_query

@pytest.mark.parametrize(
    'query, projection, table_name', [
        ('SELECT column1, column2 FROM table_name;', 'column1, column2', 'table_name'),
        ('SELECT * FROM table_name;', '*', 'table_name'),
        ('SELECT CustomerName, City FROM Customers;', 'CustomerName, City', 'Customers'),
        ('SELECT * FROM Customers;', '*', 'Customers'),
        ('SELECT Country FROM Customers;', 'Country', 'Customers')
    ])
def test_select(query, projection, table_name):
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == projection
    assert result['table_name'] == table_name
    assert result['condition'] is None
    assert result['order_by'] is None
    assert result['order_by_sort'] is None


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
    assert result['order_by_sort'] is None


def test_alternatives():
    query = 'SELECT COUNT(DISTINCT Country) FROM Customers;'
    '''
    SELECT * FROM Customers
    ORDER BY Country ASC, CustomerName DESC;
    '''

def test_where_clause():
    query = 'SELECT column1, column2 FROM table_name WHERE condition;'
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == 'column1, column2'
    assert result['table_name'] == 'table_name'
    assert result['condition'] == 'condition'
    assert result['order_by'] is None
    assert result['order_by_sort'] is None

    query = 'SELECT * FROM Customers WHERE Country="Mexico";'
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == '*'
    assert result['table_name'] == 'Customers'
    assert result['condition'] == 'Country="Mexico"'
    assert result['order_by'] is None
    assert result['order_by_sort'] is None

    query = 'SELECT * FROM Customers WHERE CustomerID=1;'
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == '*'
    assert result['table_name'] == 'Customers'
    assert result['condition'] == 'CustomerID=1'
    assert result['order_by'] is None
    assert result['order_by_sort'] is None


def test_where_clause_and_or_not():
    query = 'SELECT * FROM Customers WHERE Country="Germany" AND City="Berlin";'
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == '*'
    assert result['table_name'] == 'Customers'
    assert result['condition'] == 'Country="Germany" AND City="Berlin"'
    assert result['order_by'] is None
    assert result['order_by_sort'] is None

    query = 'SELECT * FROM Customers WHERE City="Berlin" OR City="München";'
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == '*'
    assert result['table_name'] == 'Customers'
    assert result['condition'] == 'City="Berlin" OR City="München"'
    assert result['order_by'] is None
    assert result['order_by_sort'] is None

    query = 'SELECT * FROM Customers WHERE NOT Country="Germany";'
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == '*'
    assert result['table_name'] == 'Customers'
    assert result['condition'] == 'NOT Country="Germany"'
    assert result['order_by'] is None
    assert result['order_by_sort'] is None

    query = 'SELECT * FROM Customers WHERE Country="Germany" AND (City="Berlin" OR City="München");'
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == '*'
    assert result['table_name'] == 'Customers'
    assert result['condition'] == 'Country="Germany" AND (City="Berlin" OR City="München")'
    assert result['order_by'] is None
    assert result['order_by_sort'] is None

    query = 'SELECT * FROM Customers WHERE NOT Country="Germany" AND NOT Country="USA";'
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == '*'
    assert result['table_name'] == 'Customers'
    assert result['condition'] == 'NOT Country="Germany" AND NOT Country="USA"'
    assert result['order_by'] is None
    assert result['order_by_sort'] is None

def test_order_by():
    query = 'SELECT * FROM Customers ORDER BY Country;'
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == '*'
    assert result['table_name'] == 'Customers'
    assert result['condition'] is None
    assert result['order_by'] == 'Country'

    query = 'SELECT * FROM Customers ORDER BY Country DESC;'
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == '*'
    assert result['table_name'] == 'Customers'
    assert result['condition'] is None
    assert result['order_by'] == 'Country'
    assert result['order_by_sort'] == 'DESC'

    query = 'SELECT * FROM Customers ORDER BY Country ASC;'
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == '*'
    assert result['table_name'] == 'Customers'
    assert result['condition'] is None
    assert result['order_by'] == 'Country'
    assert result['order_by_sort'] == 'ASC'

    query = 'SELECT * FROM Customers ORDER BY Country, CustomerName;'
    result = parse_query(query)
    assert not result['is_distinct']
    assert result['projection'] == '*'
    assert result['table_name'] == 'Customers'
    assert result['condition'] is None
    assert result['order_by'] == 'Country, CustomerName'
    assert result['order_by_sort'] is None

