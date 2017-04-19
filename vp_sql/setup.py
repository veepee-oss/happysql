from setuptools import setup

setup(
    name='vp_sql',
    version='0.5',
    description='REST API for sqlserver',
    packages=['vp_sql'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_swagger',
        'flask_compress',
        'flask_cors',
        'pyodbc',
        'gevent',
        'PyJWT'
        ],
)
