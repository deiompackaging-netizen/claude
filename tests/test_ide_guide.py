from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import generate_daily_content as gen


def test_daily_generation_creates_three_posts_and_specs(tmp_path, monkeypatch):
    history = tmp_path / "history.json"
    monkeypatch.setattr(gen, "HISTORY", history)
    created = gen.generate(tmp_path / "content")
    assert len([p for p in created if p.name.startswith("post_")]) == 3
    assert len([p for p in created if p.name.startswith("video_spec_")]) == 3


def test_posts_are_amp_and_have_disclaimer(tmp_path, monkeypatch):
    history = tmp_path / "history.json"
    monkeypatch.setattr(gen, "HISTORY", history)
    gen.generate(tmp_path / "content")
    for post in (tmp_path / "content").glob("post_*.html"):
        text = post.read_text(encoding="utf-8")
        assert '<html amp lang="en">' in text
        assert 'https://cdn.ampproject.org/v0.js' in text
        assert "This is an independent editorial guide" in text


def test_video_specs_are_valid_json(tmp_path, monkeypatch):
    history = tmp_path / "history.json"
    monkeypatch.setattr(gen, "HISTORY", history)
    gen.generate(tmp_path / "content")
    for spec in (tmp_path / "content").glob("video_spec_*.json"):
        data = json.loads(spec.read_text(encoding="utf-8"))
        assert data["scenes"]
        assert data["disclaimer"]


def test_history_prevents_immediate_duplicates(tmp_path, monkeypatch):
    history = tmp_path / "history.json"
    monkeypatch.setattr(gen, "HISTORY", history)
    first = gen.generate(tmp_path / "one")
    second = gen.generate(tmp_path / "two")
    first_names = {p.name.split("_")[-1].rsplit(".", 1)[0] for p in first if p.name.startswith("post_")}
    second_names = {p.name.split("_")[-1].rsplit(".", 1)[0] for p in second if p.name.startswith("post_")}
    assert first_names.isdisjoint(second_names)
