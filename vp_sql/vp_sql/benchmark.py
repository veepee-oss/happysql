import logging
import datetime

START_TIME = None


def benchmark_start():
    global START_TIME
    START_TIME = datetime.datetime.now()


def benchmark_stop():
    global START_TIME
    elapsed_time = datetime.datetime.now() - START_TIME
    logging.info("Benchmark: %d", elapsed_time.microseconds)
