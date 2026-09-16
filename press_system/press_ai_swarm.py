"""Bounded five-agent DEIOM PRESS automation coordinator.

This module is intentionally dependency-light. It can run without an API key,
using deterministic checks and capability analysis. If OPENAI_API_KEY is later
provided through GitHub Secrets, an optional AI enrichment layer can be added
without placing credentials in source control.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "press_agents"
OUT.mkdir(parents=True, exist_ok=True)

AGENTS = {
    "erp_qa": "ERP QA Agent",
    "operations": "Operations Agent",
    "revenue": "Revenue Agent",
    "ai_upgrade": "AI Upgrade Agent",
    "security": "Security & Reliability Agent",
}

FEATURE_PATTERNS = {
    "quotations": r"quotation|quote|cost estimator",
    "production": r"production|printing|press|job card",
    "quality": r"quality control|qc|capa|inspection",
    "inventory": r"inventory|warehouse|stock|grn|fifo|fefo",
    "finance": r"finance|invoice|margin|costing|receivable",
    "ai": r"ai command|ai agent|ai-assisted|estimator|auto-assignment",
    "dispatch": r"dispatch|logistics|delivery",
}


def load_reference() -> str:
    candidates = [
        ROOT / "press_system" / "DEIOM_PRESS_ERP.html",
        ROOT / "DEIOM_PRESS_ERP.html",
        ROOT / "press_system" / "PRESS_SYSTEM_MANIFEST.md",
    ]
    chunks = []
    for p in candidates:
        if p.exists():
            chunks.append(p.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(chunks)


def detect_features(text: str) -> dict[str, bool]:
    low = text.lower()
    return {k: bool(re.search(v, low)) for k, v in FEATURE_PATTERNS.items()}


def run_agent(name: str, text: str, features: dict[str, bool]) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    if name == "erp_qa":
        script_count = len(re.findall(r"<script\b", text, flags=re.I))
        return {
            "agent": AGENTS[name],
            "timestamp": now,
            "checks": {"html_present": bool(text), "script_tags": script_count},
            "actions": [
                "Run HTML syntax/runtime smoke tests.",
                "Preserve the documented classic-script load order.",
                "Verify localStorage persistence and graceful CDN failure behavior.",
            ],
        }
    if name == "operations":
        active = [k for k, v in features.items() if v]
        return {
            "agent": AGENTS[name],
            "timestamp": now,
            "detected_capabilities": active,
            "actions": [
                "Map every job stage to an owner, SLA, and next-action signal.",
                "Prioritize overdue jobs, stock shortages, QC failures, and capacity bottlenecks.",
                "Keep the Job Card as the single production record.",
            ],
        }
    if name == "revenue":
        return {
            "agent": AGENTS[name],
            "timestamp": now,
            "commercial_assets": [
                "Printing ERP implementation/setup service",
                "Solar/printing quotation workflow customization",
                "ERP training and SOP package",
                "B2B custom packaging + offset printing lead funnel",
            ],
            "actions": [
                "Create buyer-intent content from real ERP capabilities.",
                "Generate qualified B2B prospect tasks rather than fake engagement.",
                "Keep checkout and payout actions disabled until account authorization exists.",
            ],
        }
    if name == "ai_upgrade":
        return {
            "agent": AGENTS[name],
            "timestamp": now,
            "actions": [
                "Prepare demand forecasting from historical job data.",
                "Prepare AI-assisted SOP, quotation, QC-report, and customer-draft generation.",
                "Prepare a bounded API adapter that reads credentials only from environment secrets.",
                "Do not imply computer vision or IoT is live until hardware/data feeds exist.",
            ],
        }
    return {
        "agent": AGENTS[name],
        "timestamp": now,
        "security_checks": [
            "No credentials, OTPs, passwords, or payment details in source control.",
            "No covert device control or unauthorized account actions.",
            "Pin or validate external dependencies where practical.",
            "Use bounded retries and timeouts for network integrations.",
        ],
        "actions": [
            "Scan generated files for accidental secrets before commit.",
            "Keep account actions behind explicit authorization gates.",
        ],
    }


def main() -> None:
    text = load_reference()
    features = detect_features(text)
    cycle = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    reports = {k: run_agent(k, text, features) for k in AGENTS}
    aggregate = {
        "system": "DEIOM PRESS GEN Swarm",
        "cycle": cycle,
        "agents": reports,
        "feature_detection": features,
        "api_enabled": bool(os.getenv("OPENAI_API_KEY")),
        "authorization_state": "pre-account-connection",
    }
    (OUT / "latest.json").write_text(json.dumps(aggregate, indent=2), encoding="utf-8")
    print(json.dumps({"cycle": cycle, "agents": list(AGENTS), "api_enabled": aggregate["api_enabled"]}))


if __name__ == "__main__":
    main()
