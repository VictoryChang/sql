import re


class DataType(object):
    CHAR = 'string'
    BOOLEAN = 'boolean'
    INTEGER = 'integer'
    FLOAT = 'float'
    DECIMAL = 'decimal'
    DATE = 'date'
    TIME = 'time'


class BoolType(object):
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    UNKNOWN = 'UNKNOWN'


class SQL(object):
    """
    A class which simulates a single SQL database
    """
    def __init__(self):
        self.relations = {}

    def create_table(self, name, attributes=None):
        """
        Construct a relation with the corresponding attributes

        :param Text name: Relation name
        :param (Dict(Text, Any)) attributes: Attributes for the relation
        :return: True/False whether a relation was created
        """
        if name in self.relations:
            print('Relation with name {!r} already exists.'.format(name))
            return False

        self.relations[name] = Relation(name, attributes)
        print('Created Relation with name: {!r}'.format(name))
        return True

    def drop_table(self, name):
        """
        Drop a relation from the database

        :param Text name: Relation name
        :return: True/False whether a relation existed and was dropped
        """
        if name in self.relations:
            self.relations.pop(name)
            print('Relation with name {!r} was dropped.'.format(name))
            return True

        print('Relation {!r} cannot be dropped it does not exist.'.format(name))
        return False

    def show_tables(self):
        """
        List all of the available tables generated during this execution
        """
        print('Tables:')
        for index, table_name in enumerate(sorted(self.relations.keys())):
            print('{}: {}'.format(index, table_name))


class Relation(object):
    """
    A class which represents a single SQL relation (table)
    """
    def __init__(self, name, attributes=None):
        self.name = name
        self.attributes = attributes or []

    def __repr__(self):
        return self.schema

    @property
    def schema(self):
        attributes = ', '.join([field['name'] for field in self.attributes])
        return '{}({})'.format(self.name, attributes)

    @property
    def schema_domain(self):
        attributes = ', '.join(['{}:{}'.format(field['name'], field['type']) for field in self.attributes])
        return '{}({})'.format(self.name, attributes)


def parse_query(query):
    """
    Parse a query string for SQL-like commands

    :param Text query: User input command
    :return: operation and corresponding relation name where applicable
    """
    operation = None
    relation_name = None

    create_pattern = '^CREATE TABLE ([a-zA-Z0-9]+) \(\);$'
    match = re.search(create_pattern, query)
    if match:
        operation = 'CREATE'
        relation_name = match.group(1)

    drop_pattern = '^DROP TABLE ([a-zA-Z0-9]+);$'
    match = re.search(drop_pattern, query)
    if match:
        operation = 'DROP'
        relation_name = match.group(1)

    if query == 'SHOW TABLES;':
        operation = 'SHOW TABLES'

    return operation, relation_name


def main():
    print('SQL')
    sql_object = SQL()
    while True:
        query = input('> ')
        print('you said: {}'.format(query))
        if query == 'quit':
            return 'exit SQL'

        operation, relation_name = parse_query(query)
        if operation == 'CREATE':
            sql_object.create_table(name=relation_name)

        if operation == 'DROP':
            sql_object.drop_table(name=relation_name)

        if operation == 'SHOW TABLES':
            sql_object.show_tables()


if __name__ == '__main__':
    main()


'''
Regression Tests to Add
1. DROP Movies -> None, QUIT
DROP TABLE Movies;
quit

2. CREATE Movies, Drop Movies, QUIT
CREATE TABLE Movies ();
SHOW TABLES;
DROP TABLE Movies;
quit

3. CREATE Movies, Drop Stars -> None ,QUIT
CREATE TABLE Movies ();
SHOW TABLES;
DROP TABLE Stars;
quit

4. SHOW TABLES -> Empty, QUIT
SHOW TABLES;
quit
'''
