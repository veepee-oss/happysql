#!/usr/bin/env python3

import pyodbc
import logging
import serverconf
import jwt
import secrets
from datetime import datetime, timedelta
from serverconf import FIELD_SQL_TIMEOUT, FIELD_SQL_DRIVER


TOKEN_SERVER = "server"
TOKEN_DB_NAME = "dbname"
TOKEN_USER = "user"
TOKEN_PASSWORD = "password"
TOKEN_EXP = 'exp'

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_HOURS = 1


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
                return None, "missing parameters"
            token = jwt.encode(tok, JWT_SECRET, algorithm=JWT_ALGORITHM)
        co = pyodbc.connect(r'DRIVER={' +
                            serverconf.get_conf()[FIELD_SQL_DRIVER] + r'};'
                            r'SERVER=' + tok[TOKEN_SERVER] + r';'
                            r'DATABASE=' + tok[TOKEN_DB_NAME] + r';'
                            r'UID=' + tok[TOKEN_USER] + r';'
                            r'PWD=' + tok[TOKEN_PASSWORD],
                            timeout=serverconf.get_conf()[FIELD_SQL_TIMEOUT])
        return co, token.decode("utf-8")
    except pyodbc.Error as ex:
        logging.warn(ex)
    except jwt.ExpiredSignatureError:
        return None, "could not reach SQL server"
    return None, "could not reach SQL server"
