#!/usr/bin/env python3
"""Discover affiliate/referral signals from GitHub and maintain a review queue."""
from __future__ import annotations
import json
import os
from datetime import date
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "content" / "affiliate_programs.json"
QUERIES = [
    "developer tools affiliate program",
    "AI developer tools affiliate",
    "SaaS developer tools referral program",
    "developer tool commission affiliate",
]

def api_search(query: str) -> list[dict]:
    url = "https://api.github.com/search/issues?q=" + quote(query + " is:pr") + "&per_page=10"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "IDE-Guide-Affiliate-Scanner"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=20) as response:
        return json.load(response).get("items", [])

def score(text: str) -> int:
    text = text.lower()
    points = {"affiliate": 35, "referral": 25, "commission": 20, "developer tools": 10, "saas": 5}
    return min(100, sum(v for k, v in points.items() if k in text))

def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {"version": 1, "last_scanned": None, "programs": [], "rules": {}}
    existing = {x.get("source_url") for x in registry.get("programs", [])}
    added = 0
    for query in QUERIES:
        try:
            items = api_search(query)
        except Exception as exc:
            print(f"Search failed for {query!r}: {exc}")
            continue
        for item in items:
            source_url = item.get("html_url", "")
            if not source_url or source_url in existing:
                continue
            text = (item.get("title", "") + " " + item.get("body", ""))
            registry["programs"].append({
                "name": item.get("title", "GitHub discovery"),
                "status": "discovery_only",
                "official_url": "",
                "affiliate_url": "",
                "commission": None,
                "recurring": None,
                "cookie_days": None,
                "application_url": "",
                "source_url": source_url,
                "source": "GitHub PR search",
                "score": score(text),
                "last_verified": None,
                "notes": "Discovery signal only. Verify the official affiliate/referral program before publication.",
            })
            existing.add(source_url)
            added += 1
    registry["last_scanned"] = date.today().isoformat()
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Affiliate discovery complete. Added {added} candidates.")

if __name__ == "__main__":
    main()
