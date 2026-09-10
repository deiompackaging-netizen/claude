# IDE Guide 🚀

Automated content engine for technical reviews, feature comparisons, and developer setup guides for modern IDEs and code editors.

## Daily publishing package

Each daily run creates three unique IDE/editor packages under `content/YYYY-MM-DD/`:

- `post_N_<ide>.html`: clean AMP HTML suitable for Blogger.
- `video_spec_N_<ide>.json`: scene-by-scene Google Flow-style production specification for Shorts (9:16) and long-form (16:9).
- `content/history.json`: tracks covered tools to reduce repetition.

Every package contains an independent, non-sponsorship disclaimer.

## Run locally

```bash
python3 scripts/generate_daily_content.py --dry-run
python3 scripts/generate_daily_content.py
pytest tests/
```

## Agentic CLI

```bash
python3 scripts/ide_guide_agent_skill.py --ide "Windsurf Editor"
python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/lapce/lapce"
python3 scripts/ide_guide_agent_skill.py --ide "Zed" --output-dir custom_output
```

## GitHub Actions

`.github/workflows/daily_content_generation.yml` runs daily and can also be started manually from GitHub Actions. It installs dependencies, runs tests when present, generates content, validates that exactly three posts and three video specs exist, and commits the generated `content/` directory.

The current schedule is 00:30 UTC, which is 05:30 Pakistan Standard Time.

## Publishing targets

- Blogger: `ideguide.blogspot.com`
- YouTube: `@IDEguide`

Automated publishing credentials are intentionally not stored in the repository. When publishing integrations are added, keep tokens/API keys in GitHub Actions Secrets or another secret manager.

## Project structure

```text
content/
├── history.json
└── YYYY-MM-DD/
    ├── post_1_<ide>.html
    ├── video_spec_1_<ide>.json
    ├── post_2_<ide>.html
    ├── video_spec_2_<ide>.json
    ├── post_3_<ide>.html
    └── video_spec_3_<ide>.json
scripts/
├── generate_daily_content.py
└── ide_guide_agent_skill.py
tests/
└── test_ide_guide.py
.github/workflows/
└── daily_content_generation.yml
```

> Note: the repository may also contain the existing Google Pay demo files. They are kept separate so this IDE Guide work does not silently destroy the earlier project.
