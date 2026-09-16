"""Bounded five-agent DEIOM PRESS automation coordinator.

The swarm is capability-driven: it audits the PRESS ERP, revenue workflow,
AI/voice integrations, and security posture every cycle. Provider credentials
are never stored in source control. Account actions remain gated until the
owner supplies approved secrets/integrations.
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
    "voice": r"twilio|amazon connect|realtime|phone agent|sip|media stream",
    "mcp": r"model context protocol|mcp",
}


def load_reference() -> str:
    candidates = [
        ROOT / "press_system" / "DEIOM_PRESS_ERP.html",
        ROOT / "DEIOM_PRESS_ERP.html",
        ROOT / "press_system" / "PRESS_SYSTEM_MANIFEST.md",
        ROOT / "press_system" / "AI_PHONE_AGENT_INTEGRATION.md",
    ]
    chunks = []
    for p in candidates:
        if p.exists():
            chunks.append(p.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(chunks)


def load_provider_registry() -> dict:
    path = ROOT / "content" / "ai_provider_registry.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def detect_features(text: str) -> dict[str, bool]:
    low = text.lower()
    return {k: bool(re.search(v, low)) for k, v in FEATURE_PATTERNS.items()}


def run_agent(name: str, text: str, features: dict[str, bool], registry: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    if name == "erp_qa":
        script_count = len(re.findall(r"<script\b", text, flags=re.I))
        return {
            "agent": AGENTS[name],
            "timestamp": now,
            "checks": {"html_present": bool(text), "script_tags": script_count},
            "actions": [
                "Run HTML syntax/runtime smoke tests.",
                "Preserve documented classic-script load order.",
                "Verify localStorage persistence and graceful CDN failure behavior.",
                "Validate new AI/voice adapters without enabling account actions.",
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
                "Prepare voice intake so callers can create structured leads/jobs after authorization.",
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
                "AI phone receptionist / lead-intake service",
            ],
            "actions": [
                "Create buyer-intent content from real ERP capabilities.",
                "Generate qualified B2B prospect tasks rather than fake engagement.",
                "Prepare phone lead qualification and appointment workflows.",
                "Keep checkout, payout, publishing, and outbound messaging disabled until authorization exists.",
            ],
        }
    if name == "ai_upgrade":
        providers = registry.get("providers", [])
        return {
            "agent": AGENTS[name],
            "timestamp": now,
            "provider_registry_count": len(providers),
            "enabled_credentials_detected": [
                key for key in registry.get("credential_env", []) if os.getenv(key)
            ],
            "actions": [
                "Continuously compare configured AI providers by capability, reliability, latency, and cost signals.",
                "Prepare demand forecasting, AI-assisted SOP, quotation, QC-report, and customer-draft generation.",
                "Maintain OpenAI Realtime/Twilio/Amazon Connect/MCP voice integration as an optional capability layer.",
                "Use provider adapters and bounded fallback; never silently create accounts, spend money, or change billing.",
                "Prefer stable/pinned production model identifiers; test newer candidates before promotion.",
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
            "Require explicit authorization gates before publishing, messaging, payments, or phone calling.",
        ],
        "actions": [
            "Scan generated files for accidental secrets before commit.",
            "Keep account actions behind explicit authorization gates.",
            "Reject unreviewed provider/model upgrades that fail compatibility checks.",
        ],
    }


def main() -> None:
    text = load_reference()
    features = detect_features(text)
    registry = load_provider_registry()
    requested_agent = os.getenv("PRESS_AGENT", "all").lower().replace("-", "_")
    cycle = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if requested_agent in AGENTS:
        reports = {requested_agent: run_agent(requested_agent, text, features, registry)}
    else:
        reports = {k: run_agent(k, text, features, registry) for k in AGENTS}
    aggregate = {
        "system": "DEIOM PRESS GEN-5 Swarm",
        "cycle": cycle,
        "requested_agent": requested_agent,
        "agents": reports,
        "feature_detection": features,
        "provider_registry_version": registry.get("version"),
        "api_enabled": bool(os.getenv("OPENAI_API_KEY")),
        "authorization_state": "pre-account-connection",
    }
    (OUT / "latest.json").write_text(json.dumps(aggregate, indent=2), encoding="utf-8")
    print(json.dumps({"cycle": cycle, "agent": requested_agent, "api_enabled": aggregate["api_enabled"]}))


if __name__ == "__main__":
    main()
