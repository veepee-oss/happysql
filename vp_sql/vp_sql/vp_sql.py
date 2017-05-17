#!/usr/bin/env python3

import logging
import cohandler
import database_call
import serverconf
import benchmark
import datetime
from flask import Flask, request, abort, \
    render_template, jsonify, Response
from flask_apscheduler import APScheduler
from flask_compress import Compress
from flask_cors import CORS
from flask_swagger import swagger
from gevent.pool import Pool
from gevent.pywsgi import WSGIServer
from logging.handlers import RotatingFileHandler
from serverconf import FIELD_PORT, FIELD_IP, FIELD_MAX_USERS, \
    FIELD_SERVER_TIMEOUT, FIELD_DEBUG, FIELD_BENCHMARK

COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json',
                      'application/javascript']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500

app = Flask(__name__)
CORS(app, supports_credentials=True, expose_headers='X-Guid')
Compress(app)


# db_call is the function call for database
def call_db(db_call, table_name, params):
    token = request.headers.get("Authorization")
    logging.debug(token)
    co, token = cohandler.connect(token=token)
    if token is None or co is None:
        abort(500)
    cursor = co.cursor()
    guid = database_call.get_constraint(cursor, table_name)
    logging.debug(guid)
    value = db_call(cursor, table_name, params)
    if serverconf.is_benchmark():
        benchmark.delay_start()     # Benchmarking delay
    co.commit()
    if serverconf.is_benchmark():
        benchmark.delay_stop()  # Benchmarking delay
    resp = jsonify(value)
    resp.headers['X-Guid'] = guid
    return resp


@app.route('/api/doc', methods=['GET'])
def get_swagger_api():
    return render_template('api.html')


@app.route('/change_credz', methods=['POST'])
def change_credz():
    """
    Change credentials

    swagger_from_file: doc/change_credentials.yml
    """
    # token = request.headers.get("Authorization")
    args = request.form.to_dict()
    co, token = cohandler.connect(params=args)
    if co is None:
        abort(500)
    cursor = co.cursor()
    tables = database_call.get_tables(cursor, None, None)
    return jsonify({"success": True, "token": token, "tables": tables})


@app.route('/tables', methods=['GET'])
def get_tables():
    """
    Get all tables

    swagger_from_file: doc/tables.yml
    """
    return call_db(database_call.get_tables, None, None)


@app.route('/rpc/<function_name>', methods=['POST'])
def view_call(function_name):
    """
    Call user defined function

    swagger_from_file: doc/view_call.yml
    """
    args = request.form.to_dict()
    return call_db(database_call.function_call, function_name, args)


@app.route('/rpc/views', methods=["GET"])
def get_views():
    """
    Get all views

    swagger_from_file: doc/views.yml
    """
    return call_db(database_call.get_views, None, None)


@app.route('/rpc/new', methods=["POST"])
def add_stored_function():
    """
    Store user defined function

    swagger_from_file: doc/view_add.yml
    """
    args = request.form.to_dict()
    return call_db(database_call.function_store, None, params)


@app.route('/<table>/columns', methods=['GET'])
def get_columns(table):
    """
    Get columns of Table

    swagger_from_file: doc/columns.yml
    """
    return call_db(database_call.get_columns, table, None)


@app.route('/<table>/<fieldId>', methods=['PUT'])
def update_user(table, fieldId):
    """
    Update query

    """
    args = request.form.to_dict()
    logging.debug(fieldId)
    args["fieldId"] = fieldId
    logging.debug(args['fieldId'])
    return call_db(database_call.update, table, args)


@app.route('/<table>', methods=['DELETE'])
def delete(table):
    """
    Delete query

    """
    args = request.form.to_dict()
    return call_db(database_call.delete, table, args)


@app.route('/sp', methods=['GET'])
def get_procedure_names():
    """
    Get stored procedure names

    """
    return call_db(database_call.get_stored_procedure_name, None, None)
    # token = request.headers.get("Authorization")
    # co, token = cohandler.connect(token=token)
    # if token is None or co is None:
    #     abort(500)
    # cursor = co.cursor()
    # value = database_call.get_stored_procedure_name(cursor)
    # co.commit()
    # return jsonify(value)


@app.route('/sp/<sp_name>', methods=['GET'])
def get_procedure_code(sp_name):
    """
    Get stored procedure code

    """
    return call_db(database_call.get_stored_procedure_code, sp_name, None)


@app.route('/<table>', methods=['GET'])
def select(table):
    """
    Select query

    swagger_from_file: doc/select.yml
    """
    args = request.args.to_dict()
    return call_db(database_call.select, table, args)


@app.route("/spec")
def spec():
    swag = swagger(app, from_file_keyword='swagger_from_file')
    swag['info']['version'] = "0.5"
    swag['info']['title'] = "HappySQL"
    return jsonify(swag)


@app.before_request
def before_request(resp=None):
    if serverconf.get_conf()[FIELD_BENCHMARK]:
        benchmark.benchmark_start()
    return resp


@app.after_request
def after_request(resp=None):
    if serverconf.get_conf()[FIELD_BENCHMARK]:
        benchmark.benchmark_stop(request.endpoint)
    return resp


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


def run_server():
    global app
    serverconf.load_server_conf()

    if serverconf.is_debug():
        logging.getLogger().setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s :: %(levelname)s :: %(message)s',
            datefmt='%m/%d/%Y %H:%M:%S')
        file_handler = RotatingFileHandler('logs/debug_' +
                                           datetime.datetime.now().strftime(
                                               '%Y_%m_%d_%H_%M_%S') + '.log',
                                           'w')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_handler)
        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(steam_handler)
        logging.warn("Debug mode enabled!")
    elif serverconf.is_benchmark():
        logging.getLogger().setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s :: %(levelname)s :: %(message)s',
            datefmt='%m/%d/%Y %H:%M:%S')
        file_handler = RotatingFileHandler('logs/benchmark_' +
                                           datetime.datetime.now().strftime(
                                               '%Y_%m_%d_%H_%M_%S') + '.log',
                                           'w')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_handler)
        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(steam_handler)
        logging.warn("Benchmark mode enabled!")

    app.config.from_object(Config())
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    if serverconf.is_debug():
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
