"""Logging configuration"""

import logging
from pathlib import Path


def setup_logging(level=logging.INFO, log_file: Path | None = None):
    """
    Configure logging for the application

    The console shows `level`; the optional log file also gets DEBUG messages
    from the agent package (full generated code and outputs).
    """
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console = logging.StreamHandler()
    console.setLevel(level)
    handlers = [console]
    if log_file is not None:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    for handler in handlers:
        handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=handlers)
    if log_file is not None:
        logging.getLogger("agent").setLevel(logging.DEBUG)
