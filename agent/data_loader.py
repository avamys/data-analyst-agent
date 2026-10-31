"""Data loading utilities"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)


def load_dataset(filepath: str) -> pd.DataFrame:
    """Load dataset from CSV file"""
    df = pd.read_csv(filepath)
    return df


def generate_dataset_info(df: pd.DataFrame, filepath: str) -> str:
    """Generate comprehensive dataset information for LLM"""
    return f"""
    file: {filepath}
    Columns: {", ".join([col for col in df.columns])}
    {len(df)} rows. {" | ".join([f"{col}: {df[col].dtype}" for col in df.columns])}
    
    Sample data:
    {df.head().to_markdown()}
    
    Statistical summary:
    {df.describe().to_markdown()}
    
    Categorical summary:
    {df.describe(include="object").to_markdown() if len(df.select_dtypes(include="object").columns) > 0 else "No categorical columns"}
    """
