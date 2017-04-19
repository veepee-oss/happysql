#!/usr/bin/env python3

import argparse
import configparser
import logging

'''Dictionary = {port: , sql_driver: , sql_timeout: , ip: ,}'''
SERVER_CONF_DIC = {}

DEFAULT_PORT = 8080
DEFAULT_SQL_DRIVER = "ODBC Driver 13 for SQL Server"
DEFAULT_SQL_TIMEOUT = 60
DEFAULT_IP = "0.0.0.0"
DEFAULT_MAX_USERS = 1000
DEFAULT_SERVER_TIMEOUT = 60

SECTION_SERVER = "SERVER"
FIELD_PORT = "Port"
FIELD_SQL_DRIVER = "SQLDriver"
FIELD_SQL_TIMEOUT = "SQLTimeout"
FIELD_IP = "Ip"
FIELD_MAX_USERS = "MaxUsers"
FIELD_SERVER_TIMEOUT = "ServerTimeout"

WARNING_BAD_CONF_FILE = "Configuration file not found! Using default values."


def load_server_conf():
    global SERVER_CONF_DIC
    parser = argparse.ArgumentParser(description="Run VP-SQL server.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help="server's port (default: %d)" % DEFAULT_PORT)
    parser.add_argument("--sql-driver", type=str, default=DEFAULT_SQL_DRIVER,
                        help="SQL driver used to perform SQL queries ("
                             "default: %s)" % DEFAULT_SQL_DRIVER)
    parser.add_argument("--sql-timeout", type=int, default=DEFAULT_SQL_TIMEOUT,
                        help="timeout of an SQL query in seconds (default: "
                             "%d)" % DEFAULT_SQL_TIMEOUT)
    parser.add_argument("--ip", type=str, default=DEFAULT_IP,
                        help="server's ip address (default: %s)" % DEFAULT_IP)
    parser.add_argument("--max-users", type=int, default=DEFAULT_MAX_USERS,
                        help="maximum number of simultaneous users (default: "
                             "%d)" % DEFAULT_MAX_USERS)
    parser.add_argument("--server-timeout", type=int,
                        default=DEFAULT_SERVER_TIMEOUT,
                        help="timeout of an http request (default: %d)" %
                             DEFAULT_SERVER_TIMEOUT)
    parser.add_argument("--file", type=str,
                        help="load server's configuration from file")
    args = parser.parse_args()
    if args.file is not None:
        load_server_conf_from_file(args)
    SERVER_CONF_DIC[FIELD_PORT] = args.port
    SERVER_CONF_DIC[FIELD_SQL_DRIVER] = args.sql_driver
    SERVER_CONF_DIC[FIELD_SQL_TIMEOUT] = args.sql_timeout
    SERVER_CONF_DIC[FIELD_IP] = args.ip
    SERVER_CONF_DIC[FIELD_MAX_USERS] = args.max_users
    SERVER_CONF_DIC[FIELD_SERVER_TIMEOUT] = args.server_timeout
    logging.info(SERVER_CONF_DIC)


def load_server_conf_from_file(args):
    config = configparser.ConfigParser()
    config.read(args.file)
    if len(config) < 2:
        logging.warn(WARNING_BAD_CONF_FILE)
    args.port = config.getint(SECTION_SERVER,
                              FIELD_PORT, fallback=DEFAULT_PORT)
    args.sql_driver = config.get(SECTION_SERVER, FIELD_SQL_DRIVER,
                                 fallback=DEFAULT_SQL_DRIVER)
    args.sql_timeout = config.getint(SECTION_SERVER, FIELD_SQL_TIMEOUT,
                                     fallback=DEFAULT_SQL_TIMEOUT)
    args.ip = config.get(SECTION_SERVER, FIELD_IP, fallback=DEFAULT_IP)
    args.max_users = config.get(SECTION_SERVER, FIELD_MAX_USERS,
                                fallback=DEFAULT_MAX_USERS)
    args.server_timeout = config.get(SECTION_SERVER, FIELD_SERVER_TIMEOUT,
                                     fallback=DEFAULT_SERVER_TIMEOUT)


def get_conf():
    return SERVER_CONF_DIC
