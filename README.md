# Netflix Titles - Data Cleaning, Analysis & Visualization

This project looks at the Netflix Titles dataset (~8,800 movies and TV shows) and works through it in three stages: cleaning the raw data, analyzing it for patterns, and visualizing the results.

## Dataset

`netflix_titles.csv` — one row per title, with columns for type (Movie/TV Show), title, director, cast, country, date added to Netflix, release year, rating, duration, and genre.

## 1. Data Cleaning

The raw file had duplicates and a fair number of missing values, so before doing anything else I:

- Dropped duplicate rows
- Filled missing `director`, `cast`, and `country` values with "Unknown" instead of dropping them (too much data to throw away)
- Dropped the small number of rows missing `date_added` or `rating`
- Cleaned up column names (lowercase, underscores instead of spaces) and renamed `show_id` → `id` and `listed_in` → `genre`
- Dropped the `description` column since it wasn't needed for analysis

Raw dataset: 8,807 rows. After cleaning: 8,793 rows.

## 2. Data Analysis

Some of the things I pulled out of the cleaned data:

- **6,129 movies** vs **2,664 TV shows**
- Longest movie: *Black Mirror: Bandersnatch* (312 min)
- Shortest movie: *Silent* (3 min)
- TV show with the most seasons: *Grey's Anatomy* (17 seasons)
- Average movie length: ~99.6 minutes
- Average number of seasons per TV show: ~1.75
- Top countries producing content: United States, India, United Kingdom, Canada
- Most common genres: International Movies, Dramas, Comedies, International TV Shows, Documentaries
- Correlation between release year and duration was weak for both movies (-0.21) and TV shows (-0.08) — newer titles aren't really longer or shorter than older ones
- Looked at how many titles were added to Netflix per year and per month to see growth trends over time

## 3. Data Visualization

Built charts to make the analysis easier to read at a glance:

- Bar chart comparing number of movies vs TV shows
- Pie chart showing the split between movies and TV shows
- Line chart of titles added to Netflix per year
- Histogram of release years to see when most content was made
- Correlation heatmap across the numeric columns

## Tools used

- Python
- Pandas / NumPy for cleaning and analysis
- Matplotlib / Seaborn for the charts
- Streamlit to bring it all together into one interactive app

## Live demo

[INSERT YOUR LIVE STREAMLIT URL HERE]

## Files

```
app.py                  # combines all three stages into one app
requirements.txt        # dependencies
netflix_titles.csv      # the dataset
screenshots/            # screenshots of the app
```
