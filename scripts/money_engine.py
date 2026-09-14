#!/usr/bin/env python3
"""Deterministic daily commercial task planner for the DEIOM revenue system.

This script does not send messages, publish content, or move money. It creates a
prioritized work queue from configured products/channels and a small topic catalog.
External account actions remain explicitly authorized by the owner.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "content" / "money_engine_config.json"
QUEUE = ROOT / "content" / "money_engine_queue.json"

TOPICS = [
    ("AI IDE comparison: Cursor vs VS Code", 10, "ai-ide-starter"),
    ("Best developer productivity workflow for small teams", 9, "developer-productivity-pack"),
    ("How to build a professional solar quotation workflow", 10, "solar-quotation-starter"),
    ("Solar quotation mistakes that lose customers", 10, "solar-quotation-starter"),
    ("Automating repetitive developer setup tasks", 8, "developer-productivity-pack"),
    ("Hybrid solar quotation checklist for installers", 10, "solar-quotation-starter"),
]


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def build_queue(run_date: str) -> dict:
    config = load_config()
    product_map = {p["id"]: p for p in config["products"]}
    ranked = sorted(TOPICS, key=lambda item: (-item[1], item[0]))
    selected = ranked[:3]

    tasks = []
    for idx, (topic, score, product_id) in enumerate(selected, 1):
        product = product_map[product_id]
        tasks.extend(
            [
                {
                    "priority": score,
                    "type": "commercial_article",
                    "topic": topic,
                    "cta_product": product["name"],
                    "cta_url": product["checkout_url"],
                },
                {
                    "priority": score,
                    "type": "long_form_video",
                    "topic": topic,
                    "angle": "Problem -> practical demonstration -> result -> product CTA",
                },
                {
                    "priority": score,
                    "type": "short_form",
                    "topic": topic,
                    "angle": f"Hook #{idx}: one concrete mistake, fix, or shortcut",
                },
            ]
        )

    return {
        "date": run_date,
        "status": "planned",
        "tasks": tasks,
        "rules": [
            "No fake traffic or engagement",
            "No spam blasting",
            "Disclose affiliate relationships",
            "Do not publish credentials or payment secrets",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    queue = build_queue(args.date)
    print(json.dumps(queue, indent=2, ensure_ascii=False))
    if args.write:
        QUEUE.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {QUEUE}")


if __name__ == "__main__":
    main()
