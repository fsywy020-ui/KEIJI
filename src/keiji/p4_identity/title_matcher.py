"""Title token matching for P4 product identity."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class TitleMatchResult:
    """Conservative title comparison result."""

    score: float
    shared_tokens: tuple[str, ...]
    source_only_tokens: tuple[str, ...]
    listing_only_tokens: tuple[str, ...]


def tokenize_title(title: str) -> tuple[str, ...]:
    """Tokenize normalized Japanese/English product titles without external deps."""

    normalized = title.lower()
    normalized = re.sub(r"(\d+)([a-z]+)", r"\1 \2", normalized)
    raw_tokens = re.findall(r"[a-z0-9]+|[ぁ-んァ-ン一-龥ー]+", normalized)
    tokens: list[str] = []
    for token in raw_tokens:
        if len(token) <= 1 and not token.isdigit():
            continue
        tokens.append(token)
    return tuple(tokens)


def match_titles(source_title: str, listing_title: str) -> TitleMatchResult:
    """Compare title tokens with a simple Jaccard score."""

    source_tokens = set(tokenize_title(source_title))
    listing_tokens = set(tokenize_title(listing_title))
    if not source_tokens or not listing_tokens:
        return TitleMatchResult(0.0, (), tuple(sorted(source_tokens)), tuple(sorted(listing_tokens)))
    shared = source_tokens & listing_tokens
    union = source_tokens | listing_tokens
    return TitleMatchResult(
        score=round(len(shared) / len(union), 4),
        shared_tokens=tuple(sorted(shared)),
        source_only_tokens=tuple(sorted(source_tokens - listing_tokens)),
        listing_only_tokens=tuple(sorted(listing_tokens - source_tokens)),
    )
