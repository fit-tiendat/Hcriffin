"""Train and run a lexical-feature machine-learning baseline."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .dataset import DomainSample
from .domain_features import extract_features


FEATURE_NAMES = (
    "length",
    "entropy",
    "digit_ratio",
    "hyphen_ratio",
    "vowel_ratio",
    "unique_ratio",
    "max_consonant_run",
    "label_count",
)


def domain_to_vector(domain: str) -> list[float]:
    features = extract_features(domain)
    return [float(getattr(features, name)) for name in FEATURE_NAMES]


def samples_to_xy(
    samples: Iterable[DomainSample],
) -> tuple[list[list[float]], list[int]]:
    sample_list = list(samples)
    return (
        [domain_to_vector(sample.domain) for sample in sample_list],
        [int(sample.is_dga) for sample in sample_list],
    )


def build_model(random_state: int = 42) -> Pipeline:
    return Pipeline(
        steps=(
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=1_000,
                    random_state=random_state,
                ),
            ),
        )
    )


def train(samples: Sequence[DomainSample], random_state: int = 42) -> Pipeline:
    x_train, y_train = samples_to_xy(samples)
    if len(set(y_train)) < 2:
        raise ValueError("Training data must contain legitimate and DGA samples")

    model = build_model(random_state)
    model.fit(x_train, y_train)
    return model


def predict_probabilities(model: Pipeline, domains: Iterable[str]) -> list[float]:
    domain_list = list(domains)
    if not domain_list:
        return []
    matrix = [domain_to_vector(domain) for domain in domain_list]
    return [float(value) for value in model.predict_proba(matrix)[:, 1]]
