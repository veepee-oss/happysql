import logging
import time

START_TIME = None
DELAY_START = None


def benchmark_start():
    global START_TIME
    START_TIME = time.time()


def benchmark_stop(req):
    global START_TIME
    elapsed_time = time.time() - START_TIME
    logging.info("BENCHMARK : %s = %f", req, elapsed_time)


def delay_start():
    global DELAY_START
    DELAY_START = time.time()


def delay_stop():
    global DELAY_START
    global START_TIME
    delay = time.time() - DELAY_START
    START_TIME = START_TIME + delay
