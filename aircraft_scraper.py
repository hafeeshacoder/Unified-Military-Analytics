import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://www.globalfirepower.com/aircraft-total.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

try:
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    records = soup.find_all("div", class_="recordsetContainer")

    print("Total Records Found:", len(records))

    all_data = []

    for record in records:
        text = record.get_text(" | ", strip=True)

        all_data.append({
            "Data": text
        })

    df = pd.DataFrame(all_data)

    df.to_csv("military_aircraft_data.csv",
              index=False,
              encoding="utf-8-sig")

    print(df.head())
    print("\nCSV Saved Successfully!")

except Exception as e:
    print("Error:", e)