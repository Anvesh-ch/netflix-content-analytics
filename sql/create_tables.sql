-- Create netflix_titles table
CREATE TABLE IF NOT EXISTS netflix_titles (
    show_id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    director TEXT,
    "cast" TEXT,
    country TEXT,
    date_added DATE,
    release_year INTEGER NOT NULL,
    rating TEXT,
    duration TEXT,
    listed_in TEXT,
    description TEXT
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_netflix_titles_type ON netflix_titles(type);
CREATE INDEX IF NOT EXISTS idx_netflix_titles_release_year ON netflix_titles(release_year);
CREATE INDEX IF NOT EXISTS idx_netflix_titles_country ON netflix_titles(country);
CREATE INDEX IF NOT EXISTS idx_netflix_titles_rating ON netflix_titles(rating);
CREATE INDEX IF NOT EXISTS idx_netflix_titles_date_added ON netflix_titles(date_added);
CREATE INDEX IF NOT EXISTS idx_netflix_titles_listed_in ON netflix_titles(listed_in);
