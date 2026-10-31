"""Main entry point for the data analysis agent system"""

import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv

from agent.config import settings
from agent.data_loader import generate_dataset_info, load_dataset
from agent.graph import build_hierarchical_graph
from agent.logging_config import setup_logging

load_dotenv()
logger = logging.getLogger(__name__)


def main():
    """Run the data analysis workflow"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Data Analysis Agent")
    parser.add_argument(
        "--dataset",
        type=str,
        default="titanic.csv",
        help="Dataset filename in the data directory",
    )
    args = parser.parse_args()

    setup_logging(settings.log_level)

    logger.info("Starting data analysis workflow")

    # Load dataset
    datafile = Path(settings.data_directory) / args.dataset
    if not datafile.exists():
        logger.error(f"Dataset not found: {datafile}")
        return

    df = load_dataset(str(datafile))
    dataset_info = generate_dataset_info(df, str(datafile))

    logger.info("Building hierarchical multi-agent workflow...")
    workflow = build_hierarchical_graph()
    initial_state = {"dataset_info": dataset_info, "dataset_path": str(datafile)}

    # Traced in LangSmith when LANGSMITH_TRACING is enabled
    config = {
        "run_name": f"analysis:{datafile.stem}",
        "tags": [datafile.stem, settings.analyst_model],
        "metadata": {
            "dataset": str(datafile),
            "model_analyst": settings.analyst_model,
            "model_coder": settings.coder_model,
            "model_reporter": settings.reporter_model,
        },
    }

    logger.info("Running analysis flow...")
    result = workflow.invoke(initial_state, config=config)

    if result.get("report"):
        output_dir = Path(settings.output_directory)
        output_dir.mkdir(exist_ok=True)
        report_file = output_dir / f"report_{datafile.stem}.md"
        report_file.write_text(result["report"])
        logger.info(f"Report saved to: {report_file}")

    logger.info("=" * 70)
    logger.info("Analysis flow completed")
    logger.info("=" * 70)
    logger.info(f"\n{result.get('report', 'No report generated')}")


if __name__ == "__main__":
    main()
