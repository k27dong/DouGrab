import json
import argparse
from pathlib import Path
import re


def generate_html(reviews, output_file):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Douban Movie Reviews</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f4f4f4;
            }
            .review {
                background-color: #fff;
                margin-bottom: 20px;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                display: flex;
                align-items: flex-start;
            }
            .review img {
                max-width: 150px;
                border-radius: 5px;
                margin-right: 20px;
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
            .review h2 {
                margin: 0;
                font-size: 1.5em;
                color: #333;
            }
            .review h3 {
                margin: 0;
                font-size: 1.2em;
                color: #666;
            }
            .review .comment {
                font-size: 1.1em;
                margin-top: 15px;
                color: #000;
            }
            .review .date {
                margin-top: 10px;
                font-size: 0.9em;
                color: #999;
            }
            .review .rating {
                font-size: 2em;
                margin: 0;
                text-align: center;
            }
            .review-content {
                flex: 1;
                margin-left: 20px;
            }
        </style>
    </head>
    <body>
        <h1>你的影评</h1>
    """

    for review in reviews:
        poster_url = review.get("poster_url", None)
        full_title = review.get("full_title", None)
        movie_link = review.get("movie_link", None)
        intro = review.get("intro", None)
        rating = review.get("rating", None)
        date = review.get("date", None)
        comment = review.get("comment", None)
        release_year = None

        titles = full_title.split(" / ")
        main_title = titles[0]
        english_title = next(
            (
                title
                for title in titles
                if re.match(r"^[\w\s\'\-.,:;()]+$", title)
                and re.search(r"[A-Za-z]", title)
            ),
            None,
        )

        if intro:
            for part in intro.split(" / "):
                match = re.search(r"\b(\d{4})-\d{2}-\d{2}\b", part)
                if match:
                    release_year = match.group(1)
                    break

        poster_html = ""
        if poster_url:
            poster_html = f'<a href="{movie_link}" target="_blank" class="poster-link"><img src="{poster_url}" alt="{main_title} poster"></a>'

        rating_html = ""
        if rating:
            black_stars = "★" * int(rating)
            white_stars = "☆" * (5 - int(rating))
            rating_html = f'<p class="rating">{black_stars}{white_stars}</p>'

        # Build the review HTML block
        html_content += f"""
        <div class="review">
            <div>
            {poster_html}
            {rating_html}
            </div>
            <div class="review-content">
                <h2>{main_title} ({release_year})</h2>
                {"<h3>" + english_title + "</h3>" if english_title else ""}
                <div class="comment">{comment}</div>
                <div>
                    {"<p class='date'>Date: " + date + "</p>" if date else ""}

                </div>
            </div>

        </div>
        """

    html_content += """
    </body>
    </html>
    """

    # Write the HTML content to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML file created: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Convert JSON reviews to HTML")
    parser.add_argument("input_json", help="The input JSON file containing reviews")
    parser.add_argument(
        "--output",
        default="reviews.html",
        help="Output HTML file name (default: reviews.html)",
    )

    args = parser.parse_args()
    with open(args.input_json, "r", encoding="utf-8") as f:
        reviews = json.load(f)
    generate_html(reviews, args.output)


if __name__ == "__main__":
    main()
