import json
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://github.com/orgs/google/repositories?page={page}"
HEADERS = {"User-Agent": "Mozilla/5.0 (class assignment scraper)"}


def find_repo_dicts(obj, found):
    """Walk the JSON and collect dicts that look like a repository."""
    if isinstance(obj, dict):
        if "name" in obj and "starsCount" in obj:
            found.append(obj)
        for v in obj.values():
            find_repo_dicts(v, found)
    elif isinstance(obj, list):
        for v in obj:
            find_repo_dicts(v, found)


def scrape_page(page):
    res = requests.get(BASE_URL.format(page=page), headers=HEADERS)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    tag = soup.find("script", {"data-target": "react-app.embeddedData"})
    if tag is None or not tag.string:
        return []
    data = json.loads(tag.string)

    found = []
    find_repo_dicts(data, found)

    repos = []
    seen = set()
    for item in found:
        name = item["name"]
        if name in seen:
            continue
        seen.add(name)
        lang = item.get("primaryLanguage")
        language = lang.get("name") if isinstance(lang, dict) else None
        repos.append((name, language, item.get("starsCount", 0)))
    return repos


def scrape_google_repos(max_pages=3):
    """Scrape several pages and return a list of (name, language, stars)."""
    all_repos = []
    for page in range(1, max_pages + 1):
        repos = scrape_page(page)
        print(f"page {page}: found {len(repos)} repos")
        if not repos:
            break
        all_repos.extend(repos)
        time.sleep(1)  # required by the assignment
    return all_repos


if __name__ == "__main__":
    data = scrape_google_repos(1)
    for row in data[:5]:
        print(row)