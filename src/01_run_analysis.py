#!/usr/bin/env python3
"""
Netflix Content Analytics - Analysis Script
Runs SQL analysis queries and generates insights from the Netflix dataset.
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
    get_sqlalchemy_engine
)

def run_analysis_query(conn, query_name: str, query: str) -> pd.DataFrame:
    """Run an analysis query and return results as DataFrame."""
    try:
        df = pd.read_sql(query, conn)
        print(f"✓ {query_name}: {len(df)} rows returned")
        return df
    except Exception as e:
        print(f"✗ {query_name}: Failed - {e}")
        return pd.DataFrame()

def main():
    """Main function to run Netflix content analysis."""
    print("Starting Netflix content analysis...")
    
    try:
        # Load configuration
        config = load_config()
        print("Configuration loaded successfully.")
        
        # Connect to database
        print("Connecting to PostgreSQL...")
        conn = get_database_connection(config)
        engine = get_sqlalchemy_engine(config)
        
        # Define analysis queries
        analysis_queries = {
            "Genre Distribution": """
                SELECT 
                    TRIM(unnest(string_to_array(listed_in, ','))) as genre,
                    COUNT(*) as title_count,
                    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles), 2) as percentage
                FROM netflix_titles 
                WHERE listed_in IS NOT NULL
                GROUP BY TRIM(unnest(string_to_array(listed_in, ',')))
                ORDER BY title_count DESC
                LIMIT 20;
            """,
            
            "Yearly Release Trends": """
                SELECT 
                    release_year,
                    COUNT(*) as total_titles,
                    COUNT(CASE WHEN type = 'Movie' THEN 1 END) as movies,
                    COUNT(CASE WHEN type = 'TV Show' THEN 1 END) as tv_shows
                FROM netflix_titles 
                WHERE release_year IS NOT NULL
                GROUP BY release_year 
                ORDER BY release_year;
            """,
            
            "Top Countries": """
                SELECT 
                    TRIM(unnest(string_to_array(country, ','))) as country,
                    COUNT(*) as title_count,
                    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles), 2) as percentage
                FROM netflix_titles 
                WHERE country IS NOT NULL AND country != ''
                GROUP BY TRIM(unnest(string_to_array(country, ',')))
                ORDER BY title_count DESC
                LIMIT 15;
            """,
            
            "Content Ratings": """
                SELECT 
                    rating,
                    COUNT(*) as title_count,
                    COUNT(CASE WHEN type = 'Movie' THEN 1 END) as movies,
                    COUNT(CASE WHEN type = 'TV Show' THEN 1 END) as tv_shows
                FROM netflix_titles 
                WHERE rating IS NOT NULL
                GROUP BY rating
                ORDER BY title_count DESC;
            """,
            
            "Top Directors": """
                SELECT 
                    TRIM(unnest(string_to_array(director, ','))) as director_name,
                    COUNT(*) as title_count
                FROM netflix_titles 
                WHERE director IS NOT NULL AND director != ''
                GROUP BY TRIM(unnest(string_to_array(director, ',')))
                ORDER BY title_count DESC
                LIMIT 15;
            """,
            
            "Top Actors": """
                SELECT 
                    TRIM(unnest(string_to_array(cast, ','))) as actor_name,
                    COUNT(*) as title_count
                FROM netflix_titles 
                WHERE cast IS NOT NULL AND cast != ''
                GROUP BY TRIM(unnest(string_to_array(cast, ',')))
                ORDER BY title_count DESC
                LIMIT 15;
            """,
            
            "Content Addition Timeline": """
                SELECT 
                    EXTRACT(YEAR FROM date_added) as year_added,
                    COUNT(*) as titles_added
                FROM netflix_titles 
                WHERE date_added IS NOT NULL
                GROUP BY EXTRACT(YEAR FROM date_added)
                ORDER BY year_added;
            """
        }
        
        # Run all analysis queries
        print("\nRunning analysis queries...")
        results = {}
        
        for query_name, query in analysis_queries.items():
            results[query_name] = run_analysis_query(engine, query_name, query)
        
        # Generate summary insights
        print("\n" + "="*60)
        print("ANALYSIS SUMMARY")
        print("="*60)
        
        # Genre insights
        if not results["Genre Distribution"].empty:
            top_genre = results["Genre Distribution"].iloc[0]
            print(f"Top Genre: {top_genre['genre']} ({top_genre['title_count']} titles, {top_genre['percentage']}%)")
        
        # Year insights
        if not results["Yearly Release Trends"].empty:
            recent_year = results["Yearly Release Trends"].iloc[-1]
            print(f"Most Recent Year: {recent_year['release_year']} ({recent_year['total_titles']} titles)")
        
        # Country insights
        if not results["Top Countries"].empty:
            top_country = results["Top Countries"].iloc[0]
            print(f"Top Content Producer: {top_country['country']} ({top_country['title_count']} titles)")
        
        # Rating insights
        if not results["Content Ratings"].empty:
            top_rating = results["Content Ratings"].iloc[0]
            print(f"Most Common Rating: {top_rating['rating']} ({top_rating['title_count']} titles)")
        
        # Creator insights
        if not results["Top Directors"].empty:
            top_director = results["Top Directors"].iloc[0]
            print(f"Top Director: {top_director['director_name']} ({top_director['title_count']} titles)")
        
        if not results["Top Actors"].empty:
            top_actor = results["Top Actors"].iloc[0]
            print(f"Top Actor: {top_actor['actor_name']} ({top_actor['title_count']} titles)")
        
        # Content addition insights
        if not results["Content Addition Timeline"].empty:
            recent_addition = results["Content Addition Timeline"].iloc[-1]
            print(f"Most Recent Addition Year: {recent_addition['year_added']} ({recent_addition['titles_added']} titles added)")
        
        print("="*60)
        
        # Save results to CSV for further analysis
        output_dir = Path(config['data']['processed_dir'])
        output_dir.mkdir(exist_ok=True)
        
        for query_name, df in results.items():
            if not df.empty:
                filename = f"{query_name.lower().replace(' ', '_')}.csv"
                output_path = output_dir / filename
                df.to_csv(output_path, index=False)
                print(f"Saved {query_name} results to: {output_path}")
        
        conn.close()
        print("\nAnalysis completed successfully!")
        return True
        
    except Exception as e:
        print(f"ERROR: Analysis failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
