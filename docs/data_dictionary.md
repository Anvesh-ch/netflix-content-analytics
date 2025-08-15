# Netflix Titles Dataset - Data Dictionary

## Overview
This document describes the structure and content of the Netflix titles dataset used in the Netflix Content Analytics project.

## Dataset Source
- **Source**: Kaggle - Netflix Movies and TV Shows
- **URL**: https://www.kaggle.com/datasets/shivamb/netflix-shows
- **Last Updated**: September 2021
- **Total Records**: ~8,800 titles

## Table Schema: netflix_titles

### Primary Key
- **show_id** (TEXT): Unique identifier for each title

### Content Classification
- **type** (TEXT): Content type - "Movie" or "TV Show"
- **title** (TEXT): Title of the movie or TV show
- **description** (TEXT): Brief description of the content

### Creative Team
- **director** (TEXT): Director(s) of the content (comma-separated if multiple)
- **cast** (TEXT): Main cast members (comma-separated if multiple)

### Geographic & Temporal Information
- **country** (TEXT): Country(ies) where the content was produced (comma-separated if multiple)
- **release_year** (INTEGER): Year when the content was originally released
- **date_added** (DATE): Date when the content was added to Netflix

### Content Classification
- **rating** (TEXT): Content maturity rating (e.g., TV-MA, PG-13, R)
- **duration** (TEXT): 
  - For movies: Duration in minutes (e.g., "120 min")
  - For TV shows: Number of seasons (e.g., "2 Seasons")
- **listed_in** (TEXT): Genres and categories (comma-separated)

## Data Quality Notes

### Required Fields
- show_id, title, type, release_year are required and should not contain null values

### Optional Fields
- director, cast, country, date_added, rating, duration, description may contain null values

### Data Formatting
- Multiple values in director, cast, country, and listed_in are comma-separated
- Duration format varies by content type
- Date format: YYYY-MM-DD
- Release years range from 1925 to 2021

## Aggregated Views for Power BI

### 1. v_genre_distribution
- **Purpose**: Genre analysis and distribution
- **Columns**: genre, title_count, percentage, movies, tv_shows
- **Use Case**: Genre treemap, pie charts

### 2. v_yearly_releases
- **Purpose**: Content release trends over time
- **Columns**: release_year, total_titles, movies, tv_shows, avg_movie_duration
- **Use Case**: Line charts, trend analysis

### 3. v_country_content
- **Purpose**: Geographic content distribution
- **Columns**: country, title_count, percentage, movies, tv_shows
- **Use Case**: Country maps, bar charts

### 4. v_duration_distribution
- **Purpose**: Content duration analysis
- **Columns**: content_type, duration_category, count
- **Use Case**: Histograms, distribution charts

### 5. v_ratings_analysis
- **Purpose**: Content rating analysis by genre and time
- **Columns**: rating, genre, release_year, title_count, movies, tv_shows
- **Use Case**: Heatmaps, stacked bar charts

### 6. v_top_creators
- **Purpose**: Analysis of directors and actors
- **Columns**: creator_type, creator_name, title_count, movies, tv_shows
- **Use Case**: Top N lists, creator analysis

### 7. v_content_timeline
- **Purpose**: Netflix catalog growth analysis
- **Columns**: year_added, month_added, month_name, titles_added, movies_added, shows_added, percentage_of_total
- **Use Case**: Timeline charts, growth analysis

## Data Relationships

### One-to-Many Relationships
- One title can have multiple genres (listed_in)
- One title can have multiple directors
- One title can have multiple cast members
- One title can be produced in multiple countries

### Temporal Relationships
- release_year indicates original content creation
- date_added indicates Netflix acquisition timing
- These can be used to analyze content acquisition strategies

## Business Intelligence Applications

### Content Strategy
- Genre popularity analysis
- Geographic content distribution
- Content acquisition timing analysis

### Audience Analysis
- Rating distribution analysis
- Content duration preferences
- Release year trends

### Operational Insights
- Content catalog growth
- Director/actor popularity
- Country-specific content strategies

## Data Export Format
All views are exported as CSV files in the `data/processed/bi_exports/` directory for Power BI consumption.
