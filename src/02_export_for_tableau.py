#!/usr/bin/env python3
"""
Netflix Content Analytics - Tableau Export Script
Exports database views to CSV files optimized for Tableau Public dashboard creation.
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
    """Main function to export views for Tableau."""
    print("Starting Tableau export process...")
    
    try:
        # Load configuration
        config = load_config()
        print("Configuration loaded successfully.")
        
        # Connect to database
        print("Connecting to PostgreSQL...")
        engine = get_sqlalchemy_engine(config)
        
        # Define views to export for Tableau
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
        print("\nExporting views to CSV for Tableau...")
        export_results = {}
        
        for view_name in views_to_export:
            output_path = output_dir / f"{view_name}.csv"
            success = export_view_to_csv(engine, view_name, str(output_path))
            export_results[view_name] = success
        
        # Summary
        print("\n" + "="*60)
        print("TABLEAU EXPORT SUMMARY")
        print("="*60)
        
        successful_exports = sum(export_results.values())
        total_exports = len(export_results)
        
        print(f"Successfully exported: {successful_exports}/{total_exports} views")
        
        for view_name, success in export_results.items():
            status = "✓" if success else "✗"
            print(f"{status} {view_name}")
        
        print("="*60)
        
        if successful_exports == total_exports:
            print("\nAll views exported successfully for Tableau!")
            print(f"CSV files are ready in: {output_dir}")
            print("\nNext steps for Tableau Public:")
            print("1. Download Tableau Public (free) from tableau.com")
            print("2. Open Tableau Public")
            print("3. Import the CSV files from the bi_exports directory")
            print("4. Build your dashboard following the Tableau guide")
            print("5. Publish to Tableau Public for portfolio sharing")
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
