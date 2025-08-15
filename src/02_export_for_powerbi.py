#!/usr/bin/env python3
"""
Netflix Content Analytics - Power BI Export Script
Exports database views to CSV files for Power BI dashboard creation.
"""

import sys
import os
import pandas as pd
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from utils import (
    load_config, 
    get_sqlalchemy_engine,
    export_view_to_csv
)

def main():
    """Main function to export views for Power BI."""
    print("Starting Power BI export process...")
    
    try:
        # Load configuration
        config = load_config()
        print("Configuration loaded successfully.")
        
        # Connect to database
        print("Connecting to PostgreSQL...")
        engine = get_sqlalchemy_engine(config)
        
        # Define views to export
        views_to_export = [
            "v_genre_distribution",
            "v_yearly_releases", 
            "v_country_content",
            "v_duration_distribution",
            "v_ratings_analysis",
            "v_top_creators",
            "v_content_timeline"
        ]
        
        # Create output directory
        output_dir = Path(config['data']['bi_exports_dir'])
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Export directory: {output_dir}")
        
        # Export each view
        print("\nExporting views to CSV...")
        export_results = {}
        
        for view_name in views_to_export:
            output_path = output_dir / f"{view_name}.csv"
            success = export_view_to_csv(engine, view_name, str(output_path))
            export_results[view_name] = success
        
        # Summary
        print("\n" + "="*60)
        print("EXPORT SUMMARY")
        print("="*60)
        
        successful_exports = sum(export_results.values())
        total_exports = len(export_results)
        
        print(f"Successfully exported: {successful_exports}/{total_exports} views")
        
        for view_name, success in export_results.items():
            status = "✓" if success else "✗"
            print(f"{status} {view_name}")
        
        print("="*60)
        
        if successful_exports == total_exports:
            print("\nAll views exported successfully!")
            print(f"CSV files are ready in: {output_dir}")
            print("\nNext steps:")
            print("1. Open Power BI Desktop")
            print("2. Import the CSV files from the bi_exports directory")
            print("3. Build your dashboard using the data")
            print("4. Save as .pbix file in the docs directory")
        else:
            print(f"\nWARNING: {total_exports - successful_exports} exports failed!")
            return False
        
        return True
        
    except Exception as e:
        print(f"ERROR: Export failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
