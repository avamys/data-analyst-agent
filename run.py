"""Runs one analysis: the same as `analyst run <csv>` (kept for the eval runner)"""

import sys

from agent.cli import main

if __name__ == "__main__":
    sys.exit(main(["run", *sys.argv[1:]]))
