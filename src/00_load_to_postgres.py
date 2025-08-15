#!/usr/bin/env python3
"""
Netflix Content Analytics - Data Loading Script
Loads the Netflix titles dataset into PostgreSQL database.
"""

import sys
import os
import pandas as pd
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from utils import (
    load_config, 
    get_database_connection, 
    get_sqlalchemy_engine,
    validate_data_quality,
    clean_dataframe,
    run_sql_script
)

def main():
    """Main function to load Netflix data into PostgreSQL."""
    print("Starting Netflix data loading process...")
    
    try:
        # Load configuration
        config = load_config()
        print("Configuration loaded successfully.")
        
        # Read the CSV file
        csv_path = config['data']['raw_csv']
        print(f"Reading CSV file: {csv_path}")
        
        df = pd.read_csv(csv_path)
        print(f"CSV loaded successfully. Shape: {df.shape}")
        
        # Validate data quality
        print("Validating data quality...")
        validation_results = validate_data_quality(df)
        
        print(f"Data validation results:")
        print(f"  Total rows: {validation_results['total_rows']}")
        print(f"  Duplicate rows: {validation_results['duplicate_rows']}")
        print(f"  Missing required columns: {validation_results['missing_required_columns']}")
        
        if validation_results['missing_required_columns']:
            print("ERROR: Required columns are missing!")
            return False
        
        # Check for nulls in required columns
        nulls_in_required = validation_results.get('nulls_in_required_columns', {})
        if any(nulls_in_required.values()):
            print("WARNING: Found nulls in required columns:")
            for col, null_count in nulls_in_required.items():
                if null_count > 0:
                    print(f"  {col}: {null_count} nulls")
        
        # Clean the dataframe
        print("Cleaning data...")
        df_clean = clean_dataframe(df)
        
        # Connect to database
        print("Connecting to PostgreSQL...")
        conn = get_database_connection(config)
        engine = get_sqlalchemy_engine(config)
        
        # Create tables
        print("Creating database tables...")
        create_tables_success = run_sql_script(conn, "sql/create_tables.sql")
        if not create_tables_success:
            print("ERROR: Failed to create tables!")
            return False
        
        # Load data into database
        print("Loading data into database...")
        df_clean.to_sql(
            'netflix_titles', 
            engine, 
            if_exists='replace', 
            index=False,
            method='multi'
        )
        print("Data loaded successfully into netflix_titles table.")
        
        # Create aggregated views
        print("Creating aggregated views...")
        create_views_success = run_sql_script(conn, "sql/aggregated_views.sql")
        if not create_views_success:
            print("ERROR: Failed to create views!")
            return False
        
        # Verify data was loaded
        print("Verifying data load...")
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM netflix_titles")
            row_count = cursor.fetchone()[0]
            print(f"Total rows in database: {row_count}")
            
            cursor.execute("SELECT COUNT(*) FROM v_genre_distribution")
            view_count = cursor.fetchone()[0]
            print(f"Genre distribution view rows: {view_count}")
        
        conn.close()
        print("Data loading process completed successfully!")
        return True
        
    except Exception as e:
        print(f"ERROR: Data loading failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
