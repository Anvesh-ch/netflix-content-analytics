import yaml
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path: str = "configs/config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
        raise

def get_database_connection(config: Dict[str, Any]) -> psycopg2.extensions.connection:
    """Create a direct PostgreSQL connection."""
    try:
        conn = psycopg2.connect(
            host=config['database']['host'],
            port=config['database']['port'],
            database=config['database']['database'],
            user=config['database']['user'],
            password=config['database']['password']
        )
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise

def get_sqlalchemy_engine(config: Dict[str, Any]) -> Any:
    """Create SQLAlchemy engine for pandas operations."""
    try:
        connection_string = f"postgresql://{config['database']['user']}:{config['database']['password']}@{config['database']['host']}:{config['database']['port']}/{config['database']['database']}"
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        logger.error(f"SQLAlchemy engine creation failed: {e}")
        raise

def validate_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """Validate data quality of the Netflix dataset."""
    validation_results = {
        'total_rows': len(df),
        'null_counts': df.isnull().sum().to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'data_types': df.dtypes.to_dict(),
        'unique_values': {col: df[col].nunique() for col in df.columns}
    }
    
    # Check required columns
    required_columns = ['show_id', 'title', 'type', 'release_year']
    missing_required = [col for col in required_columns if col not in df.columns]
    validation_results['missing_required_columns'] = missing_required
    
    # Check for nulls in required columns
    if not missing_required:
        nulls_in_required = df[required_columns].isnull().sum().to_dict()
        validation_results['nulls_in_required_columns'] = nulls_in_required
    
    # Check release year range
    if 'release_year' in df.columns:
        year_range = df['release_year'].describe()
        validation_results['release_year_range'] = {
            'min': year_range['min'],
            'max': year_range['max'],
            'mean': year_range['mean']
        }
    
    return validation_results

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare the Netflix dataset for database insertion."""
    df_clean = df.copy()
    
    # Convert date_added to proper date format
    if 'date_added' in df_clean.columns:
        df_clean['date_added'] = pd.to_datetime(df_clean['date_added'], errors='coerce')
    
    # Ensure release_year is integer
    if 'release_year' in df_clean.columns:
        df_clean['release_year'] = pd.to_numeric(df_clean['release_year'], errors='coerce').astype('Int64')
    
    # Clean text fields - remove extra whitespace
    text_columns = ['title', 'director', 'cast', 'country', 'rating', 'duration', 'listed_in', 'description']
    for col in text_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].replace('nan', None)
    
    return df_clean

def export_view_to_csv(engine: Any, view_name: str, output_path: str) -> bool:
    """Export a database view to CSV file."""
    try:
        query = f"SELECT * FROM {view_name}"
        df = pd.read_sql(query, engine)
        df.to_csv(output_path, index=False)
        logger.info(f"Successfully exported {view_name} to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to export {view_name}: {e}")
        return False

def run_sql_script(conn: psycopg2.extensions.connection, script_path: str) -> bool:
    """Run a SQL script file."""
    try:
        with open(script_path, 'r') as file:
            sql_script = file.read()
        
        with conn.cursor() as cursor:
            cursor.execute(sql_script)
            conn.commit()
        
        logger.info(f"Successfully executed SQL script: {script_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to execute SQL script {script_path}: {e}")
        conn.rollback()
        return False
