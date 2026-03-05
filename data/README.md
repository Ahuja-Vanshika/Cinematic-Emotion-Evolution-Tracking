# Data

This folder contains raw and cleaned social media data collected for 10 movies from Reddit and Letterboxd.

## Folder Structure

Each movie has its own folder with two subfolders:

```
data/
├── MovieName/
│   ├── raw/
│   │   ├── moviename_reddit_raw.csv
│   │   └── moviename_letterboxd_raw.csv
│   └── cleaned/
│       ├── moviename_reddit_cleaned.csv
│       └── moviename_letterboxd_cleaned.csv
```

## Data Sources

| Platform | Method | Coverage |
|----------|--------|----------|
| Reddit | PRAW API | 2008 → 2026 |
| Letterboxd | Web Scraping | 2011 → 2026 |

## Movies Covered

| Movie | Release Year |
|-------|-------------|
| Titanic | 1997 |
| Shawshank Redemption | 1994 |
| The Dark Knight | 2008 |
| Parasite | 2019 |
| Interstellar | 2014 |
| La La Land | 2016 |
| Schindlers List | 1993 |
| Fight Club | 1999 |
| A Beautiful Mind | 2001 |
| Inception | 2010 |
