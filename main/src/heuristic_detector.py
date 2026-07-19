"""An explainable heuristic baseline for suspicious domain detection."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .domain_features import DomainFeatures, extract_features


DEFAULT_THRESHOLD = 0.55


@dataclass(frozen=True)
class DetectionResult:
    domain: str
    score: float
    verdict: str
    reasons: tuple[str, ...]
    features: DomainFeatures

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["reasons"] = list(self.reasons)
        return payload


def score_features(features: DomainFeatures) -> tuple[float, tuple[str, ...]]:
    score = 0.0
    reasons: list[str] = []

    if features.length >= 16:
        score += 0.25
        reasons.append("long label")
    if features.length >= 25:
        score += 0.10
        reasons.append("very long label")

    if features.entropy >= 3.5:
        score += 0.30
        reasons.append("high character entropy")
    elif features.entropy >= 3.0:
        score += 0.15
        reasons.append("moderate character entropy")

    if features.digit_ratio >= 0.20:
        score += 0.20
        reasons.append("many digits")

    if features.length >= 12 and features.vowel_ratio <= 0.20:
        score += 0.15
        reasons.append("low vowel ratio")

    if features.length >= 12 and features.unique_ratio >= 0.70:
        score += 0.10
        reasons.append("high unique-character ratio")

    if features.max_consonant_run >= 5:
        score += 0.15
        reasons.append("long consonant run")

    return round(min(score, 1.0), 2), tuple(reasons)


def detect(domain: str, threshold: float = DEFAULT_THRESHOLD) -> DetectionResult:
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1")

    features = extract_features(domain)
    score, reasons = score_features(features)
    verdict = "suspicious" if score >= threshold else "likely-legitimate"
    return DetectionResult(features.domain, score, verdict, reasons, features)
