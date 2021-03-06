#!/usr/bin/env python3

import pyodbc
import logging
from . import serverconf
import jwt
import secrets
from datetime import datetime, timedelta
from happy_sql.serverconf import FIELD_SQL_TIMEOUT, FIELD_SQL_DRIVER

TOKEN_SERVER = "server"
TOKEN_DB_NAME = "dbname"
TOKEN_USER = "user"
TOKEN_PASSWORD = "password"
TOKEN_EXP = 'exp'

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_HOURS = 1


''' Transaction code, to be implemented'''
'''
transation_dict = {}


def check_transaction(params, tok):
    global transation_dict

    if params['cookie'] in transation_dict.keys():
        return params['cookie'], transation_dict[params['cookie']]
    else:
        co = pyodbc.connect(r'DRIVER={' +
                            serverconf.get_conf()[FIELD_SQL_DRIVER] + r'};'
                            r'SERVER=' + tok[TOKEN_SERVER] + r';'
                            r'DATABASE=' + tok[TOKEN_DB_NAME] + r';'
                            r'UID=' + tok[TOKEN_USER] + r';'
                            r'PWD=' + tok[TOKEN_PASSWORD],
                            timeout=serverconf.get_conf()[FIELD_SQL_TIMEOUT])
        # gen_cookie
        cookie = "lol"
        transation_dict.cookie = co
        return cookie, co
'''


def refresh_secret():
    global JWT_SECRET
    JWT_SECRET = secrets.token_bytes(secrets.choice(range(32, 64)))


def connect(token=None, params=dict()):
    try:
        if token is not None:
            token = token.encode('utf-8')
            try:
                tok = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except Exception as e:
                logging.error(e)
                return None, "you should reauthenticate"
        else:
            try:
                tok = dict()
                tok[TOKEN_SERVER] = params[TOKEN_SERVER]
                tok[TOKEN_DB_NAME] = params[TOKEN_DB_NAME]
                tok[TOKEN_USER] = params[TOKEN_USER]
                tok[TOKEN_PASSWORD] = params[TOKEN_PASSWORD]
                tok[TOKEN_EXP] = datetime.utcnow() + timedelta(
                    hours=JWT_EXP_DELTA_HOURS)
            except Exception as e:
                logging.error(e)
                return None, "missing parameters"
            token = jwt.encode(tok, JWT_SECRET, algorithm=JWT_ALGORITHM)
        tok[TOKEN_SERVER] = tok[TOKEN_SERVER].replace(':', ',')
        logging.debug(tok[TOKEN_SERVER])
        co = pyodbc.connect(r'DRIVER={' +
                            serverconf.get_conf()[FIELD_SQL_DRIVER] + r'};'
                            r'SERVER=' + tok[TOKEN_SERVER] + r';'
                            r'DATABASE=' + tok[TOKEN_DB_NAME] + r';'
                            r'UID=' + tok[TOKEN_USER] + r';'
                            r'PWD=' + tok[TOKEN_PASSWORD],
                            timeout=serverconf.get_conf()[FIELD_SQL_TIMEOUT])
        return co, token.decode("utf-8")
    except pyodbc.Error as ex:
        logging.error(ex)
    except jwt.ExpiredSignatureError:
        return None, "could not reach SQL server"
    return None, "could not reach SQL server"
