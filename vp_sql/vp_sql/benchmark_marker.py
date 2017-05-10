import re
import logging

BENCHMARK_FILE = "benchmark.log"
BENCHMARK_REGEX = r'^.*:: INFO :: Benchmark: ([0-9]+).*$'
BENCHMARK_DEST_FILE = "benchmark_graph.log"


def parse_lines():
    file = open(BENCHMARK_FILE, 'r')
    lines = file.readlines()
    res_lines = []
    for i in lines:
        if i.find(":: INFO ::") != -1:
            res_lines.append(i.strip('\n'))
    return res_lines


def find_benchmark(lines):
    res_file = []
    prog = re.compile(BENCHMARK_REGEX)
    for i in lines:
        result = prog.match(i)
        if result:
            res_file.append(result.group(1))
    return res_file


def write_to_file(res_file):
    file = open(BENCHMARK_DEST_FILE, 'w')
    for i in res_file:
        file.write(i + '\n')


if __name__ == "__main__":
    try:
        lines = parse_lines()
        res_file = find_benchmark(lines)
        write_to_file(res_file)
        print("Job is done!")
    except Exception as e:
        logging.error(e)
