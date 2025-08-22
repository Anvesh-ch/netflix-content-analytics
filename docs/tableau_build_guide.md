# Tableau Public Dashboard Build Guide

## Overview
This guide provides step-by-step instructions for building a comprehensive Netflix Content Analytics dashboard using Tableau Public and the exported CSV data from our PostgreSQL analysis.

## Prerequisites
- Tableau Public (free download from [tableau.com](https://www.tableau.com/products/public))
- CSV export files from the `data/processed/bi_exports/` directory
- Basic familiarity with Tableau interface

## Dashboard Structure
The dashboard will consist of 7 main visualizations answering key business questions about Netflix content.

## Step-by-Step Build Process

### Step 1: Download and Install Tableau Public
1. Go to [tableau.com/products/public](https://www.tableau.com/products/public)
2. Click "Download Tableau Public"
3. Install the application on your Mac
4. Launch Tableau Public

### Step 2: Import Data Sources
1. Open Tableau Public
2. Click "Connect to Data" → "Text file"
3. Import the following CSV files:
   - `v_genre_distribution.csv`
   - `v_yearly_releases.csv`
   - `v_country_content.csv`
   - `v_duration_distribution.csv`
   - `v_ratings_analysis.csv`
   - `v_top_creators.csv`
   - `v_content_timeline.csv`

### Step 3: Data Model Setup
1. Go to "Data Source" view
2. Ensure all tables are properly connected
3. Set appropriate data types:
   - `release_year` and `year_added` as Number (Whole)
   - `title_count`, `movies`, `tv_shows` as Number (Whole)
   - `percentage` as Number (Decimal)
   - All other fields as String

### Step 4: Create Dashboard Layout

#### Page 1: Content Overview
**Layout**: 2x2 grid

1. **Genre Distribution Treemap**
   - Data: `v_genre_distribution`
   - Marks: Treemap
   - Size: `title_count`
   - Color: `genre`
   - Tooltip: `percentage`, `movies`, `tv_shows`

2. **Content Type Distribution**
   - Data: `v_genre_distribution` (aggregated)
   - Marks: Pie Chart
   - Values: Sum of `movies` vs Sum of `tv_shows`
   - Color: Content Type

3. **Top Countries Bar Chart**
   - Data: `v_country_content`
   - Marks: Bar Chart
   - Columns: `country` (top 10)
   - Rows: `title_count`
   - Sort: Descending by `title_count`

4. **Content Ratings Distribution**
   - Data: `v_ratings_analysis` (aggregated)
   - Marks: Bar Chart
   - Columns: `rating`
   - Rows: Sum of `title_count`

#### Page 2: Temporal Analysis
**Layout**: 2x2 grid

1. **Yearly Release Trends**
   - Data: `v_yearly_releases`
   - Marks: Line Chart
   - Columns: `release_year`
   - Rows: `total_titles`, `movies`, `tv_shows`
   - Color: Content Type

2. **Content Addition Timeline**
   - Data: `v_content_timeline`
   - Marks: Area Chart
   - Columns: `year_added`
   - Rows: `titles_added`
   - Secondary axis: `percentage_of_total`

3. **Monthly Addition Patterns**
   - Data: `v_content_timeline`
   - Marks: Bar Chart
   - Columns: `month_name`
   - Rows: `titles_added`
   - Sort: By month order

4. **Release Year vs Addition Year**
   - Data: `v_yearly_releases` + `v_content_timeline`
   - Marks: Scatter Plot
   - Columns: `release_year`
   - Rows: `year_added`
   - Size: `total_titles`

#### Page 3: Content Analysis
**Layout**: 2x2 grid

1. **Duration Distribution**
   - Data: `v_duration_distribution`
   - Marks: Clustered Bar Chart
   - Columns: `duration_category`
   - Rows: `count`
   - Color: `content_type`

2. **Genre-Rating Heatmap**
   - Data: `v_ratings_analysis`
   - Marks: Heatmap
   - Columns: `rating`
   - Rows: `genre` (top 15)
   - Color: `title_count`

3. **Top Directors**
   - Data: `v_top_creators` (filtered by `creator_type = 'Director'`)
   - Marks: Bar Chart
   - Columns: `creator_name` (top 10)
   - Rows: `title_count`
   - Sort: Descending

4. **Top Actors**
   - Data: `v_top_creators` (filtered by `creator_type = 'Actor'`)
   - Marks: Bar Chart
   - Columns: `creator_name` (top 10)
   - Rows: `title_count`
   - Sort: Descending

#### Page 4: Interactive Dashboard
**Layout**: 3x3 grid with filters

1. **Main KPI Cards** (top row)
   - Total Titles
   - Total Movies
   - Total TV Shows
   - Average Release Year
   - Most Popular Genre

2. **Interactive Filters** (left column)
   - Year Range Slider
   - Content Type Filter
   - Rating Filter
   - Country Filter

3. **Dynamic Visualizations** (center/right)
   - Genre Distribution (filtered by selections)
   - Country Map (if available)
   - Timeline Chart
   - Creator Analysis

### Step 5: Add Interactivity

#### Filters
- Create global filters for year, content type, rating, and country
- Apply filters to all relevant visualizations
- Test filter interactions

#### Actions
- Set up highlight actions between related charts
- Create URL actions for external links
- Add parameter controls for dynamic analysis

#### Tooltips
- Customize tooltips with relevant information
- Add calculated fields for enhanced insights
- Include data source information

### Step 6: Formatting and Styling

#### Color Scheme
- Use consistent color palette throughout
- Apply Netflix brand colors where appropriate
- Ensure accessibility (colorblind-friendly)

#### Typography
- Use clear, readable fonts
- Consistent heading hierarchy
- Appropriate font sizes for different visual types

#### Layout
- Consistent spacing and alignment
- Proper visual hierarchy
- Responsive design considerations

### Step 7: Add Calculated Fields

#### Key Performance Indicators
```
Total Titles = SUM([title_count])
Total Movies = SUM([movies])
Total TV Shows = SUM([tv_shows])
Average Release Year = AVG([release_year])
```

#### Percentage Calculations
```
Movie Percentage = [Total Movies] / [Total Titles]
TV Show Percentage = [Total TV Shows] / [Total Titles]
```

#### Growth Metrics
```
Year over Year Growth = 
IF [Year Added] = MAX([Year Added]) THEN
    ([Titles Added] - LOOKUP([Titles Added], -1)) / LOOKUP([Titles Added], -1)
ELSE NULL
END
```

### Step 8: Testing and Validation

#### Data Validation
- Verify all CSV data is properly imported
- Check for data type consistency
- Validate calculated fields

#### User Experience Testing
- Test all filter interactions
- Verify highlight actions
- Check performance with large datasets

#### Cross-Platform Testing
- Test on different screen sizes
- Verify mobile compatibility
- Check Tableau Public deployment

### Step 9: Finalization

#### Documentation
- Add tooltips to all visualizations
- Include data source information
- Add usage instructions

#### Performance Optimization
- Optimize calculated fields
- Reduce visual complexity if needed
- Test refresh performance

#### Export and Sharing
- Save as `.twbx` file
- Publish to Tableau Public
- Share via web link

## Dashboard Features Summary

### Visualizations
- **7 main analysis areas** with multiple chart types
- **Interactive filters** for dynamic analysis
- **Cross-filtering** between all components
- **Highlight actions** for detailed analysis

### Key Insights
- Genre popularity and distribution
- Temporal content trends
- Geographic content analysis
- Creator and rating analysis
- Content acquisition patterns

### Business Value
- Content strategy insights
- Audience preference analysis
- Operational performance metrics
- Strategic decision support

## Publishing to Tableau Public

### Step 1: Save Your Work
1. Save your dashboard as `.twbx` file
2. Ensure all data sources are included
3. Test all functionality

### Step 2: Publish to Tableau Public
1. Click "Server" → "Tableau Public" → "Save to Tableau Public"
2. Sign in to your Tableau Public account
3. Add title: "Netflix Content Analytics Dashboard"
4. Add description: "Comprehensive analysis of Netflix's global content library"
5. Add tags: "Netflix", "Content Analytics", "Data Visualization"
6. Click "Save"

### Step 3: Share Your Dashboard
1. Copy the public URL
2. Add to your portfolio/resume
3. Share on LinkedIn or other professional networks
4. Include in job applications

## Troubleshooting

### Common Issues
1. **Data Import Errors**: Check CSV file paths and formats
2. **Relationship Errors**: Verify data model connections
3. **Performance Issues**: Optimize calculated fields and reduce visual complexity
4. **Filter Problems**: Check filter settings and relationships

### Best Practices
- Use consistent naming conventions
- Implement proper error handling in calculated fields
- Test with sample data before full deployment
- Document all custom calculations and filters

## Next Steps
After building the dashboard:
1. Share with stakeholders for feedback
2. Iterate based on user requirements
3. Schedule regular data refreshes
4. Plan for additional analysis features
5. Consider Tableau Server deployment for collaboration

## Success Metrics

### Technical Success
- [ ] All CSV data imports correctly
- [ ] Dashboard loads all visualizations
- [ ] Filters and interactions work properly
- [ ] Performance is acceptable

### Analysis Success
- [ ] Key business questions are answered
- [ ] Insights are actionable and meaningful
- [ ] Dashboard provides value to users
- [ ] Analysis reveals unexpected patterns

### Business Success
- [ ] Dashboard supports decision-making
- [ ] Analysis provides competitive insights
- [ ] Project demonstrates technical capabilities
- [ ] Results can be presented to stakeholders

## Conclusion

This Tableau Public dashboard provides a solid foundation for Netflix content analysis while offering professional-grade visualization capabilities. The interactive features and public sharing make it an excellent portfolio piece that demonstrates both technical skills and business acumen.

Key success factors include:
1. **Data Quality**: Ensuring reliable data import and validation
2. **Performance**: Optimizing visualizations and calculations
3. **Usability**: Creating intuitive and valuable dashboard experience
4. **Documentation**: Maintaining clear understanding of capabilities and limitations

By following this guide, you'll create a professional Netflix analytics dashboard that showcases your data visualization skills and provides valuable business insights.
