import json
import argparse
from playwright.sync_api import sync_playwright


def collect_reviews(user_id, include_poster, max_pages=None):
    url = f"https://movie.douban.com/people/{user_id}/collect"
    reviews = []
    current_page = 1

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        while True:
            review_elements = page.query_selector_all(".item.comment-item")

            for e in review_elements:
                cid = e.get_attribute("data-cid")

                # Movie Title
                full_title = e.query_selector(".title a").inner_text().strip()

                # Movie Link
                movie_link = e.query_selector(".title a").get_attribute("href")

                # Movie Intro (e.g., release date, director, actors, etc.)
                intro = e.query_selector(".intro").inner_text().strip()

                # Rating given by the user (1 - 5)
                rating_element = e.query_selector('span[class^="rating"]')
                rating = (
                    rating_element.get_attribute("class")
                    .split("rating")[1]
                    .split("-")[0]
                    if rating_element
                    and rating_element.get_attribute("class").startswith("rating")
                    else None
                )

                # Date of the review
                date = e.query_selector(".date").inner_text().strip()

                # Comment of the movie
                comment_element = e.query_selector(".comment")
                comment = (
                    comment_element.inner_text().strip() if comment_element else None
                )

                # Movie Poster URL
                poster_element = e.query_selector(".pic img")
                poster_url = (
                    poster_element.get_attribute("src") if poster_element else None
                )

                # Create one review object for the current movie
                review = {
                    "cid": cid,
                    "full_title": full_title,
                    "movie_link": movie_link,
                    "intro": intro,
                    **({"rating": rating} if rating else {}),
                    **({"date": date} if date else {}),
                    **({"comment": comment} if comment else {}),
                    **(
                        {"poster_url": poster_url}
                        if include_poster and poster_url
                        else {}
                    ),
                }

                reviews.append(review)

            if max_pages and current_page >= max_pages:
                break

            next_button = page.query_selector(".paginator .next a")
            if next_button:
                next_page_url = next_button.get_attribute("href")
                page.goto(f"https://movie.douban.com{next_page_url}")
                page.wait_for_load_state("networkidle")
                current_page += 1
            else:
                break

        # Close the browser
        browser.close()

    return reviews


def save_reviews_to_json(reviews, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)


def main():
    parser = argparse.ArgumentParser(description="Douban Movie Reviews Scraper")
    parser.add_argument("user_id", help="The Douban user ID")
    parser.add_argument(
        "--include_poster",
        action="store_true",
        help="Whether to include the movie poster URL in the output",
    )
    parser.add_argument(
        "--output",
        default="reviews.json",
        help="Output file name (default: reviews.json)",
    )
    parser.add_argument(
        "--max_pages",
        type=int,
        help="Maximum number of pages to scrape (default: all pages)",
    )

    args = parser.parse_args()

    reviews = collect_reviews(args.user_id, args.include_poster, args.max_pages)
    save_reviews_to_json(reviews, args.output)

    print(f"Saved {len(reviews)} reviews to {args.output}")


if __name__ == "__main__":
    main()
