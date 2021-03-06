#!/usr/bin/env python3

import logging
from . import serverconf
from . import benchmark
from dateutil.parser import parse


def get_constraint(cursor, table_name):
    if table_name is not None:
        query = "SELECT TABLE_NAME, TABLE_SCHEMA, COLUMN_NAME, " \
                "CONSTRAINT_NAME FROM " \
                "INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE"
        sql_response = execute_request(cursor, query, [])
        for i in sql_response:
            if i['CONSTRAINT_NAME'].find("PK__") != -1:
                if i['TABLE_NAME'] == table_name.replace(
                                i['TABLE_SCHEMA'] + ".", "", 1):
                    logging.debug(i['COLUMN_NAME'])
                    return i['COLUMN_NAME']
        logging.warn("Primary key not found! Table is in read only mode.")
    return ""


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
        log.debug("YALA")
        return key + " LIKE " + str(params[key])
    elif typename == "str":
        log.debug("YOLO")
        return key + " LIKE '" + params[key] + "'"
    return False


def offset(params):
    if "limit" in params.keys():
        final = "OFFSET " + params["offset"] + " ROWS FETCH NEXT " + params[
            "limit"] + " ROWS ONLY"
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
    return execute_request(cursor, query, arguments)


def get_columns(cursor, table_name, param):
    arguments = []
    query = "SELECT * FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME = ?"
    arguments.append(table_name.split('.')[1])
    return execute_request(cursor, query, arguments)


def get_tables(cursor, name, param):
    query = "select table_schema, table_name from INFORMATION_SCHEMA.TABLES " \
            "where TABLE_TYPE = 'BASE TABLE'"
    return execute_request(cursor, query, [])


def execute_request(cursor, query, args):
    query = query.replace("--", "")
    query = query.replace("#", "")
    logging.debug(query + " | {}".format(args))
    if serverconf.is_benchmark():
        benchmark.delay_start()     # Benchmarking delay
    try:
        cursor.execute(query, *args)
    except Exception as e:
        logging.error(e)
        return {'success': False}
    if serverconf.is_benchmark():
        benchmark.delay_stop()  # Benchmarking delay
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
    logging.debug(request, arguments)
    return execute_request(cursor, request, arguments)


def where(params):
    final = " WHERE "
    a = False
    special_words = ["select", "order", "group", "limit", "offset"]
    tab = {
        "eq": "LIKE", "gte": ">=", "gt": ">", "lte": "<=", "lt": "<",
        "neq": "NOT LIKE", "like": "LIKE", "is": "IS", "between": "BETWEEN"
    }
    for key in params.keys():
        if key in special_words:
            continue
        split = params[key].split(',')
        for elem in split:
            a = True
            value = elem.split('.')
            if len(value) >= 2:
                final += key + " " + tab[value[0]] + " "
                i = 1
                while i < len(value):
                    final += value[i] + " and "
                    i += 1
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
        return query
    for key, value in join_params.items():
        query += " INNER JOIN (SELECT "
        for val in value:
            query += val + ","
        if len(value) != 0:
            query = query[:-1]
        query += " FROM " + key + ") on " + table_name + ".id = " + key + \
                 ".fk_id"
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
    row = False
    for param in select_params:
        if param == "ROW_NUMBER":
            row = True
        else:
            select_query += param + ","
    select_query = select_query[:-1]
    if row is False:
        select_query += " FROM " + table_name
    else:
        select_query += " FROM (select *, ROW_NUMBER() OVER (ORDER BY Id) " \
                        "ROW_NUMBER from " + table_name + ") AS A "
    select_query += where(params)

    if "order" in params.keys():
        select_query += order_by(params)
    elif "offset" in params.keys():
        select_query += " ORDER BY (SELECT 0) "
    if "offset" in params.keys():
        select_query += offset(params)

    select_query += inner_join(table_name, join_params)
    return execute_request(cursor, select_query, arguments)


def delete(cursor, table, params):
    query = "DELETE FROM " + table + " WHERE "
    for key, value in params.items():
        query += key + "=" + value + " and "
    if len(params) != 0:
        query = query[:-5]
    logging.debug(query)
    try:
        cursor.execute(query)
    except Exception as e:
        return {"success": False}
    return {"success": True}


def update(cursor, table, params):
    arguments = []
    guid = get_constraint(cursor, table)
    query = "UPDATE " + table + " SET "
    for key, value in params.items():
        value = value.replace("'", "\\'")
        value = value.replace('"', '\\"')
        if key == "fieldId" or key == guid:
            continue
        a = is_date(value)
        if a:
            value = a
        query += key + " = ?,"
        arguments.append(value)
    if len(params) != 0:
        query = query[:-1]
    query += " FROM " + table
    query += " WHERE " + guid + "=" + params["fieldId"]
    logging.debug(query + " | ", arguments)
    try:
        cursor.execute(query, *arguments)
    except Exception as e:
        logging.error(e)
        return {"success": False, "message": e}
    return {"success": True}


def store_procedure(cursor, name, params):
    # PROTECT FROM SQLI !!!!
    query = params["query"]
    try:
        cursor.execute(query)
    except Exception as e:
        logging.error(e)
        return {"success": False}
    return {"success": True}


def get_stored_procedure_name(cursor, p2, p3):
    try:
        cursor.execute("SELECT name FROM dbo.sysobjects WHERE (TYPE = 'P')")
    except Exception as e:
        logging.error(e)
        return {"success": False}
    code = []
    for row in cursor:
        a = row[0].split('\n')
        for line in a:
            if len(line) > 0:
                code.append(line)
    return {"names": code}


def get_stored_procedure_code(cursor, procName, p3):
    try:
        cursor.execute("EXEC sp_helptext N'" + procName + "'")
    except Exception as e:
        logging.error(e)
        return {"success": False}
    code = []
    for row in cursor:
        a = row[0].split('\n')
        for line in a:
            if len(line) > 0:
                code.append(line)
    return {procName: code}
