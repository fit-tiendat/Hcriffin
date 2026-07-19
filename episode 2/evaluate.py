"""Evaluate the Episode 1 heuristic on a deterministic holdout split."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from src.dataset import DomainSample, label_counts, load_csv, stratified_split
from src.heuristic_detector import DEFAULT_THRESHOLD, detect
from src.metrics import ClassificationMetrics


BASE_DIR = Path(__file__).resolve().parent


def evaluate(
    samples: Sequence[DomainSample], threshold: float
) -> tuple[ClassificationMetrics, list[tuple[DomainSample, float, bool]]]:
    results = []
    for sample in samples:
        prediction = detect(sample.domain, threshold)
        predicted_dga = prediction.verdict == "suspicious"
        results.append((sample, prediction.score, predicted_dga))

    metrics = ClassificationMetrics.from_predictions(
        (sample.is_dga for sample, _, _ in results),
        (predicted for _, _, predicted in results),
    )
    return metrics, results


def format_report(
    dataset_size: int,
    train_size: int,
    test_samples: Sequence[DomainSample],
    threshold: float,
    metrics: ClassificationMetrics,
    results: Sequence[tuple[DomainSample, float, bool]],
) -> str:
    counts = label_counts(test_samples)
    errors = [
        (sample, score, predicted)
        for sample, score, predicted in results
        if sample.is_dga != predicted
    ]

    lines = [
        "# Episode 02 Evaluation Report",
        "",
        "## Configuration",
        "",
        f"- Dataset size: {dataset_size}",
        f"- Train split: {train_size}",
        f"- Test split: {len(test_samples)}",
        f"- Test labels: legitimate={counts['legitimate']}, dga={counts['dga']}",
        f"- Detection threshold: {threshold:.2f}",
        f"- Dataset type: manual benign + synthetic DGA (pipeline demo only)",
        "",
        "## Confusion Matrix",
        "",
        "| | Predicted DGA | Predicted legitimate |",
        "|---|---:|---:|",
        f"| Actual DGA | {metrics.true_positive} | {metrics.false_negative} |",
        f"| Actual legitimate | {metrics.false_positive} | {metrics.true_negative} |",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Accuracy | {metrics.accuracy:.3f} |",
        f"| Precision | {metrics.precision:.3f} |",
        f"| Recall | {metrics.recall:.3f} |",
        f"| F1 | {metrics.f1:.3f} |",
        "",
        "## Misclassified Holdout Samples",
        "",
    ]

    if not errors:
        lines.append("No misclassified samples in this holdout split.")
    else:
        lines.extend(("| Domain | Actual | Score | Predicted |", "|---|---|---:|---|"))
        for sample, score, predicted in sorted(errors, key=lambda item: item[0].domain):
            verdict = "dga" if predicted else "legitimate"
            lines.append(f"| `{sample.domain}` | {sample.label} | {score:.2f} | {verdict} |")

    lines.extend(
        (
            "",
            "## Interpretation",
            "",
            "These numbers validate the evaluation pipeline, not production accuracy.",
            "The dataset is small and partly synthetic. Episode 3 will train and compare",
            "an ML baseline using the same metrics.",
        )
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate the heuristic DGA baseline")
    parser.add_argument(
        "--dataset", type=Path, default=BASE_DIR / "data" / "domains.csv"
    )
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--test-ratio", type=float, default=0.25)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--report", type=Path, default=BASE_DIR / "reports" / "evaluation.md"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    samples = load_csv(args.dataset)
    train, test = stratified_split(samples, args.test_ratio, args.seed)
    metrics, results = evaluate(test, args.threshold)
    report = format_report(len(samples), len(train), test, args.threshold, metrics, results)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")

    print(f"dataset={len(samples)} train={len(train)} test={len(test)}")
    print(
        f"TP={metrics.true_positive} TN={metrics.true_negative} "
        f"FP={metrics.false_positive} FN={metrics.false_negative}"
    )
    print(
        f"accuracy={metrics.accuracy:.3f} precision={metrics.precision:.3f} "
        f"recall={metrics.recall:.3f} f1={metrics.f1:.3f}"
    )
    print(f"Report written to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
