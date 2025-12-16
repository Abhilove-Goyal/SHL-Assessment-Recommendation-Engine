import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}

train = pd.read_csv("data/processed/train.csv")
urls = train["Assessment_url"].unique().tolist()

print("Unique assessment URLs:", len(urls))

records = []

for i, url in enumerate(urls):
    try:
        print(f"[{i+1}/{len(urls)}] Crawling {url}")
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        name = soup.find("h1")
        name = name.get_text(strip=True) if name else ""

        description = soup.find("meta", {"name": "description"})
        description = description["content"] if description else ""

        records.append({
            "assessment_url": url,
            "name": name,
            "description": description
        })

        time.sleep(0.8)

    except Exception as e:
        print("Error:", url, e)

df = pd.DataFrame(records)
df.to_csv("data/processed/shl_catalog.csv", index=False)

print("Final catalog size:", df.shape)
