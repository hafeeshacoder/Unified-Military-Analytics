import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Browser header
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Read the links file
with open("links_for_military_data.txt", "r", encoding="utf-8") as file:
    content = file.read()

# Extract all URLs from the file
urls = re.findall(r"https://[^\s'\",}]+", content)

print(f"Found {len(urls)} URLs\n")

all_data = []

# Loop through each URL
for url in urls:
    try:
        print(f"Scraping: {url}")

        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Page title (Metric Name)
        title = soup.title.get_text(strip=True) if soup.title else "Unknown Metric"

        # Find all country records
        records = soup.find_all("div", class_="recordsetContainer")

        print(f"Records found: {len(records)}")

        # Extract information
        for record in records:

            rank = record.find("div", class_="rankNumContainer")

            country = record.find("div", class_="longFormName")

            value = record.find("div", class_="valueContainer")

            all_data.append({
                "Metric": title,
                "Rank": rank.get_text(strip=True) if rank else "",
                "Country": country.get_text(strip=True) if country else "",
                "Value": value.get_text(" ", strip=True) if value else "",
                "Source_URL": url
            })

        # Wait before next request
        time.sleep(1)

    except Exception as e:
        print(f"Failed: {url}")
        print(e)

# Create DataFrame
df = pd.DataFrame(all_data)

# Save CSV
df.to_csv("military_raw_data.csv", index=False, encoding="utf-8")

print("\n=========================================")
print("Scraping Completed Successfully!")
print(f"Total Records Scraped : {len(df)}")
print("Output File           : military_raw_data.csv")
print("=========================================")

# Show first few rows
print(df.head())