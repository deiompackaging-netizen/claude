#!/usr/bin/env python3
"""Score content ideas for earning potential without inventing affiliate claims."""
from __future__ import annotations


def commercial_score(*, buyer_intent: int, demand: int, affiliate_verified: bool, recurring: bool = False, competition: int = 5) -> int:
    """Return a 0-100 opportunity score.

    Inputs are 0-10 except booleans. Affiliate status is binary because an
    unverified program must never be treated as monetizable.
    """
    score = buyer_intent * 4 + demand * 3 + (20 if affiliate_verified else 0)
    score += 5 if recurring and affiliate_verified else 0
    score += max(0, 10 - competition) * 1
    return max(0, min(100, score))


def classify(score: int) -> str:
    if score >= 80:
        return "high"
    if score >= 60:
        return "medium"
    return "low"


if __name__ == "__main__":
    print(commercial_score(buyer_intent=9, demand=8, affiliate_verified=False))
