-- Create views for Power BI consumption

-- 1. Genre Distribution View
CREATE OR REPLACE VIEW v_genre_distribution AS
SELECT 
    TRIM(unnest(string_to_array(listed_in, ','))) as genre,
    COUNT(*) as title_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles), 2) as percentage,
    COUNT(CASE WHEN type = 'Movie' THEN 1 END) as movies,
    COUNT(CASE WHEN type = 'TV Show' THEN 1 END) as tv_shows
FROM netflix_titles 
WHERE listed_in IS NOT NULL
GROUP BY TRIM(unnest(string_to_array(listed_in, ',')))
ORDER BY title_count DESC;

-- 2. Yearly Release Trends View
CREATE OR REPLACE VIEW v_yearly_releases AS
SELECT 
    release_year,
    COUNT(*) as total_titles,
    COUNT(CASE WHEN type = 'Movie' THEN 1 END) as movies,
    COUNT(CASE WHEN type = 'TV Show' THEN 1 END) as tv_shows,
    ROUND(AVG(CASE WHEN type = 'Movie' AND duration LIKE '%min%' 
        THEN CAST(REPLACE(REPLACE(duration, ' min', ''), ' ', '') AS INTEGER) END), 2) as avg_movie_duration
FROM netflix_titles 
WHERE release_year IS NOT NULL
GROUP BY release_year 
ORDER BY release_year;

-- 3. Country Content View
CREATE OR REPLACE VIEW v_country_content AS
SELECT 
    TRIM(unnest(string_to_array(country, ','))) as country,
    COUNT(*) as title_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles), 2) as percentage,
    COUNT(CASE WHEN type = 'Movie' THEN 1 END) as movies,
    COUNT(CASE WHEN type = 'TV Show' THEN 1 END) as tv_shows
FROM netflix_titles 
WHERE country IS NOT NULL AND country != ''
GROUP BY TRIM(unnest(string_to_array(country, ',')))
ORDER BY title_count DESC;

-- 4. Duration Distribution View
CREATE OR REPLACE VIEW v_duration_distribution AS
SELECT 
    'Movie' as content_type,
    CASE 
        WHEN duration LIKE '%min%' THEN 
            CASE 
                WHEN CAST(REPLACE(REPLACE(duration, ' min', ''), ' ', '') AS INTEGER) < 60 THEN 'Under 1 hour'
                WHEN CAST(REPLACE(REPLACE(duration, ' min', ''), ' ', '') AS INTEGER) < 90 THEN '1-1.5 hours'
                WHEN CAST(REPLACE(REPLACE(duration, ' min', ''), ' ', '') AS INTEGER) < 120 THEN '1.5-2 hours'
                ELSE 'Over 2 hours'
            END
    END as duration_category,
    COUNT(*) as count
FROM netflix_titles 
WHERE type = 'Movie' AND duration LIKE '%min%'
GROUP BY duration_category

UNION ALL

SELECT 
    'TV Show' as content_type,
    CASE 
        WHEN duration LIKE '%Season%' THEN 
            CASE 
                WHEN CAST(REPLACE(REPLACE(duration, ' Season', ''), 's', '') AS INTEGER) = 1 THEN '1 Season'
                WHEN CAST(REPLACE(REPLACE(duration, ' Season', ''), 's', '') AS INTEGER) <= 3 THEN '2-3 Seasons'
                WHEN CAST(REPLACE(REPLACE(duration, ' Season', ''), 's', '') AS INTEGER) <= 6 THEN '4-6 Seasons'
                ELSE '7+ Seasons'
            END
    END as duration_category,
    COUNT(*) as count
FROM netflix_titles 
WHERE type = 'TV Show' AND duration LIKE '%Season%'
GROUP BY duration_category
ORDER BY content_type, count DESC;

-- 5. Ratings Analysis View
CREATE OR REPLACE VIEW v_ratings_analysis AS
SELECT 
    rating,
    TRIM(unnest(string_to_array(listed_in, ','))) as genre,
    release_year,
    COUNT(*) as title_count,
    COUNT(CASE WHEN type = 'Movie' THEN 1 END) as movies,
    COUNT(CASE WHEN type = 'TV Show' THEN 1 END) as tv_shows
FROM netflix_titles 
WHERE rating IS NOT NULL AND listed_in IS NOT NULL
GROUP BY rating, TRIM(unnest(string_to_array(listed_in, ','))), release_year
ORDER BY rating, genre, release_year;

-- 6. Top Creators View
CREATE OR REPLACE VIEW v_top_creators AS
SELECT 
    'Director' as creator_type,
    TRIM(unnest(string_to_array(director, ','))) as creator_name,
    COUNT(*) as title_count,
    COUNT(CASE WHEN type = 'Movie' THEN 1 END) as movies,
    COUNT(CASE WHEN type = 'TV Show' THEN 1 END) as tv_shows
FROM netflix_titles 
WHERE director IS NOT NULL AND director != ''
GROUP BY TRIM(unnest(string_to_array(director, ',')))

UNION ALL

SELECT 
    'Actor' as creator_type,
    TRIM(unnest(string_to_array("cast", ','))) as creator_name,
    COUNT(*) as title_count,
    COUNT(CASE WHEN type = 'Movie' THEN 1 END) as movies,
    COUNT(CASE WHEN type = 'TV Show' THEN 1 END) as tv_shows
FROM netflix_titles 
WHERE "cast" IS NOT NULL AND "cast" != ''
GROUP BY TRIM(unnest(string_to_array("cast", ',')))
ORDER BY creator_type, title_count DESC;

-- 7. Content Addition Timeline View
CREATE OR REPLACE VIEW v_content_timeline AS
SELECT 
    EXTRACT(YEAR FROM date_added) as year_added,
    EXTRACT(MONTH FROM date_added) as month_added,
    TO_CHAR(date_added, 'Month') as month_name,
    COUNT(*) as titles_added,
    COUNT(CASE WHEN type = 'Movie' THEN 1 END) as movies_added,
    COUNT(CASE WHEN type = 'TV Show' THEN 1 END) as shows_added,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles WHERE date_added IS NOT NULL), 2) as percentage_of_total
FROM netflix_titles 
WHERE date_added IS NOT NULL
GROUP BY EXTRACT(YEAR FROM date_added), EXTRACT(MONTH FROM date_added), TO_CHAR(date_added, 'Month')
ORDER BY year_added, month_added;
