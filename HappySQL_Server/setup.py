from setuptools import setup

setup(
    name='HappySQL',
    version='1.0',
    description='RESTful API for Microsoft SQL Server',
    packages=['happy_sql'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_swagger',
        'flask_compress',
        'flask_cors',
        'pyodbc',
        'gevent',
        'PyJWT',
        'python-dateutil',
        ],
)
