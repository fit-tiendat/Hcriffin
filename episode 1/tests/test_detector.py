import unittest

from src.domain_features import extract_features, normalize_domain, shannon_entropy
from src.heuristic_detector import detect


class DomainFeatureTests(unittest.TestCase):
    def test_normalizes_url_and_trailing_dot(self):
        self.assertEqual(normalize_domain("HTTPS://Example.COM./path"), "example.com")

    def test_rejects_invalid_domain(self):
        with self.assertRaises(ValueError):
            normalize_domain("not a domain")

    def test_selects_longest_non_tld_label(self):
        features = extract_features("www.security-example.com")
        self.assertEqual(features.candidate_label, "security-example")

    def test_entropy_of_repeated_character_is_zero(self):
        self.assertEqual(shannon_entropy("aaaaaaaa"), 0.0)


class HeuristicDetectorTests(unittest.TestCase):
    def test_common_domain_is_not_flagged(self):
        result = detect("google.com")
        self.assertEqual(result.verdict, "likely-legitimate")

    def test_synthetic_random_domain_is_flagged(self):
        result = detect("asdkjhqwekjhzxc.com")
        self.assertEqual(result.verdict, "suspicious")

    def test_threshold_is_validated(self):
        with self.assertRaises(ValueError):
            detect("example.com", threshold=1.2)


if __name__ == "__main__":
    unittest.main()
