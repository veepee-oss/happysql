import logging
import time

START_TIME = None


def benchmark_start():
    global START_TIME
    START_TIME = time.time()


def benchmark_stop(req):
    global START_TIME
    elapsed_time = time.time() - START_TIME
    logging.info("BENCHMARK : %s = %f", req,elapsed_time)
