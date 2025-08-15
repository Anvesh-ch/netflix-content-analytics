-- 1. Genre distribution of titles on Netflix
SELECT 
    TRIM(unnest(string_to_array(listed_in, ','))) as genre,
    COUNT(*) as title_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles), 2) as percentage
FROM netflix_titles 
WHERE listed_in IS NOT NULL
GROUP BY TRIM(unnest(string_to_array(listed_in, ',')))
ORDER BY title_count DESC;

-- 2. Number of titles released each year over time
SELECT 
    release_year,
    COUNT(*) as title_count,
    COUNT(CASE WHEN type = 'Movie' THEN 1 END) as movies,
    COUNT(CASE WHEN type = 'TV Show' THEN 1 END) as tv_shows
FROM netflix_titles 
WHERE release_year IS NOT NULL
GROUP BY release_year 
ORDER BY release_year;

-- 3. Top countries by title count
SELECT 
    TRIM(unnest(string_to_array(country, ','))) as country,
    COUNT(*) as title_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles), 2) as percentage
FROM netflix_titles 
WHERE country IS NOT NULL AND country != ''
GROUP BY TRIM(unnest(string_to_array(country, ',')))
ORDER BY title_count DESC
LIMIT 20;

-- 4. Movie durations and TV show season counts distribution
-- For Movies
SELECT 
    CASE 
        WHEN duration LIKE '%min%' THEN 
            CASE 
                WHEN CAST(REPLACE(REPLACE(duration, ' min', ''), ' ', '') AS INTEGER) < 60 THEN 'Under 1 hour'
                WHEN CAST(REPLACE(REPLACE(duration, ' min', ''), ' ', '') AS INTEGER) < 90 THEN '1-1.5 hours'
                WHEN CAST(REPLACE(REPLACE(duration, ' min', ''), ' ', '') AS INTEGER) < 120 THEN '1.5-2 hours'
                ELSE 'Over 2 hours'
            END
    END as duration_category,
    COUNT(*) as movie_count
FROM netflix_titles 
WHERE type = 'Movie' AND duration LIKE '%min%'
GROUP BY duration_category
ORDER BY movie_count DESC;

-- For TV Shows
SELECT 
    CASE 
        WHEN duration LIKE '%Season%' THEN 
            CASE 
                WHEN CAST(REPLACE(REPLACE(duration, ' Season', ''), 's', '') AS INTEGER) = 1 THEN '1 Season'
                WHEN CAST(REPLACE(REPLACE(duration, ' Season', ''), 's', '') AS INTEGER) <= 3 THEN '2-3 Seasons'
                WHEN CAST(REPLACE(REPLACE(duration, ' Season', ''), 's', '') AS INTEGER) <= 6 THEN '4-6 Seasons'
                ELSE '7+ Seasons'
            END
    END as season_category,
    COUNT(*) as show_count
FROM netflix_titles 
WHERE type = 'TV Show' AND duration LIKE '%Season%'
GROUP BY season_category
ORDER BY show_count DESC;

-- 5. Content maturity rating by genre and over time
SELECT 
    rating,
    TRIM(unnest(string_to_array(listed_in, ','))) as genre,
    release_year,
    COUNT(*) as title_count
FROM netflix_titles 
WHERE rating IS NOT NULL AND listed_in IS NOT NULL
GROUP BY rating, TRIM(unnest(string_to_array(listed_in, ','))), release_year
ORDER BY rating, genre, release_year;

-- 6. Most prolific directors and actors
-- Top Directors
SELECT 
    TRIM(unnest(string_to_array(director, ','))) as director_name,
    COUNT(*) as title_count
FROM netflix_titles 
WHERE director IS NOT NULL AND director != ''
GROUP BY TRIM(unnest(string_to_array(director, ',')))
ORDER BY title_count DESC
LIMIT 20;

-- Top Actors
SELECT 
    TRIM(unnest(string_to_array("cast", ','))) as actor_name,
    COUNT(*) as title_count
FROM netflix_titles 
WHERE cast IS NOT NULL AND cast != ''
GROUP BY TRIM(unnest(string_to_array(cast, ',')))
ORDER BY title_count DESC
LIMIT 20;

-- 7. Netflix catalog changes based on date_added
SELECT 
    EXTRACT(YEAR FROM date_added) as year_added,
    EXTRACT(MONTH FROM date_added) as month_added,
    COUNT(*) as titles_added,
    COUNT(CASE WHEN type = 'Movie' THEN 1 END) as movies_added,
    COUNT(CASE WHEN type = 'TV Show' THEN 1 END) as shows_added
FROM netflix_titles 
WHERE date_added IS NOT NULL
GROUP BY EXTRACT(YEAR FROM date_added), EXTRACT(MONTH FROM date_added)
ORDER BY year_added, month_added;
