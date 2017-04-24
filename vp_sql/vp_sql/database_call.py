#!/usr/bin/env python3

from cohandler import TOKEN_DB_NAME
from dateutil.parser import parse


def is_date(string):
    try:
        a = parse(string)
        try:
            number = int(string)
            return False
        except Exception as e:
            pass
        return a
    except ValueError:
        return False


def check_type(key, params):
    typename = type(params[key]).__name__
    if params[key] == "":
        return ""
    if typename == "int":
        return key + " LIKE " + str(params[key])
    elif typename == "str":
        return key + " LIKE '" + params[key] + "'"
    return False


def offset(params):
    if "limit" in params.keys():
        final = "OFFSET " + params["offset"] + " ROWS FETCH NEXT " + params["limit"] + " ROWS ONLY"
    else:
        final = "OFFSET " + params["offset"] + " ROWS FETCH NEXT 20 ROWS ONLY"
    return final


def order_by(params):
    final = " ORDER BY "
    values = params["order"].split(",")
    for value in values:
        elems = value.split(".")
        for elem in elems:
            final += elem + " "
        final += ", "
    final = final[:-2]
    return final


def get_views(cursor, name, param):
    arguments = []
    query = "SELECT * FROM sys.views"
    return (execute_request(cursor, query, arguments))


def get_columns(cursor, table_name, param):
    arguments = []
    query = "SELECT * FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = ?"
    arguments.append(table_name.split('.')[1])
    return (execute_request(cursor, query, arguments))


def get_tables(cursor, name, param):
    query = "select table_schema, table_name from INFORMATION_SCHEMA.TABLES where TABLE_TYPE = 'BASE TABLE'"
    return (execute_request(cursor, query, []))


def execute_request(cursor, query, args):
    query = query.replace("--", "")
    query = query.replace("#", "")
    print (query + " | ", args)
    try:
        cursor.execute(query, *args)
    except Exception as e:
        print (e)
        return {'success': False}
    keys = []
    for elem in cursor.description:
        keys.append(elem[0])

    result = []
    for row in cursor:
        i = 0
        value = {}
        for elem in row:
            value[keys[i]] = elem
            i = i + 1
        result.append(value)
    return result


def function_call(cursor, function_name, params):
    arguments = []
    request = "SELECT * FROM " + function_name + "(" + params.get("arg") + ")"
    print (request, arguments)
    return (execute_request(cursor, request, arguments))


def where(params):
    final = " WHERE "
    a = False
    special_words = ["select", "order", "group", "limit", "offset"]
    tab = {
        "eq": "LIKE", "gte": ">=", "gt": ">", "lte": "<=", "lt": "<",
        "neq": "NOT LIKE", "like": "LIKE", "is": "IS"
    }
    for key in params.keys():
        if key in special_words:
            continue
        split = params[key].split(',')
        for elem in split:
            a = True
            value = elem.split('.')
            if len(value) == 2:
                final += key + " " + tab[value[0]] + " '" + value[1] + "' and "
            else:
                value[0] = value[0].replace("'", "\\'")
                value[0] = value[0].replace('"', '\\"')
                final += key + " LIKE '" + value[0] + "' and "
    if a is True:
        final = final[:-5]
    else:
        final = final[:-6]
    return final


def separate_select_params(params):
    all_params = []
    join = False
    tmp = ""
    for c in params:
        if c == ',' and not join:
            all_params.append(tmp)
            tmp = ""
        else:
            tmp += c
        if c == '{' or c == '}':
            join = not join

    all_params.append(tmp)

    select_params = []
    join_params = {}
    for elem in all_params:
        if elem.find('{') == -1:
            select_params.append(elem)
        else:
            elem = elem.split('{')
            name = elem[0]
            value = elem[1].strip('}')
            tmp = []
            for val in value.split(','):
                tmp.append(val)
            join_params[name] = tmp

    return select_params, join_params


def inner_join(table_name, join_params):
    query = ""
    if len(join_params) == 0:
        return (query)
    for key, value in join_params.items():
        query += " INNER JOIN (SELECT "
        for val in value:
            query += val + ","
        if len(value) != 0:
            query = query[:-1]
        query += " FROM " + key + ") on " + table_name + ".id = " + key + ".fk_id"
    return query


def select(cursor, table_name, params):
    arguments = []
    select_query = "SELECT "
    join_params = {}
    select_params = []
    if "limit" in params.keys() and "offset" not in params.keys():
        select_query += "TOP(?)"
        arguments.append(params["limit"])
    if 'select' in params.keys():
        select_params, join_params = separate_select_params(params["select"])
    if len(select_params) == 0:
        select_query += "*,"
    for param in select_params:
        select_query += "?,"
        arguments.append(param)
    select_query = select_query[:-1]

    select_query += " FROM " + table_name
    select_query += where(params)

    if "order" in params.keys():
        select_query += order_by(params)
    elif "offset" in params.keys():
        select_query += " ORDER BY (SELECT 0) "
    if "offset" in params.keys():
        select_query += offset(params)

    select_query += inner_join(table_name, join_params)
    return (execute_request(cursor, select_query, arguments))


def delete(cursor, table, params):
    query = "DELETE FROM " + table + " WHERE "
    for key, value in params.items():
        query += key + "=" + value + " and "
    if len(params) != 0:
        query = query[:-5]
    print (query)
    try:
        cursor.execute(query)
    except Exception as e:
        return {"success": False}
    return ({"success": True})


def update(cursor, table, params):
    arguments = []
    query = "UPDATE " + table + " SET "
    for key, value in params.items():
        value = value.replace("'", "\\'")
        value = value.replace('"', '\\"')
        if key == "fieldID":
            continue
        a = is_date(value)
        if not a:
            value = a
        query += key + " = ?,"
        arguments.append(value)
    if len(params) != 0:
        query = query[:-1]
    query += " FROM " + table + " "
    query += " WHERE Id=" + params["Id"]
    print (query + " | ", arguments)
    try:
        cursor.execute(query, *arguments)
    except Exception as e:
        print (e)
        return {"success": False}
    return ({"success": True})


def function_store(cursor, name, params):
    try:
        cursor.execute(params["query"])
    except Exception as e:
        print (e)
        return {"success": False}
    return ({"success": True})
