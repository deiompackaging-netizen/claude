#!/usr/bin/env python3
"""Generate three deterministic IDE Guide content packages per day.

The generator is dependency-free and safe to run in GitHub Actions. It avoids
repeating IDEs by reading content/history.json. An AI provider can later be
plugged into the content builder without changing the output contract.
"""
from __future__ import annotations

import argparse
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "content" / "history.json"

CATALOG = [
    {"name": "Cursor", "slug": "cursor", "category": "AI-native", "license": "Commercial", "repo": "https://github.com/getcursor/cursor"},
    {"name": "Zed", "slug": "zed", "category": "AI-native", "license": "Open source", "repo": "https://github.com/zed-industries/zed"},
    {"name": "Neovim", "slug": "neovim", "category": "Terminal editor", "license": "Open source", "repo": "https://github.com/neovim/neovim"},
    {"name": "Lapce", "slug": "lapce", "category": "Rust editor", "license": "Open source", "repo": "https://github.com/lapce/lapce"},
    {"name": "Helix", "slug": "helix", "category": "Modal editor", "license": "Open source", "repo": "https://github.com/helix-editor/helix"},
    {"name": "VSCodium", "slug": "vscodium", "category": "Desktop editor", "license": "Open source", "repo": "https://github.com/VSCodium/vscodium"},
    {"name": "Eclipse Theia", "slug": "eclipse-theia", "category": "Cloud IDE", "license": "Open source", "repo": "https://github.com/eclipse-theia/theia"},
    {"name": "Kate", "slug": "kate", "category": "Desktop editor", "license": "Open source", "repo": "https://github.com/KDE/kate"},
    {"name": "Lite XL", "slug": "lite-xl", "category": "Lightweight editor", "license": "Open source", "repo": "https://github.com/lite-xl/lite-xl"},
]

DISCLAIMER = "This is an independent editorial guide. It is not sponsored, endorsed, or paid for by the featured IDE or editor."


def load_history() -> dict:
    if not HISTORY.exists():
        return {"covered": []}
    try:
        return json.loads(HISTORY.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"covered": []}


def choose_three(history: dict) -> list[dict]:
    covered = set(history.get("covered", []))
    fresh = [x for x in CATALOG if x["slug"] not in covered]
    if len(fresh) < 3:
        covered.clear()
        fresh = CATALOG[:]
    return fresh[:3]


def make_post(ide: dict) -> str:
    name = html.escape(ide["name"])
    slug = html.escape(ide["slug"])
    category = html.escape(ide["category"])
    license_ = html.escape(ide["license"])
    repo = html.escape(ide["repo"], quote=True)
    return f'''<!doctype html>\n<html amp lang="en">\n<head>\n<meta charset="utf-8">\n<title>{name} IDE Guide: Setup, Features and Developer Workflow</title>\n<link rel="canonical" href="https://ideguide.blogspot.com/">\n<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">\n<script async src="https://cdn.ampproject.org/v0.js"></script>\n<style amp-custom>body{{font-family:Arial,sans-serif;line-height:1.65;margin:0;padding:24px;max-width:820px;margin:auto;color:#202124}}h1{{line-height:1.2}}.meta{{padding:12px;background:#f1f3f4;border-radius:10px}}code{{background:#f1f3f4;padding:2px 5px;border-radius:4px}}a{{word-break:break-word}}</style>\n</head>\n<body>\n<main>\n<p class="meta">IDE Guide • {category} • {license_}</p>\n<h1>{name} IDE Guide: Setup, Features and Developer Workflow</h1>\n<p>{name} is a developer-focused tool worth evaluating when you care about editing speed, project navigation, extensions, terminal workflows, or AI-assisted development. This guide gives you a practical starting point rather than another ceremonial tour of buttons nobody asked for.</p>\n<h2>Why developers consider {name}</h2>\n<p>The useful evaluation points are startup time, language support, Git workflow, project search, debugging, extension support, customization, and how comfortably the editor fits an existing development stack.</p>\n<h2>Quick setup</h2>\n<ol><li>Install the current release from the project's official distribution channel.</li><li>Open an existing project and verify language tooling.</li><li>Connect Git and configure formatting, linting, and terminal preferences.</li><li>Enable only the extensions or integrations you actually need.</li></ol>\n<h2>Developer workflow</h2>\n<p>Start with project-wide search, jump-to-definition, source control, an integrated terminal, and diagnostics. Then measure the workflow on a real repository. A polished screenshot proves almost nothing; finishing a real feature quickly proves considerably more.</p>\n<h2>Open-source project</h2>\n<p>Repository: <a href="{repo}">{repo}</a></p>\n<h2>Who should try it?</h2>\n<p>{name} is best evaluated by developers whose workflow matches its strengths. Compare it against your current editor using the same project, language, extensions, and tasks so the result is meaningful.</p>\n<h2>Verdict</h2>\n<p>Treat {name} as a workflow tool, not a popularity contest. The best editor is the one that removes friction from your actual daily work.</p>\n<hr>\n<p><strong>Disclaimer:</strong> {DISCLAIMER}</p>\n</main>\n</body>\n</html>\n'''


