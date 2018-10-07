import re


def parse_query(query_string):
    is_distinct = False
    projection = None
    table_name = None
    condition = None
    order_by = None
    order_by_sort = None

    match_pattern = '^SELECT ([\w*, \.]+) FROM (\w+);$'
    match = re.search(match_pattern, query_string)
    if match:
        projection = match.group(1)
        table_name = match.group(2)

    match_pattern = '^SELECT DISTINCT ([\w*, \.]+) FROM (\w+);'
    match = re.search(match_pattern, query_string)
    if match:
        projection = match.group(1)
        table_name = match.group(2)
        is_distinct = True

    match_pattern = '^SELECT ([\w*, \.]+) FROM (\w+) WHERE ([\w+=" ()]+);$'
    match = re.search(match_pattern, query_string)
    if match:
        projection = match.group(1)
        table_name = match.group(2)
        condition = match.group(3)

    # ordered by ASCENDING by default
    match_pattern = '^SELECT ([\w*, \.]+) FROM (\w+) ORDER BY ([\w, ]+?)(?: (DESC|ASC))?;$'
    match = re.search(match_pattern, query_string)
    if match:
        projection = match.group(1)
        table_name = match.group(2)
        order_by = match.group(3)
        order_by_sort = match.group(4)
        print(order_by_sort)

    match_pattern = '^SELECT ([\w*, \.]+) FROM (\w+) WHERE (Country=\"Mexico\");$'
    match = re.search(match_pattern, query_string)
    if match:
        projection = match.group(1)
        table_name = match.group(2)
        condition = match.group(3)

    return {
        'projection': projection,
        'table_name': table_name,
        'is_distinct': is_distinct,
        'condition': condition,
        'order_by': order_by,
        'order_by_sort': order_by_sort if order_by_sort is not None else 'ASC'
    }