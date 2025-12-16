import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

BASE_URL = "https://www.shl.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

SEARCH_URL = (
    "https://www.shl.com/solutions/products/product-catalog/"
    "?page={page}"
)

def get_all_assessment_links(max_pages=20):
    urls = set()

    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}")
        res = requests.get(SEARCH_URL.format(page=page), headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        links = soup.select("a[href*='/product-catalog/view/']")
        if not links:
            break

        for a in links:
            href = a.get("href")
            if href and "pre-packaged" not in href.lower():
                urls.add(BASE_URL + href)

        time.sleep(1)

    print(f"Total unique assessments found: {len(urls)}")
    return list(urls)


def safe_text(soup, label):
    try:
        el = soup.find(text=re.compile(label, re.I))
        if el:
            return el.find_next().get_text(strip=True)
    except:
        pass
    return ""


def crawl_assessment(url):
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    name = soup.find("h1")
    name = name.get_text(strip=True) if name else ""

    description = soup.find("meta", {"name": "description"})
    description = description["content"] if description else ""

    duration = safe_text(soup, "Duration")
    test_type = safe_text(soup, "Test Type")
    remote_support = safe_text(soup, "Remote")
    adaptive_support = safe_text(soup, "Adaptive")

    return {
        "assessment_url": url,
        "name": name,
        "description": description,
        "test_type": test_type,
        "duration": duration,
        "remote_support": remote_support,
        "adaptive_support": adaptive_support
    }


def main():
    urls = get_all_assessment_links(max_pages=25)
    records = []

    for i, url in enumerate(urls):
        try:
            print(f"[{i+1}/{len(urls)}] Crawling {url}")
            records.append(crawl_assessment(url))
            time.sleep(0.8)
        except Exception as e:
            print("Error:", url, e)

    df = pd.DataFrame(records)
    df.to_csv("data/processed/shl_catalog.csv", index=False)
    print("Saved catalog:", df.shape)


if __name__ == "__main__":
    main()
