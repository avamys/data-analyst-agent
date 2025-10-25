"""Main entry point for the data analysis agent system"""
import logging
from pathlib import Path
from agent.config import settings
from agent.logging_config import setup_logging
from agent.data_loader import load_dataset, generate_dataset_info
from agent.graph.builder import build_graph

logger = logging.getLogger(__name__)

def main():
    """Run the data analysis workflow"""
    setup_logging(settings.log_level)
    
    logger.info("Starting data analysis workflow")

    datafile = Path(settings.data_directory) / "titanic.csv"
    df = load_dataset(str(datafile))

    workflow = build_graph()

    dataset_info = generate_dataset_info(df, str(datafile))

    logger.info("Running analysis flow...")
    result = workflow.invoke({"dataset_info": dataset_info})
    
    logger.info("Analysis flow completed")
    logger.info(f"\n{result.get('report', 'No report generated')}")

if __name__ == "__main__":
    main()