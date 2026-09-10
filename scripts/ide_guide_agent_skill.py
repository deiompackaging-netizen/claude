#!/usr/bin/env python3
"""On-demand IDE Guide generator."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_daily_content import CATALOG, make_post, make_video  # noqa: E402


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "ide"


def find_ide(name: str, repo: str | None = None) -> dict:
    target = (repo or name).lower().rstrip("/")
    for item in CATALOG:
        if target == item["name"].lower() or target == item["repo"].lower().rstrip("/") or target.endswith(item["repo"].lower().rstrip("/")):
            return item
    return {"name": name, "slug": slugify(name), "category": "Developer tool", "license": "Unknown", "repo": repo or ""}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a custom IDE Guide package")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ide")
    group.add_argument("--repo")
    parser.add_argument("--output-dir", default="custom_output")
    args = parser.parse_args()
    ide = find_ide(args.ide or args.repo, args.repo)
    out = ROOT / args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    (out / f"post_{ide['slug']}.html").write_text(make_post(ide), encoding="utf-8")
    (out / f"video_spec_{ide['slug']}.json").write_text(__import__("json").dumps(make_video(ide), indent=2) + "\n", encoding="utf-8")
    print(f"Generated guide for {ide['name']} in {out}")


if __name__ == "__main__":
    main()
