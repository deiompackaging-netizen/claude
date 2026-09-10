#!/usr/bin/env python3
"""Maintain an internal revenue ledger. This is not a bank or payment wallet."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WALLET = ROOT / "content" / "revenue_wallet.json"


def load():
    return json.loads(WALLET.read_text(encoding="utf-8"))


def save(data):
    WALLET.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def add(amount: float, source: str, status: str):
    data = load()
    tx = {
        "id": datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f"),
        "date": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "amount": round(amount, 2),
        "status": status,
    }
    data["transactions"].append(tx)
    if status == "paid":
        data["paid"] += amount
        data["balance"] += amount
    elif status == "pending":
        data["pending"] += amount
    save(data)
    print(json.dumps(tx, indent=2))


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("amount", type=float)
    a.add_argument("source")
    a.add_argument("--status", choices=["pending", "paid"], default="pending")
    sub.add_parser("show")
    args = p.parse_args()
    if args.cmd == "add":
        add(args.amount, args.source, args.status)
    else:
        print(json.dumps(load(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
