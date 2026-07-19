import tempfile
import unittest
from pathlib import Path

from src.dataset import (
    DGA,
    LEGITIMATE,
    DomainSample,
    deduplicate,
    load_csv,
    stratified_split,
    write_csv,
)


class DatasetTests(unittest.TestCase):
    def test_deduplicate_keeps_one_sample(self):
        samples = [
            DomainSample("example.com", LEGITIMATE, "first"),
            DomainSample("example.com", LEGITIMATE, "second"),
        ]
        self.assertEqual(len(deduplicate(samples)), 1)

    def test_conflicting_labels_are_rejected(self):
        samples = [
            DomainSample("example.com", LEGITIMATE, "a"),
            DomainSample("example.com", DGA, "b"),
        ]
        with self.assertRaises(ValueError):
            deduplicate(samples)

    def test_csv_round_trip(self):
        samples = [
            DomainSample("example.com", LEGITIMATE, "test"),
            DomainSample("x9k2z7.test", DGA, "test"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "domains.csv"
            write_csv(samples, path)
            self.assertEqual(load_csv(path), deduplicate(samples))

    def test_stratified_split_is_deterministic_and_preserves_labels(self):
        samples = [
            DomainSample(f"good{index}.com", LEGITIMATE, "test")
            for index in range(6)
        ] + [
            DomainSample(f"bad{index}x9.test", DGA, "test")
            for index in range(6)
        ]
        first_train, first_test = stratified_split(samples, test_ratio=0.33, seed=7)
        second_train, second_test = stratified_split(samples, test_ratio=0.33, seed=7)

        self.assertEqual(first_train, second_train)
        self.assertEqual(first_test, second_test)
        self.assertEqual({sample.label for sample in first_test}, {LEGITIMATE, DGA})
        self.assertFalse(set(first_train) & set(first_test))

    def test_invalid_split_ratio_is_rejected(self):
        samples = [
            DomainSample("good.com", LEGITIMATE, "test"),
            DomainSample("good2.com", LEGITIMATE, "test"),
            DomainSample("bad.test", DGA, "test"),
            DomainSample("bad2.test", DGA, "test"),
        ]
        with self.assertRaises(ValueError):
            stratified_split(samples, test_ratio=1.0)


if __name__ == "__main__":
    unittest.main()
