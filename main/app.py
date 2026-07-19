"""Command-line demo for the episode 1 explainable DGA baseline."""

from __future__ import annotations

import argparse
import json

from src.heuristic_detector import DEFAULT_THRESHOLD, detect


DEFAULT_DOMAINS = (
    "google.com",
    "microsoft.com",
    "wikipedia.org",
    "asdkjhqwekjhzxc.com",
    "xk3jh2kasdjf.net",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Score domain names with an explainable heuristic baseline."
    )
    parser.add_argument("domains", nargs="*", help="Domain names to inspect")
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help=f"Suspicious score threshold (default: {DEFAULT_THRESHOLD})",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    domains = args.domains or DEFAULT_DOMAINS

    try:
        results = [detect(domain, args.threshold) for domain in domains]
    except ValueError as exc:
        print(f"error: {exc}")
        return 2

    if args.json:
        print(json.dumps([result.to_dict() for result in results], indent=2))
        return 0

    print(f"{'DOMAIN':<32} {'SCORE':>5}  {'VERDICT':<17} REASONS")
    print("-" * 100)
    for result in results:
        reasons = ", ".join(result.reasons) or "no strong lexical signal"
        print(f"{result.domain:<32} {result.score:>5.2f}  {result.verdict:<17} {reasons}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
