import unittest

from src.dataset import DGA, LEGITIMATE, DomainSample
from src.ml_model import FEATURE_NAMES, domain_to_vector, predict_probabilities, train


class MachineLearningModelTests(unittest.TestCase):
    def setUp(self):
        self.samples = [
            DomainSample("google.com", LEGITIMATE, "test"),
            DomainSample("microsoft.com", LEGITIMATE, "test"),
            DomainSample("python.org", LEGITIMATE, "test"),
            DomainSample("wikipedia.org", LEGITIMATE, "test"),
            DomainSample("asdkjhqwekjhzxc.test", DGA, "test"),
            DomainSample("zmxncbvpoiuqwer123.test", DGA, "test"),
            DomainSample("q7w9e2r4t6y8u1i3.test", DGA, "test"),
            DomainSample("mncbvxzasdfghjkl.test", DGA, "test"),
        ]

    def test_domain_vector_has_named_numeric_features(self):
        vector = domain_to_vector("example.com")
        self.assertEqual(len(vector), len(FEATURE_NAMES))
        self.assertTrue(all(isinstance(value, float) for value in vector))

    def test_model_returns_probabilities(self):
        model = train(self.samples, random_state=7)
        probabilities = predict_probabilities(model, ["google.com", "x9k2z7m4.test"])

        self.assertEqual(len(probabilities), 2)
        self.assertTrue(all(0.0 <= value <= 1.0 for value in probabilities))

    def test_training_requires_both_labels(self):
        with self.assertRaises(ValueError):
            train(self.samples[:4])


if __name__ == "__main__":
    unittest.main()
