# HappySQL_Server
## Description
A Python REST server implementing a RESTful API and interpreting REST
requests into MSSQL requests.

<br/>

## Supported Databases
* Microsoft SQL Server (2005, 2008, 2012 & 2016)
* PostgreSQL

<br/>

## System requirements
* Debian 8.x Jessie (or any Debian based system)
* Python version 3.6 or higher
* Python-pip version 3.6 or higher

## Required packages
* unixodbc
* unixodbc-dev
* ODBC Driver for SQL Server (version 11 or 13)

## Python packages included with HappySQL
* flask
* flask_swagger
* flask_apscheduler
* flask_compress
* flask_cors
* pyodbc
* gevent
* PyJWT
* python-dateutil

<br/>

## Install
### Classic install:
```bash
$ python3 setup.py build
$ sudo python3 setup.py install
```
#### Pip and Docker install coming soon...

<br/>

## Usage
### Import and run HappySQL in a Python file:
```python
import happy_sql

happy_sql.run_server()
```

### OR

### Run our precoded file:
```bash
$ python3 happy_sql_server.py
```
