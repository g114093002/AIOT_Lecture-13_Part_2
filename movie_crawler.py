import requests
from bs4 import BeautifulSoup
import csv

# The URL pattern to scrape
BASE_URL = "https://ssr1.scrape.center/page/{page}"
# The number of pages to scrape
NUM_PAGES = 10

# List to store all movie data
all_movies = []

# Loop through pages 1 to 10
for page in range(1, NUM_PAGES + 1):
    url = BASE_URL.format(page=page)
    print(f"Scraping page {page}: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.text, "html.parser")

        # Find all movie containers on the page
        movie_items = soup.find_all("div", class_="el-card__body")

        for item in movie_items:
            # --- Extract Movie Name ---
            # The name is in an h2 tag
            name_tag = item.find("h2", class_="m-b-sm")
            name = name_tag.text.strip() if name_tag else "N/A"
            
            # --- Extract Image URL ---
            # The image URL is in the 'src' attribute of the img tag
            img_tag = item.find("img", class_="cover")
            img_url = img_tag["src"] if img_tag and "src" in img_tag.attrs else "N/A"

            # --- Extract Score ---
            # The score is in a p tag with class 'score'
            score_tag = item.find("p", class_="score")
            score = score_tag.text.strip() if score_tag else "N/A"

            # --- Extract Categories ---
            # Categories are in div tags with class 'm-v-sm'
            category_tags = item.find_all("div", class_="m-v-sm")
            categories = []
            # The second div with this class contains the categories
            if len(category_tags) > 1:
                category_buttons = category_tags[1].find_all("button")
                categories = [button.text.strip() for button in category_buttons]
            
            # Append the extracted data to our list
            all_movies.append({
                "name": name,
                "image_url": img_url,
                "score": score,
                "categories": ", ".join(categories) # Join categories into a single string
            })

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")

# --- Write data to CSV ---
# Define the CSV file path
csv_file = "movie.csv"
# Define the headers for the CSV
headers = ["name", "image_url", "score", "categories"]

# Write the data to the CSV file
with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_movies)

print(f"\nScraping complete. Data saved to {csv_file}")
