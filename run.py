"""Main entry point for the data analysis agent system"""

import logging
import mlflow
import argparse
from dotenv import load_dotenv
from pathlib import Path
from agent.config import settings
from agent.logging_config import setup_logging
from agent.data_loader import load_dataset, generate_dataset_info
from agent.graph import build_hierarchical_graph


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

    mlflow.set_experiment("Agent")
    mlflow.langchain.autolog()

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
    run_name = "hierarchical_analysis"
    initial_state = {"dataset_info": dataset_info, "dataset_path": str(datafile)}

    # Run workflow with MLflow tracking
    with mlflow.start_run(run_name=run_name):
        mlflow.log_param("dataset", str(datafile))
        mlflow.log_param("model_analyst", settings.analyst_model)
        mlflow.log_param("model_coder", settings.coder_model)

        logger.info("Running analysis flow...")

        result = workflow.invoke(initial_state)

        # Log results
        mlflow.log_dict(result, "workflow_result.json")
        if result.get("report"):
            mlflow.log_text(result["report"], "final_report.txt")

            # Save report to file
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
