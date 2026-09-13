#!/usr/bin/env python3
"""Build a daily, monetization-aware content package.

This script does not log into platforms, buy traffic, or send unsolicited messages.
It creates a ready-to-publish plan with CTAs, disclosure text, and tracking fields.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "content" / "earning_engine_config.json"
OUT = ROOT / "content" / "earning_queue.json"

TOPICS = [
    {
        "topic": "AI IDE workflow for small businesses",
        "pillar": "AI + software",
        "product": "ai-ide-starter-guide",
        "format": "long_video",
        "hook": "Stop wasting hours switching between coding tools. Build one repeatable AI IDE workflow.",
    },
    {
        "topic": "Developer productivity automation",
        "pillar": "AI + software",
        "product": "developer-productivity-template-pack",
        "format": "long_video",
        "hook": "Turn a messy project into a repeatable delivery system with templates and automation.",
    },
    {
        "topic": "Solar quotation automation",
        "pillar": "solar + business",
        "product": "solar-quotation-automation-starter-pack",
        "format": "long_video",
        "hook": "Build a professional solar quote faster, with fewer calculation and pricing mistakes.",
    },
]


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def build_queue(config: dict) -> dict:
    today = datetime.now(timezone.utc).date().isoformat()
    products = {p["slug"]: p for p in config["product_ctas"]}
    items = []
    for i, topic in enumerate(TOPICS, start=1):
        product = products[topic["product"]]
        items.append(
            {
                "id": f"{today}-{i}",
                "date": today,
                "pillar": topic["pillar"],
                "format": topic["format"],
                "title": topic["topic"],
                "hook": topic["hook"],
                "cta": {
                    "product": topic["product"],
                    "price_usd": product["price_usd"],
                    "checkout_url": product["checkout_url"],
                    "status": "replace_placeholder_before_publish",
                },
                "shorts": [
                    f"{topic['topic']}: 30-second mistake to avoid",
                    f"{topic['topic']}: one practical tip",
                    f"{topic['topic']}: before/after workflow",
                ],
                "disclosure": "Affiliate links, if used, will be clearly disclosed. Product links are commercial offers.",
                "tracking": {
                    "utm_source": "youtube",
                    "utm_medium": "video",
                    "utm_campaign": topic["product"],
                    "views": 0,
                    "clicks": 0,
                    "sales": 0,
                    "revenue_usd": 0,
                },
            }
        )
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "daily monetization-ready content queue",
        "items": items,
        "publish_status": "draft_queue_only",
        "safety": config["rules"],
    }


def main() -> None:
    config = load_config()
    queue = build_queue(config)
    OUT.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
