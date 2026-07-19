"""Extract explainable lexical features from a domain name."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from math import log2
import re


DOMAIN_RE = re.compile(r"^[a-z0-9.-]+$")
VOWELS = frozenset("aeiou")


@dataclass(frozen=True)
class DomainFeatures:
    domain: str
    candidate_label: str
    length: int
    entropy: float
    digit_ratio: float
    hyphen_ratio: float
    vowel_ratio: float
    unique_ratio: float
    max_consonant_run: int
    label_count: int

    def to_dict(self) -> dict[str, str | int | float]:
        return asdict(self)


def normalize_domain(domain: str) -> str:
    """Return a lowercase hostname without scheme, port, path or trailing dot."""
    value = domain.strip().lower()
    if "://" in value:
        value = value.split("://", 1)[1]
    value = value.split("/", 1)[0]
    value = value.rsplit(":", 1)[0]
    value = value.rstrip(".")

    if not value or ".." in value or not DOMAIN_RE.fullmatch(value):
        raise ValueError(f"Invalid domain: {domain!r}")

    labels = value.split(".")
    if any(not label or len(label) > 63 for label in labels):
        raise ValueError(f"Invalid domain labels: {domain!r}")
    return value


def shannon_entropy(value: str) -> float:
    if not value:
        return 0.0
    counts = Counter(value)
    size = len(value)
    return -sum((count / size) * log2(count / size) for count in counts.values())


def longest_consonant_run(value: str) -> int:
    longest = 0
    current = 0
    for char in value:
        if char.isalpha() and char not in VOWELS:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def select_candidate_label(domain: str) -> str:
    """Select the longest non-TLD label as a simple DGA candidate."""
    labels = domain.split(".")
    candidates = labels[:-1] if len(labels) > 1 else labels
    return max(candidates, key=len)


def extract_features(domain: str) -> DomainFeatures:
    normalized = normalize_domain(domain)
    candidate = select_candidate_label(normalized)
    size = len(candidate)

    return DomainFeatures(
        domain=normalized,
        candidate_label=candidate,
        length=size,
        entropy=round(shannon_entropy(candidate), 4),
        digit_ratio=round(sum(char.isdigit() for char in candidate) / size, 4),
        hyphen_ratio=round(candidate.count("-") / size, 4),
        vowel_ratio=round(sum(char in VOWELS for char in candidate) / size, 4),
        unique_ratio=round(len(set(candidate)) / size, 4),
        max_consonant_run=longest_consonant_run(candidate),
        label_count=len(normalized.split(".")),
    )
