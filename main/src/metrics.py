"""Binary classification metrics implemented with the Python standard library."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


def safe_divide(numerator: int | float, denominator: int | float) -> float:
    return float(numerator / denominator) if denominator else 0.0


@dataclass(frozen=True)
class ClassificationMetrics:
    true_positive: int
    true_negative: int
    false_positive: int
    false_negative: int

    @classmethod
    def from_predictions(
        cls, expected: Iterable[bool], predicted: Iterable[bool]
    ) -> "ClassificationMetrics":
        expected_values = list(expected)
        predicted_values = list(predicted)
        if len(expected_values) != len(predicted_values):
            raise ValueError("expected and predicted must have the same length")

        tp = tn = fp = fn = 0
        for truth, prediction in zip(expected_values, predicted_values):
            if truth and prediction:
                tp += 1
            elif not truth and not prediction:
                tn += 1
            elif not truth and prediction:
                fp += 1
            else:
                fn += 1
        return cls(tp, tn, fp, fn)

    @property
    def total(self) -> int:
        return self.true_positive + self.true_negative + self.false_positive + self.false_negative

    @property
    def accuracy(self) -> float:
        return safe_divide(self.true_positive + self.true_negative, self.total)

    @property
    def precision(self) -> float:
        return safe_divide(self.true_positive, self.true_positive + self.false_positive)

    @property
    def recall(self) -> float:
        return safe_divide(self.true_positive, self.true_positive + self.false_negative)

    @property
    def f1(self) -> float:
        return safe_divide(2 * self.precision * self.recall, self.precision + self.recall)

    def to_dict(self) -> dict[str, int | float]:
        return {
            "tp": self.true_positive,
            "tn": self.true_negative,
            "fp": self.false_positive,
            "fn": self.false_negative,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
        }
