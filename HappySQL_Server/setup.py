from setuptools import setup

setup(
    name='HappySQL',
    version='1.0',
    description='RESTful API for Microsoft SQL Server',
    keywords='vente-privee sql mssql server happysql rest resful api',
    author=['Anis BENNABI', 'Louis GIESEN'],
    author_email=['abennabi@vente-privee.com', 'lgiesen@vente-privee.com'],
    url=['https://git.vpgrp.io/vp-labs/happysql'],
    packages=['happy_sql'],
    install_requires=[
        'flask_swagger',
        'flask_apscheduler',
        'flask_compress',
        'flask_cors',
        'flask',
        'pyodbc',
        'gevent',
        'PyJWT',
        'python-dateutil',
        ],
)