def make_video(ide: dict) -> dict:
    name = ide["name"]
    return {
        "title": f"{name} in 60 Seconds: IDE Guide",
        "format": {"shorts": "9:16", "long_form": "16:9"},
        "duration_seconds": 60,
        "visual_style": "clean premium developer-tool editorial",
        "scenes": [
            {"timecode": "00:00-00:06", "visual": f"Fast cinematic reveal of {name} editor interface on a modern developer workstation", "camera": "slow push-in", "lighting": "soft monitor glow", "voiceover": f"Meet {name}, a developer tool worth putting through a real workflow."},
            {"timecode": "00:06-00:20", "visual": "Project tree, editor, search and terminal shown in quick purposeful cuts", "camera": "screen-focused tracking", "lighting": "neutral studio", "voiceover": "Focus on project navigation, search, language tooling, Git and terminal flow."},
            {"timecode": "00:20-00:40", "visual": "Developer edits code, searches symbols, reviews a Git change and runs a command", "camera": "over-shoulder medium shot", "lighting": "balanced practical lighting", "voiceover": "The real test is not the feature list. It is how quickly you can finish real work."},
            {"timecode": "00:40-00:54", "visual": "Three concise on-screen cards: strengths, trade-offs, ideal user", "camera": "locked editorial frame", "lighting": "clean high-key", "voiceover": f"Evaluate {name} against your current editor using the same project and tasks."},
            {"timecode": "00:54-01:00", "visual": f"{name} wordmark-style title card with IDE Guide branding", "camera": "gentle pull-back", "lighting": "minimal studio", "voiceover": f"IDE Guide: {name}. Independent review, not sponsored or endorsed by the vendor."},
        ],
        "disclaimer": DISCLAIMER,
    }


def generate(output_dir: Path | None = None) -> list[Path]:
    history = load_history()
    today = date.today().isoformat()
    out = output_dir or ROOT / "content" / today
    out.mkdir(parents=True, exist_ok=True)
    selected = choose_three(history)
    created = []
    for index, ide in enumerate(selected, 1):
        post = out / f"post_{index}_{ide['slug']}.html"
        video = out / f"video_spec_{index}_{ide['slug']}.json"
        post.write_text(make_post(ide), encoding="utf-8")
        video.write_text(json.dumps(make_video(ide), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        created.extend([post, video])
    covered = history.get("covered", [])
    for ide in selected:
        if ide["slug"] not in covered:
            covered.append(ide["slug"])
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps({"covered": covered, "last_generated": today}, indent=2) + "\n", encoding="utf-8")
    return created


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    if args.dry_run:
        print("Dry run: would generate 3 IDE posts and 3 video specs.")
        return
    for path in generate(Path(args.output_dir) if args.output_dir else None):
        print(path)


if __name__ == "__main__":
    main()
