import sys
from multiprocessing import Lock

ITERATIONS = 457
DELAY = 5
VERBOSE = False
STDIN = sys.stdin.fileno()
LOCK = Lock()
