import re

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

    def show_tables(self):
        """
        List all of the available tables generated during this execution
        """
        print('Tables:')
        for index, table_name in enumerate(sorted(self.relations.keys())):
            print('{}: {}'.format(index, table_name))


class Relation(object):
    def __init__(self, name, attributes=None):
        self.name = name
        self.attributes = attributes


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

    show_pattern = '^SHOW TABLES;$'
    match = re.search(show_pattern, query)
    if match:
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

        if operation == 'SHOW TABLES':
            sql_object.show_tables()


    return 'completed'


if __name__ == '__main__':
    main()
