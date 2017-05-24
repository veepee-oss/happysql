from setuptools import setup

setup(
    name='HappySQL',
    version='1.0',
    description='RESTful API for Microsoft SQL Server',
    keywords='vente-privee sql mssql server happysql rest resful api',
    author=['Anis BENNABI', 'Louis GIESEN'],
    author_email=['abennabi@vente-privee.com', 'lgiesen@vente-privee.com'],
    url=['https://git.vpgrp.io/vp-labs/happysql'],
    packages=['happy_sql', 'happy_sql_benchmarking_tool'],
    include_package_data=True,
    install_requires=[
        'flask_swagger',
        'flask_compress',
        'flask_cors',
        'flask',
        'pyodbc',
        'gevent',
        'PyJWT',
        'python-dateutil',
        ],
)
