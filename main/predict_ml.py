"""Run domain inference with a trained scikit-learn model artifact."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib

from src.ml_model import predict_probabilities


BASE_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict DGA probabilities")
    parser.add_argument("domains", nargs="+", help="Domain names to classify")
    parser.add_argument(
        "--model",
        type=Path,
        default=BASE_DIR / "artifacts" / "dga_logistic.joblib",
    )
    parser.add_argument("--threshold", type=float, default=0.50)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 0.0 <= args.threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1")
    if not args.model.exists():
        raise FileNotFoundError(
            f"Model not found: {args.model}. Run train_model.py first."
        )

    model = joblib.load(args.model)
    probabilities = predict_probabilities(model, args.domains)

    print(f"{'DOMAIN':<36} {'DGA_PROB':>8}  VERDICT")
    print("-" * 62)
    for domain, probability in zip(args.domains, probabilities):
        verdict = "suspicious" if probability >= args.threshold else "likely-legitimate"
        print(f"{domain:<36} {probability:>8.3f}  {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
