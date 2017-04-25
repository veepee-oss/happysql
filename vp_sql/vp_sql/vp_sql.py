#!/usr/bin/env python3

import serverconf
import database_call
import cohandler
import werkzeug.serving
import logging
from flask import Flask, request, session, g, redirect, url_for, abort,\
    render_template, flash, jsonify
from flask_swagger import swagger
from gevent.pywsgi import WSGIServer
from flask_compress import Compress
from flask_cors import CORS, cross_origin
from flask_apscheduler import APScheduler
from gevent.pool import Pool
from serverconf import FIELD_PORT, FIELD_IP, FIELD_MAX_USERS,\
    FIELD_SERVER_TIMEOUT


COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json',
                      'application/javascript']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app, supports_credentials=True)
Compress(app)


# db_call is the function call for database
def call_db(token, db_call, table_name, params):
    token = request.headers.get("Authorization")
    co, token = cohandler.connect(token=token)
    if token is None or co is None:
        abort(500)
    cursor = co.cursor()
    value = db_call(cursor, table_name, params)
    co.commit()
    return jsonify(value)


@app.route('/api/doc', methods=['GET'])
def get_swagger_api():
    return render_template('api.html')


@app.route('/change_credz', methods=['POST'])
def change_credz():
    """
    Change credentials

    swagger_from_file: doc/change_credentials.yml
    """
    args = request.form.to_dict()
    co, token = cohandler.connect(params=args)
    if co is None:
        abort(500)
    cursor = co.cursor()
    tables = database_call.get_tables(cursor, None, None)
    return jsonify({"success": True, "token": token, "tables": tables})


@app.route('/tables', methods=['GET'])
def get_tables():
    token = request.headers.get("Authorization")
    return (call_db(token, database_call.get_tables, None, None))


@app.route('/rpc/<function_name>', methods=['POST'])
def view_call(function_name):
    """
    Call user defined function

    swagger_from_file: doc/view_call.yml
    """
    token = request.headers.get("Authorization")
    args = request.form.to_dict()
    return (call_db(token, database_call.function_call, function_name, args))


@app.route('/rpc/views', methods=["GET"])
def get_views():
    """
    Get all views

    """
    token = request.headers.get("Authorization")
    return (call_db(token, database_call.get_views, None, None))


@app.route('/rpc/new', methods=["POST"])
def add_stored_function():
    """
    Store user defined function

    """
    token = request.headers.get("Authorization")
    args = request.form.to_dict()
    return (call_db(token, database_call.function_store, None, params))


@app.route('/<table>/columns', methods=['GET'])
def get_columns(table):
    """
    Get columns of Table

    """
    token = request.headers.get("Authorization")
    return (call_db(token, database_call.get_columns, table, None))


@app.route('/<table>/<fieldId>', methods=['PUT'])
def update_user(table, fieldId):
    """
    Update query

    """
    token = request.headers.get("Authorization")
    args = request.form.to_dict()
    args["fieldID"] = fieldId
    return (call_db(token, database_call.update, table, args))


@app.route('/<table>', methods=['DELETE'])
def delete(table):
    """
    Delete query

    """
    token = request.headers.get("Authorization")
    args = request.form.to_dict()
    return (call_db(token, database_call.delete, table, args))


@app.route('/<table>', methods=['GET'])
def select(table):
    """
    Select query

    swagger_from_file: doc/select.yml
    """
    token = request.headers.get("Authorization")
    args = request.args.to_dict()
    return (call_db(token, database_call.select, table, args))


@app.route("/spec")
def spec():
    swag = swagger(app, from_file_keyword='swagger_from_file')
    swag['info']['version'] = "0.5"
    swag['info']['title'] = "SQLServer REST API"
    return jsonify(swag)


class Config(object):
    JOBS = [
        {
            'id': 'refresh_secret',
            'func': 'cohandler:refresh_secret',
            'args': (),
            'trigger': 'interval',
            'hours': 1
        }
    ]

    SCHEDULER_API_ENABLED = True


@werkzeug.serving.run_with_reloader
def run_server():
    serverconf.load_server_conf()
    app.config.from_object(Config())
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)

    # Debug enabled
    app.debug = True

    cohandler.refresh_secret()
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    pool = Pool(serverconf.get_conf()[FIELD_MAX_USERS])
    http_server = WSGIServer((serverconf.get_conf()[FIELD_IP],
                              serverconf.get_conf()[FIELD_PORT]),
                             app, spawn=pool)
    http_server.serve_forever(stop_timeout=
                              serverconf.get_conf()[FIELD_SERVER_TIMEOUT])


if __name__ == "__main__":
    run_server()
