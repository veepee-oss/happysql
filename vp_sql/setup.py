from setuptools import setup

setup(
    name='HappySQL',
    version='0.5',
    description='REST API for SQL Server',
    packages=['HappySQL'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_swagger',
        'flask_compress',
        'flask_cors',
        'pyodbc',
        'gevent',
        'PyJWT',
        'python-dateutil'
        ],
)
