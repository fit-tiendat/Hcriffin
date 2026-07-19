import unittest

from src.metrics import ClassificationMetrics


class MetricsTests(unittest.TestCase):
    def test_confusion_matrix_and_metrics(self):
        metrics = ClassificationMetrics.from_predictions(
            [True, True, False, False],
            [True, False, True, False],
        )

        self.assertEqual(metrics.true_positive, 1)
        self.assertEqual(metrics.true_negative, 1)
        self.assertEqual(metrics.false_positive, 1)
        self.assertEqual(metrics.false_negative, 1)
        self.assertAlmostEqual(metrics.accuracy, 0.5)
        self.assertAlmostEqual(metrics.precision, 0.5)
        self.assertAlmostEqual(metrics.recall, 0.5)
        self.assertAlmostEqual(metrics.f1, 0.5)

    def test_zero_division_returns_zero(self):
        metrics = ClassificationMetrics.from_predictions([False], [False])
        self.assertEqual(metrics.precision, 0.0)
        self.assertEqual(metrics.recall, 0.0)
        self.assertEqual(metrics.f1, 0.0)

    def test_mismatched_lengths_are_rejected(self):
        with self.assertRaises(ValueError):
            ClassificationMetrics.from_predictions([True], [True, False])


if __name__ == "__main__":
    unittest.main()
