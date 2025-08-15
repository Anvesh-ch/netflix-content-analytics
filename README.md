# Netflix Content Analytics

A comprehensive data analytics project that analyzes Netflix's global content library to identify genre trends, rating distributions, and release patterns. Built with PostgreSQL, Python, and Power BI for strategic content insights.

## Project Overview

This project provides an end-to-end solution for analyzing Netflix content data, from raw CSV ingestion to interactive Power BI dashboards. It answers key business questions about content strategy, audience preferences, and operational performance.

### Key Features
- **Data Pipeline**: Automated loading of Netflix titles dataset into PostgreSQL
- **SQL Analysis**: Comprehensive content analysis using advanced SQL queries
- **Power BI Dashboard**: Interactive visualizations for strategic insights
- **Data Quality**: Robust validation and cleaning processes
- **Reproducible**: Complete automation from data to insights

## Business Questions Answered

1. **What is the genre distribution of titles on Netflix?**
2. **How has the number of titles released each year evolved over time?**
3. **Which countries produce the most Netflix content?**
4. **How are movie durations and TV show season counts distributed?**
5. **How does content maturity rating vary by genre and over time?**
6. **Who are the most prolific directors and actors on Netflix?**
7. **How has Netflix's catalog changed based on the date_added field?**

## Tech Stack

- **Python 3.11**: Data processing and automation
- **PostgreSQL 15**: Data storage and analysis
- **Docker**: Containerized database setup
- **Power BI**: Interactive dashboard creation
- **Pandas & SQLAlchemy**: Data manipulation and database operations
- **PyTest**: Testing and validation

## Quick Start

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Power BI Desktop (for dashboard creation)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd netflix-content-analytics
pip install -r requirements.txt
```

### 2. Start PostgreSQL Database
```bash
docker-compose up -d
```

### 3. Load Data and Run Analysis
```bash
# Load Netflix data into PostgreSQL
python src/00_load_to_postgres.py

# Run content analysis
python src/01_run_analysis.py

# Export data for Power BI
python src/02_export_for_powerbi.py
```

### 4. Build Power BI Dashboard
1. Open Power BI Desktop
2. Import CSV files from `data/processed/bi_exports/`
3. Follow the build guide in `docs/powerbi_build_guide.md`
4. Save dashboard as `.pbix` file

## Project Structure

```
netflix-content-analytics/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # PostgreSQL setup
├── configs/
│   └── config.yaml          # Configuration settings
├── data/
│   ├── raw/
│   │   └── netflix_titles.csv    # Source dataset
│   └── processed/
│       └── bi_exports/           # CSV exports for Power BI
├── notebooks/
│   ├── 00_data_exploration.ipynb    # Initial data analysis
│   └── 01_sql_analysis.ipynb        # SQL query exploration
├── sql/
│   ├── create_tables.sql     # Database schema
│   ├── analysis_queries.sql  # Analysis queries
│   └── aggregated_views.sql  # Power BI views
├── src/
│   ├── __init__.py
│   ├── 00_load_to_postgres.py    # Data loading script
│   ├── 01_run_analysis.py        # Analysis execution
│   ├── 02_export_for_powerbi.py  # Power BI export
│   └── utils.py                   # Utility functions
├── tests/
│   └── test_data_quality.py      # Data quality tests
└── docs/
    ├── powerbi_build_guide.md    # Dashboard creation guide
    ├── data_dictionary.md         # Dataset documentation
    └── assumptions.md             # Project assumptions
