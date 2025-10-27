"""Logging configuration for the agent system"""
import logging
import sys
from pathlib import Path


AGENT_LOGGER = "agent.llm"
FLOW_LOGGER = "agent.flow"


def setup_logging(level=logging.INFO, logs_dir: str = "logs"):
    """
    Configure two distinct loggers for the agent system.
    
    Args:
        level: Logging level (default: INFO)
        logs_dir: Directory to store log files (default: "logs")
    
    Loggers:
        - agent.llm: For LLM responses, token usage, and agent metadata
        - agent.flow: For application flow, events, and outputs
    """
    log_path = Path(logs_dir)
    log_path.mkdir(exist_ok=True)
    
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    
    agent_logger = logging.getLogger(AGENT_LOGGER)
    agent_logger.setLevel(level)
    agent_logger.propagate = False
    agent_file_handler = logging.FileHandler(
        log_path / f"agent_responses.log"
    )
    agent_file_handler.setLevel(level)
    agent_file_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(funcName)s:\n%(message)s\n" + "="*80,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    agent_file_handler.setFormatter(agent_file_formatter)
    agent_logger.addHandler(agent_file_handler)
    
    flow_logger = logging.getLogger(FLOW_LOGGER)
    flow_logger.setLevel(level)
    flow_logger.propagate = False
    flow_console_handler = logging.StreamHandler(sys.stdout)
    flow_console_handler.setLevel(level)
    flow_console_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )
    flow_console_handler.setFormatter(flow_console_formatter)
    flow_logger.addHandler(flow_console_handler)
    flow_file_handler = logging.FileHandler(
        log_path / f"flow.log"
    )
    flow_file_handler.setLevel(level)
    flow_file_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    flow_file_handler.setFormatter(flow_file_formatter)
    flow_logger.addHandler(flow_file_handler)

    root_logger.setLevel(logging.INFO)
    root_console_handler = logging.StreamHandler(sys.stderr)
    root_console_handler.setLevel(logging.INFO)
    root_console_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    root_console_handler.setFormatter(root_console_formatter)
    root_logger.addHandler(root_console_handler)
    
    flow_logger.info(f"Logging initialized - Logs directory: {log_path.absolute()}")
    flow_logger.info(f"Agent responses → {log_path / f'agent_responses.log'}")
    flow_logger.info(f"Flow logs → {log_path / f'flow.log'}")
    
    return agent_logger, flow_logger


def get_agent_logger():
    """Get the agent/LLM logger instance"""
    return logging.getLogger(AGENT_LOGGER)


def get_flow_logger():
    """Get the flow logger instance"""
    return logging.getLogger(FLOW_LOGGER)