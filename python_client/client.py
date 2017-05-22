#!/usr/bin/env python

# coding: utf8

import requests
# from pwn import *

# p = log.progress("Hacking in progress")
URL = "http://localhost:8080"


token = ""


def help():
    print("+-----------------------------------------+")
    print("| CONNECT {user} {pass} {dbname} {server} |")
    print("| GET {table} [Columns,...]               |")
    print("+-----------------------------------------+")


def select_columns(all_columns, json):
    for line in json:
        final_line = "|"
        for elem in all_columns:
            try:
                final_line = final_line + " " + str(line[elem])[:20] + " " * (20 - len(str(line[elem]))) + " |"
            except Exception as e:
                final_line = final_line + " ERROR" + " " * (20 - len("ERROR")) + " |"
        print(final_line)


def select_all(args):
    global token
    url = URL + "/" + args[1] + "/columns"
    headers = {"Authorization": token}
    r = requests.get(url, headers=headers)
    json_columns = r.json()
    columns = "|"
    all_columns = []
    for elem in json_columns:
        columns = columns + " " + elem['COLUMN_NAME'][:20] + " " * (20 - len(elem['COLUMN_NAME'])) + " |"
        all_columns.append(elem['COLUMN_NAME'])
    print(columns)
    print("_" * len(columns))
    url = URL + "/" + args[1]
    headers = {"Authorization": token}
    r = requests.get(url, headers=headers)
    json = r.json()
    select_columns(all_columns, json)


def select_column(args):
    global token
    all_columns = args[2:]
    columns = "|"
    url = URL + "/" + args[1] + "?select="
    for elem in all_columns:
        columns = columns + " " + elem[:20] + " " * (20 - len(elem)) + " |"
        url += elem + ","
    print(columns)
    print("_" * len(columns))
    url = url[:-1]
    headers = {"Authorization": token}
    r = requests.get(url, headers=headers)
    json = r.json()
    select_columns(all_columns, json)


def select(args):
    if len(args) < 2:
        print("Wrong number of arguments, write HELP for more informations")
        return
    elif len(args) == 2:
        select_all(args)
    else:
        select_column(args)


def connect(args):
    global token
    url = URL + "/change_credz"
    if len(args) != 5:
        print("Wrong number of arguments, write HELP for more informations")
        return
    data = {"user": args[1], "password": args[2],
            "dbname": args[3], "server": args[4]}
    r = requests.post(url, data=data)
    json = r.json()
    if json['success'] is True:
        print("-----------TABLES-----------")
        for elem in json['tables']:
            print(elem['table_schema'] + "." + elem['table_name'])
        print("----------------------------")
        token = json['token']


def read_until_exit():
    try:
        while True:
            inp = raw_input("> ")
            sent = inp.split()
            if len(sent) == 0 or sent[0] == "EXIT":
                print("Goodbye !")
                break
            if sent[0] == "CONNECT":
                connect(sent)
            elif sent[0] == "GET":
                select(sent)
            elif sent[0] == "HELP":
                help()
            else:
                help()
    except Exception as e:
        print(e)
        print("You left without saying goodbye :-(")


read_until_exit()
