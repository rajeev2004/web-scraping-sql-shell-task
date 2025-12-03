#!/usr/bin/env python3

"""
Scrapes OLX using their public JSON API and prints a table of:
- title
- price (display format)
- description snippet
- link
"""

import requests
from tabulate import tabulate
import argparse
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_URL = "https://www.olx.in/api/relevance/v4/search"


def fetch_results(query, limit):
    """Fetch OLX search results with retry and longer timeout."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
    })

    params = {"query": query, "limit": limit}

    for attempt in range(5):  # retry up to 5 times
        try:
            res = session.get(
                API_URL,
                params=params,
                timeout=30  # ← increase timeout
            )
            res.raise_for_status()
            return res.json()

        except requests.exceptions.Timeout:
            print(f"Timeout… retrying ({attempt + 1}/5)")
            continue
        except Exception as e:
            print("Error fetching API:", e)
            sys.exit(1)

    print("Failed after 5 retries.")
    sys.exit(1)


def parse_results(data, limit):
    """Convert OLX JSON API output into clean rows."""
    items = data.get("data", [])
    results = []

    for item in items[:limit]:
        title = item.get("title", "").strip()
        desc = item.get("description", "").strip()

        # price.value.display
        price_display = ""
        if item.get("price") and item["price"].get("value"):
            price_display = item["price"]["value"].get("display", "")

        # Link
        ad_id = item.get("id")
        link = f"https://www.olx.in/item/{ad_id}" if ad_id else ""

        results.append([
            title,
            price_display,
            desc[:120],
            link
        ])

    return results


def main():
    parser = argparse.ArgumentParser(description="OLX API Search Scraper (No HTML scraping)")
    parser.add_argument("query", help="Search keyword (e.g., 'car cover')")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    json_data = fetch_results(args.query, args.limit)
    rows = parse_results(json_data, args.limit)

    if not rows:
        print("No results found.")
        return

    print(tabulate(rows, headers=["Title", "Price", "Description", "Link"], tablefmt="github"))


if __name__ == "__main__":
    main()
