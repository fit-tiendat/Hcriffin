"""Load, validate, deduplicate and split labelled domain datasets."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
import random
from typing import Iterable, Sequence

from .domain_features import normalize_domain


LEGITIMATE = "legitimate"
DGA = "dga"
VALID_LABELS = frozenset((LEGITIMATE, DGA))


@dataclass(frozen=True)
class DomainSample:
    domain: str
    label: str
    source: str

    @property
    def is_dga(self) -> bool:
        return self.label == DGA


def read_domain_list(path: Path, label: str, source: str) -> list[DomainSample]:
    if label not in VALID_LABELS:
        raise ValueError(f"Unsupported label: {label}")

    samples: list[DomainSample] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            value = line.strip()
            if not value or value.startswith("#"):
                continue
            try:
                domain = normalize_domain(value)
            except ValueError as exc:
                raise ValueError(f"{path}:{line_number}: {exc}") from exc
            samples.append(DomainSample(domain, label, source))
    return samples


def deduplicate(samples: Iterable[DomainSample]) -> list[DomainSample]:
    unique: dict[str, DomainSample] = {}
    for sample in samples:
        existing = unique.get(sample.domain)
        if existing and existing.label != sample.label:
            raise ValueError(
                f"Conflicting labels for {sample.domain}: "
                f"{existing.label} and {sample.label}"
            )
        unique.setdefault(sample.domain, sample)
    return sorted(unique.values(), key=lambda item: (item.label, item.domain))


def write_csv(samples: Sequence[DomainSample], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("domain", "label", "source"))
        writer.writeheader()
        for sample in samples:
            writer.writerow(
                {"domain": sample.domain, "label": sample.label, "source": sample.source}
            )


def load_csv(path: Path) -> list[DomainSample]:
    samples: list[DomainSample] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"domain", "label", "source"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"Dataset must contain columns: {sorted(required)}")

        for row_number, row in enumerate(reader, start=2):
            label = row["label"].strip().lower()
            if label not in VALID_LABELS:
                raise ValueError(f"{path}:{row_number}: unsupported label {label!r}")
            samples.append(
                DomainSample(
                    normalize_domain(row["domain"]),
                    label,
                    row["source"].strip() or "unknown",
                )
            )
    return deduplicate(samples)


def label_counts(samples: Iterable[DomainSample]) -> dict[str, int]:
    counts = {LEGITIMATE: 0, DGA: 0}
    for sample in samples:
        counts[sample.label] += 1
    return counts


def stratified_split(
    samples: Sequence[DomainSample], test_ratio: float = 0.25, seed: int = 42
) -> tuple[list[DomainSample], list[DomainSample]]:
    if not 0.0 < test_ratio < 1.0:
        raise ValueError("test_ratio must be between 0 and 1")

    grouped = {
        label: [sample for sample in samples if sample.label == label]
        for label in VALID_LABELS
    }
    if any(len(group) < 2 for group in grouped.values()):
        raise ValueError("Each label needs at least two samples for a split")

    rng = random.Random(seed)
    train: list[DomainSample] = []
    test: list[DomainSample] = []

    for label in sorted(grouped):
        group = grouped[label][:]
        rng.shuffle(group)
        test_count = max(1, min(len(group) - 1, round(len(group) * test_ratio)))
        test.extend(group[:test_count])
        train.extend(group[test_count:])

    rng.shuffle(train)
    rng.shuffle(test)
    return train, test
