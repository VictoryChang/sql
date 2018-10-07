import re


class MySQL(object):
    def __init__(self):
        self.databases = []

    def create_database(self, name):
        if name in self.databases:
            return f'ERROR 1007 (HY000): Can\'t create database {name!r}; database exists'

        self.databases.append(name)
        return 'Query OK, 1 row affected (0.xx sec)'

    def drop_database(self, name):
        if name in self.databases:
            self.databases.remove(name)
            return 'Query OK, 0 row affected (0.xx sec)'  # 0 is number of tables deleted

        return f'ERROR 1008 (HY000): Can\'t drop database {name!r}; database doesn\'t exists'


def parse_query(query_string):
    op = None
    level = None
    name = None
    attributes = None

    if query_string == 'SHOW DATABASES;':
        op = 'show'
        level = 'database'

    else:
        use_pattern = '^USE (\w+);$'
        match = re.search(use_pattern, query_string)
        if match:
            op = 'use'
            level = 'database'
            name = match.group(1)

        create_drop_db_pattern = '^(CREATE|DROP) DATABASE (\w+);$'
        match = re.search(create_drop_db_pattern, query_string)
        if match:
            op = match.group(1).lower()
            level = 'database'
            name = match.group(2)

        create_table_pattern = '^CREATE TABLE (\w+)\(([\w, ()]+?)\);$'
        match = re.search(create_table_pattern, query_string)
        if match:
            op = 'create'
            level = 'table'
            name = match.group(1)
            argument_string = match.group(2)

            print(argument_string)

            attributes = []

            for argument in argument_string.split(','):
                attributes.append({
                    'name': argument.split(' ')[0],
                    'type': argument.split(' ')[1]
                })

            print(attributes)

        drop_table_pattern = '^DROP TABLE (\w+);$'
        match = re.search(drop_table_pattern, query_string)
        if match:
            op = 'drop'
            level = 'table'
            name = match.group(1)

    return op, level, name, attributes

