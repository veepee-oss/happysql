import argparse
import re
import logging
import datetime

BENCHMARK_FILE = "benchmark.log"
BENCHMARK_REGEX = r'^(.*) :: INFO :: BENCHMARK : (.+) = ([0-9]+.[0-9]+)$'
BENCHMARK_DEST_FILE = "benchmark_graph.csv"


def parse_lines(req):
    file = open(BENCHMARK_FILE, 'r')
    lines = file.readlines()
    res_lines = []
    if req is None:
        req = ""
    for i in lines:
        if i.find(":: INFO :: BENCHMARK : " + req) != -1:
            res_lines.append(i.strip('\n'))
    return res_lines


def find_benchmark(lines):
    res_file = []
    prog = re.compile(BENCHMARK_REGEX)
    for i in lines:
        result = prog.match(i)
        if result:
            data = []
            data.append(result.group(1))
            data.append(result.group(2))
            data.append(result.group(3))
            res_file.append(data)
    return res_file


def write_to_file(res_file):
    file = open(BENCHMARK_DEST_FILE, 'w')
    for i in res_file:
        file.write(i[0] + ',' + i[1] + ',' + i[2] + '\n')


def choose_request():
    global BENCHMARK_DEST_FILE
    global BENCHMARK_FILE
    parser = argparse.ArgumentParser(description="Parse HappySQL log file.")
    parser.add_argument("-r", "--request", type=str, default=None,
                        help="benchmarked request (default: ALL)")
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="input file name")
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="output file name (default: "
                             "benchmark_<query>_<timestamp>.csv")
    args = parser.parse_args()
    BENCHMARK_FILE = args.input
    BENCHMARK_DEST_FILE = args.output
    if BENCHMARK_DEST_FILE is None:
        str_req = "" if args.request is None else args.request
        BENCHMARK_DEST_FILE = 'csv/benchmark_' + str_req + '_'\
                              + datetime.datetime.now().strftime(
                                '%Y_%m_%d_%H_%M_%S')\
                              + '.csv'
    return args.request


if __name__ == "__main__":
    try:
        print("Parsing...")
        req = choose_request()
        lines = parse_lines(req)
        res_file = find_benchmark(lines)
        write_to_file(res_file)
        print("Job is done!")
    except Exception as e:
        logging.error(e)
