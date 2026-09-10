#!/usr/bin/env python3
"""Maintain a verified affiliate-opportunity registry.

This scanner uses public GitHub PR search results as discovery signals. It does
not assume that a GitHub listing is an affiliate program and never fabricates
commission rates or tracking URLs. Human/official verification is required
before an opportunity can be published.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "content" / "affiliate_programs.json"

DISCOVERY_QUERIES = [
    "developer tools affiliate program",
    "AI developer tools affiliate",
    "SaaS developer tools referral program",
]


def load_registry() -> dict:
    if not REGISTRY.exists():
        return {"version": 1, "last_scanned": None, "programs": [], "rules": {}}
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def github_search_url(query: str) -> str:
    return "https://github.com/search?q=" + query.replace(" ", "+") + "&type=pullrequests"


def score_candidate(candidate: dict) -> int:
    """Score only discovery quality; this is not a claim that a program exists."""
    text = (candidate.get("title", "") + " " + candidate.get("body", "")).lower()
    score = 0
    for term, points in (("affiliate", 30), ("referral", 20), ("commission", 15), ("developer tools", 10), ("saas", 5)):
        if term in text:
            score += points
    return min(score, 100)


def add_discovery(registry: dict, title: str, url: str, source: str, notes: str = "") -> None:
    existing = {item.get("source_url") for item in registry["programs"]}
    if url in existing:
        return
    registry["programs"].append({
        "name": title,
        "status": "discovery_only",
        "official_url": "",
        "affiliate_url": "",
        "commission": None,
        "recurring": None,
        "cookie_days": None,
        "application_url": "",
        "source_url": url,
        "source": source,
        "score": score_candidate({"title": title, "body": notes}),
        "last_verified": None,
        "notes": "GitHub discovery signal only. Verify the official affiliate/referral terms before publication.",
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Create registry structure and example discovery sources without claiming programs.")
    args = parser.parse_args()

    registry = load_registry()
    registry["last_scanned"] = date.today().isoformat()

    if args.demo:
        for query in DISCOVERY_QUERIES:
            add_discovery(
                registry,
                f"GitHub search: {query}",
                github_search_url(query),
                "GitHub PR search",
                query,
            )

    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Affiliate registry updated: {REGISTRY}")


if __name__ == "__main__":
    main()
