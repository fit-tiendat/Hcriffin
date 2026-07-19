"""Train, evaluate and persist the lexical Logistic Regression baseline."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Sequence

import joblib
import sklearn

from src.dataset import DomainSample, label_counts, load_csv, stratified_split
from src.heuristic_detector import DEFAULT_THRESHOLD as HEURISTIC_THRESHOLD
from src.heuristic_detector import detect
from src.metrics import ClassificationMetrics
from src.ml_model import FEATURE_NAMES, predict_probabilities, train


BASE_DIR = Path(__file__).resolve().parent


def metrics_from_probabilities(
    samples: Sequence[DomainSample], probabilities: Sequence[float], threshold: float
) -> ClassificationMetrics:
    return ClassificationMetrics.from_predictions(
        (sample.is_dga for sample in samples),
        (probability >= threshold for probability in probabilities),
    )


def evaluate_heuristic(samples: Sequence[DomainSample]) -> ClassificationMetrics:
    return ClassificationMetrics.from_predictions(
        (sample.is_dga for sample in samples),
        (
            detect(sample.domain, HEURISTIC_THRESHOLD).verdict == "suspicious"
            for sample in samples
        ),
    )


def metric_row(name: str, metrics: ClassificationMetrics) -> str:
    return (
        f"| {name} | {metrics.accuracy:.3f} | {metrics.precision:.3f} | "
        f"{metrics.recall:.3f} | {metrics.f1:.3f} |"
    )


def metric_payload(metrics: ClassificationMetrics) -> dict[str, int | float]:
    return {
        key: round(value, 6) if isinstance(value, float) else value
        for key, value in metrics.to_dict().items()
    }


def build_report(
    train_samples: Sequence[DomainSample],
    test_samples: Sequence[DomainSample],
    probabilities: Sequence[float],
    ml_metrics: ClassificationMetrics,
    heuristic_metrics: ClassificationMetrics,
    threshold: float,
    feature_weights: dict[str, float],
) -> str:
    counts = label_counts(test_samples)
    errors = [
        (sample, probability)
        for sample, probability in zip(test_samples, probabilities)
        if sample.is_dga != (probability >= threshold)
    ]
    weights = sorted(feature_weights.items(), key=lambda item: abs(item[1]), reverse=True)

    lines = [
        "# ML Baseline Evaluation",
        "",
        "## Configuration",
        "",
        "- Algorithm: StandardScaler + LogisticRegression",
        f"- scikit-learn: {sklearn.__version__}",
        f"- Train samples: {len(train_samples)}",
        f"- Test samples: {len(test_samples)}",
        f"- Test labels: legitimate={counts['legitimate']}, dga={counts['dga']}",
        f"- ML threshold: {threshold:.2f}",
        f"- Heuristic threshold: {HEURISTIC_THRESHOLD:.2f}",
        "",
        "## Baseline Comparison",
        "",
        "| Detector | Accuracy | Precision | Recall | F1 |",
        "|---|---:|---:|---:|---:|",
        metric_row("Heuristic", heuristic_metrics),
        metric_row("Logistic Regression", ml_metrics),
        "",
        "## ML Confusion Matrix",
        "",
        "| | Predicted DGA | Predicted legitimate |",
        "|---|---:|---:|",
        f"| Actual DGA | {ml_metrics.true_positive} | {ml_metrics.false_negative} |",
        f"| Actual legitimate | {ml_metrics.false_positive} | {ml_metrics.true_negative} |",
        "",
        "## Standardized Feature Weights",
        "",
        "| Feature | Weight |",
        "|---|---:|",
    ]
    lines.extend(f"| `{name}` | {weight:.4f} |" for name, weight in weights)
    lines.extend(("", "## Misclassified Holdout Samples", ""))

    if errors:
        lines.extend(("| Domain | Actual | DGA probability |", "|---|---|---:|"))
        for sample, probability in sorted(errors, key=lambda item: item[0].domain):
            lines.append(f"| `{sample.domain}` | {sample.label} | {probability:.3f} |")
    else:
        lines.append("No misclassified samples in this holdout split.")

    lines.extend(
        (
            "",
            "## Interpretation",
            "",
            "This experiment validates the ML training pipeline, not production accuracy.",
            "The dataset is small, balanced and partly synthetic, so the reported metrics",
            "must be confirmed on larger independent DNS datasets.",
        )
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the DGA ML baseline")
    parser.add_argument(
        "--dataset", type=Path, default=BASE_DIR / "data" / "domains.csv"
    )
    parser.add_argument("--test-ratio", type=float, default=0.25)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--threshold", type=float, default=0.50)
    parser.add_argument(
        "--model-output",
        type=Path,
        default=BASE_DIR / "artifacts" / "dga_logistic.joblib",
    )
    parser.add_argument(
        "--metadata-output",
        type=Path,
        default=BASE_DIR / "artifacts" / "model_metadata.json",
    )
    parser.add_argument(
        "--report", type=Path, default=BASE_DIR / "reports" / "ml_baseline.md"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 0.0 <= args.threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1")

    samples = load_csv(args.dataset)
    train_samples, test_samples = stratified_split(samples, args.test_ratio, args.seed)
    model = train(train_samples, args.seed)
    probabilities = predict_probabilities(
        model, (sample.domain for sample in test_samples)
    )
    ml_metrics = metrics_from_probabilities(test_samples, probabilities, args.threshold)
    heuristic_metrics = evaluate_heuristic(test_samples)

    classifier = model.named_steps["classifier"]
    feature_weights = dict(zip(FEATURE_NAMES, classifier.coef_[0].tolist()))

    args.model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.model_output)
    model_hash = sha256(args.model_output.read_bytes()).hexdigest()
    dataset_hash = sha256(args.dataset.read_bytes()).hexdigest()

    metadata = {
        "algorithm": "StandardScaler + LogisticRegression",
        "dataset_sha256": dataset_hash,
        "feature_names": list(FEATURE_NAMES),
        "heuristic_metrics": metric_payload(heuristic_metrics),
        "ml_metrics": metric_payload(ml_metrics),
        "model_sha256": model_hash,
        "random_seed": args.seed,
        "scikit_learn_version": sklearn.__version__,
        "dataset_size": len(samples),
        "test_size": len(test_samples),
        "threshold": args.threshold,
        "train_size": len(train_samples),
    }
    args.metadata_output.parent.mkdir(parents=True, exist_ok=True)
    args.metadata_output.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    report = build_report(
        train_samples,
        test_samples,
        probabilities,
        ml_metrics,
        heuristic_metrics,
        args.threshold,
        feature_weights,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")

    print(metric_row("Heuristic", heuristic_metrics))
    print(metric_row("Logistic Regression", ml_metrics))
    print(f"Model written to {args.model_output}")
    print(f"Metadata written to {args.metadata_output}")
    print(f"Report written to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
