"""Build a labelled CSV from the raw legitimate and synthetic DGA lists."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.dataset import DGA, LEGITIMATE, deduplicate, label_counts, read_domain_list, write_csv


BASE_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare the Episode 2 dataset")
    parser.add_argument(
        "--legitimate",
        type=Path,
        default=BASE_DIR / "data" / "raw_legitimate.txt",
    )
    parser.add_argument(
        "--dga",
        type=Path,
        default=BASE_DIR / "data" / "raw_dga_synthetic.txt",
    )
    parser.add_argument(
        "--output", type=Path, default=BASE_DIR / "data" / "domains.csv"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    samples = deduplicate(
        read_domain_list(args.legitimate, LEGITIMATE, "manual-benign")
        + read_domain_list(args.dga, DGA, "synthetic-dga")
    )
    write_csv(samples, args.output)
    counts = label_counts(samples)
    print(f"Wrote {len(samples)} samples to {args.output}")
    print(f"legitimate={counts[LEGITIMATE]}, dga={counts[DGA]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
