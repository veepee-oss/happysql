# HappySQL_Server
## Description
A Python REST server implementing a RESTful API and interpreting REST
requests into MSSQL requests.

<br/>

## Supported Databases
* Microsoft SQL Server (2005, 2008, 2012 & 2016)

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

#### Docker install

```
git clone git@git.vpgrp.io:vp-labs/happysql.git

# Builds happysql:dev docker image.
docker build --tag happysql:dev $(pwd)/happysql/HappySQL_Server/docker

# Enters in happysql:dev container.
docker run \
  --hostname happy \
  --interactive \
  --tty \
  --publish 127.0.0.1:8080:8080 \
  --volume $(pwd)/happysql/HappySQL_Server:/happy-server \
  happysql:dev \
  /bin/bash
```

When in the container, go to `/happy-server` then happy hacking !

Note: If you run the server in the container, it will be available at port
8080. If you want to change that, please update `--publish` in the docker
command above and happy server `--port` argument accordingly.

Note: From there, you can follow 'Classic install' steps. Have
in mind that you will have to re-run 'Classic install' steps every
time you exit the container. At the moment, we don't provide any
`virtualenv` environment.

#### Pip install coming soon...

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
$ python3 happy_sql_server.py --help
```
