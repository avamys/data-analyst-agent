"""Main entry point for the data analysis agent system"""
import logging
import mlflow
from pathlib import Path
from agent.config import settings
from agent.logging_config import setup_logging
from agent.data_loader import load_dataset, generate_dataset_info
from agent.graph.builder import build_graph


logger = logging.getLogger(__name__)


def main():
    """Run the data analysis workflow"""
    setup_logging(settings.log_level)

    mlflow.set_experiment("Agent")
    mlflow.langchain.autolog()
    
    logger.info("Starting data analysis workflow")

    datafile = Path(settings.data_directory) / "titanic.csv"
    df = load_dataset(str(datafile))
    workflow = build_graph()
    dataset_info = generate_dataset_info(df, str(datafile))

    with mlflow.start_run(run_name="data_analysis_workflow") as run:
        mlflow.log_param("dataset", str(datafile))
        mlflow.log_param("model_analyst", settings.analyst_model)
        mlflow.log_param("model_coder", settings.coder_model)
  
        logger.info("Running analysis flow...")

        result = workflow.invoke({"dataset_info": dataset_info})

        mlflow.log_dict(result, "workflow_result.json")
        if result.get('report'):
            mlflow.log_text(result['report'], "final_report.txt")
        
        logger.info("Analysis flow completed")
        logger.info(f"\n{result.get('report', 'No report generated')}")

if __name__ == "__main__":
    main()