```

## Data Pipeline

### 1. Data Ingestion
- **Source**: Kaggle Netflix Movies and TV Shows dataset
- **Format**: CSV with ~8,800 titles
- **Validation**: Data quality checks and cleaning
- **Storage**: PostgreSQL with optimized schema

### 2. Data Processing
- **Cleaning**: Handle missing values and format inconsistencies
- **Transformation**: Convert data types and standardize formats
- **Validation**: Ensure data integrity and completeness

### 3. Analysis
- **SQL Queries**: Advanced analytics using PostgreSQL features
- **Aggregated Views**: Pre-calculated metrics for Power BI
- **Insights**: Key trends and patterns identification

### 4. Visualization
- **CSV Export**: Structured data for Power BI consumption
- **Dashboard**: Interactive visualizations and filters
- **Insights**: Actionable business intelligence

## Database Schema

### Main Table: netflix_titles
| Column | Type | Description |
|--------|------|-------------|
| show_id | TEXT | Unique identifier (Primary Key) |
| type | TEXT | Content type (Movie/TV Show) |
| title | TEXT | Title of the content |
| director | TEXT | Director(s) of the content |
| cast | TEXT | Main cast members |
| country | TEXT | Production country(ies) |
| date_added | DATE | Date added to Netflix |
| release_year | INTEGER | Original release year |
| rating | TEXT | Content maturity rating |
| duration | TEXT | Duration (minutes/seasons) |
| listed_in | TEXT | Genres and categories |
| description | TEXT | Content description |

### Aggregated Views
- **v_genre_distribution**: Genre popularity analysis
- **v_yearly_releases**: Temporal content trends
- **v_country_content**: Geographic distribution
- **v_duration_distribution**: Content length analysis
- **v_ratings_analysis**: Rating patterns by genre
- **v_top_creators**: Director and actor analysis
- **v_content_timeline**: Netflix catalog growth

## Analysis Capabilities

### Content Strategy Insights
- Genre popularity and trends
- Geographic content distribution
- Content acquisition timing
- Rating strategy analysis

### Operational Metrics
- Content catalog growth
- Release year distribution
- Duration optimization
- Creator relationships

### Audience Analysis
- Content type preferences
- Rating distribution
- Temporal viewing patterns
- Geographic preferences

## Power BI Dashboard

### Dashboard Pages
1. **Content Overview**: Genre distribution, content types, top countries
2. **Temporal Analysis**: Release trends, addition timeline, monthly patterns
3. **Content Analysis**: Duration distribution, ratings, top creators
4. **Interactive Dashboard**: KPI cards, filters, dynamic visualizations

### Key Visualizations
- Genre distribution treemap
- Yearly release trend lines
- Country-content heatmap
- Ratings distribution charts
- Duration histograms
- Creator top-10 lists
- Content addition timeline

## Testing

Run the test suite to validate data quality and functionality:

```bash
pytest tests/
```

Tests cover:
- Data quality validation
- Data cleaning functions
- Database operations
- Export functionality

## Configuration

Edit `configs/config.yaml` to customize:
- Database connection settings
- File paths and directories
- Analysis parameters
- Export options

## Troubleshooting

### Common Issues
1. **Database Connection**: Ensure Docker is running and PostgreSQL is accessible
2. **Data Loading**: Check CSV file path and database permissions
3. **Power BI Import**: Verify CSV file formats and data types
4. **Performance**: Optimize database queries for large datasets

### Getting Help
- Check the documentation in the `docs/` directory
- Review error messages in the console output
- Validate data quality using the test suite
- Consult the assumptions document for limitations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is for educational and portfolio purposes. The Netflix dataset is sourced from Kaggle and subject to their terms of use.

## Portfolio Value

This project demonstrates:
- **Data Engineering**: ETL pipelines, database design, data quality
- **Data Analysis**: SQL analytics, statistical analysis, business insights
- **Data Visualization**: Power BI dashboards, interactive analytics
- **Project Management**: Documentation, testing, reproducible workflows
- **Technical Skills**: Python, PostgreSQL, Docker, Power BI

## Next Steps

1. **Deploy to Production**: Set up automated data refresh processes
2. **Enhanced Analytics**: Add machine learning and predictive modeling
3. **Real-time Updates**: Implement live database connections
4. **Additional Sources**: Integrate viewership and rating data
5. **Advanced Visualizations**: Create custom Power BI visuals

## Contact

For questions or feedback about this project, please open an issue in the repository.

---

**Note**: This project analyzes publicly available Netflix content data for educational purposes. It does not represent official Netflix analytics or business intelligence.
