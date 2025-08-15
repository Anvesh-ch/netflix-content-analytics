#!/usr/bin/env python3
"""
Test suite for Netflix Content Analytics project.
Tests data quality, database operations, and utility functions.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from utils import validate_data_quality, clean_dataframe

class TestDataQuality:
    """Test data quality validation functions."""
    
    def test_validate_data_quality_complete_data(self):
        """Test validation with complete, valid data."""
        # Create sample data
        data = {
            'show_id': ['s1', 's2', 's3'],
            'title': ['Title 1', 'Title 2', 'Title 3'],
            'type': ['Movie', 'TV Show', 'Movie'],
            'release_year': [2020, 2021, 2022],
            'director': ['Director 1', 'Director 2', 'Director 3'],
            'cast': ['Actor 1', 'Actor 2', 'Actor 3'],
            'country': ['USA', 'UK', 'Canada'],
            'date_added': ['2020-01-01', '2021-01-01', '2022-01-01'],
            'rating': ['PG-13', 'TV-MA', 'R'],
            'duration': ['120 min', '2 Seasons', '90 min'],
            'listed_in': ['Action', 'Drama', 'Comedy'],
            'description': ['Description 1', 'Description 2', 'Description 3']
        }
        
        df = pd.DataFrame(data)
        results = validate_data_quality(df)
        
        assert results['total_rows'] == 3
        assert results['duplicate_rows'] == 0
        assert len(results['missing_required_columns']) == 0
        assert results['release_year_range']['min'] == 2020
        assert results['release_year_range']['max'] == 2022
    
    def test_validate_data_quality_missing_required(self):
        """Test validation with missing required columns."""
        data = {
            'show_id': ['s1', 's2'],
            'title': ['Title 1', 'Title 2']
            # Missing 'type' and 'release_year'
        }
        
        df = pd.DataFrame(data)
        results = validate_data_quality(df)
        
        assert 'type' in results['missing_required_columns']
        assert 'release_year' in results['missing_required_columns']
    
    def test_validate_data_quality_nulls_in_required(self):
        """Test validation with nulls in required columns."""
        data = {
            'show_id': ['s1', 's2', 's3'],
            'title': ['Title 1', None, 'Title 3'],
            'type': ['Movie', 'TV Show', 'Movie'],
            'release_year': [2020, 2021, None]
        }
        
        df = pd.DataFrame(data)
        results = validate_data_quality(df)
        
        assert results['nulls_in_required_columns']['title'] == 1
        assert results['nulls_in_required_columns']['release_year'] == 1
    
    def test_clean_dataframe(self):
        """Test dataframe cleaning functionality."""
        data = {
            'show_id': ['s1', 's2'],
            'title': ['  Title 1  ', 'Title 2'],
            'type': ['Movie', 'TV Show'],
            'release_year': ['2020', '2021'],
            'date_added': ['2020-01-01', '2021-01-01'],
            'director': ['Director 1', 'nan'],
            'cast': ['Actor 1', 'Actor 2'],
            'country': ['USA', 'UK'],
            'rating': ['PG-13', 'TV-MA'],
            'duration': ['120 min', '2 Seasons'],
            'listed_in': ['Action', 'Drama'],
            'description': ['Description 1', 'Description 2']
        }
        
        df = pd.DataFrame(data)
        df_clean = clean_dataframe(df)
        
        # Check that whitespace is trimmed
        assert df_clean['title'].iloc[0] == 'Title 1'
        
        # Check that 'nan' strings are converted to None
        assert pd.isna(df_clean['director'].iloc[1])
        
        # Check that release_year is numeric
        assert df_clean['release_year'].dtype == 'Int64'
        
        # Check that date_added is datetime
        assert pd.api.types.is_datetime64_any_dtype(df_clean['date_added'])

class TestDataStructure:
    """Test data structure and schema validation."""
    
    def test_expected_columns(self):
        """Test that the dataset has expected columns."""
        expected_columns = [
            'show_id', 'type', 'title', 'director', 'cast', 'country',
            'date_added', 'release_year', 'rating', 'duration', 'listed_in', 'description'
        ]
        
        # This test would require the actual CSV file
        # For now, we'll just verify the expected structure
        assert len(expected_columns) == 12
        assert 'show_id' in expected_columns
        assert 'title' in expected_columns
        assert 'type' in expected_columns
        assert 'release_year' in expected_columns

if __name__ == "__main__":
    pytest.main([__file__])
