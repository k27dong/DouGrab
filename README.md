# DouGrab

**D**ouGrab **O**btains **U**ser's **G**raded **R**eviews **a**nd **B**its

## Overview
This repository contains two Python scripts that allow you to scrape movie reviews from a user's Douban account and visualize them in an HTML format.

1. `dougrab.py`: Scrapes movie reviews from Douban for a given user and saves the data in a JSON file.
2. `visualize.py`: Converts the JSON data of movie reviews into an HTML file for easy viewing.

## Prerequisites
- Python 3.8+
- Playwright

## Usage

### `dougrab.py`

```bash
python dougrab.py <user_id> [--include_poster] [--output OUTPUT] [--max_pages MAX_PAGES]
```

- `<user_id>`: (Required) The Douban user ID for whom you want to scrape reviews.
- `--include_poster`: (Optional) Include this flag if you want to scrape and save the movie poster URLs.
- `--output OUTPUT`: (Optional) The name of the output JSON file. Defaults to reviews.json.
- `--max_pages MAX_PAGES`: (Optional) The maximum number of pages to scrape. If not provided, the script will scrape all available pages.

#### Example

```bash
python dougrab.py 162434298 --include_poster --output my_reviews.json --max_pages 3
```

#### JSON Output Structure

- `cid`: The unique comment ID.
- `full_title`: The full title of the movie, including original and translated titles.
- `movie_link`: A URL to the movie's Douban page.
- `intro`: A brief introduction, including release dates, directors, and genres.
- `rating`: The user's rating (1-5).
- `date`: The date the review was posted.
- `comment`: The user's comment on the movie.
- `poster_url`: URL to the movie's poster image (if --include_poster is used).

### `visualize.py`

```bash
python visualize.py <input_json> [--output OUTPUT]
```
- `<input_json>`: (Required) The JSON file containing the reviews.
- `--output OUTPUT`: (Optional) The name of the output HTML file. Defaults to reviews.html.

#### Example

```bash
python json_to_html.py my_reviews.json --output my_reviews.html
```

## License
MIT