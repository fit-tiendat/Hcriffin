# ML Baseline Evaluation

## Configuration

- Algorithm: StandardScaler + LogisticRegression
- scikit-learn: 1.9.0
- Train samples: 48
- Test samples: 16
- Test labels: legitimate=8, dga=8
- ML threshold: 0.50
- Heuristic threshold: 0.55

## Baseline Comparison

| Detector | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Heuristic | 0.688 | 1.000 | 0.375 | 0.545 |
| Logistic Regression | 0.938 | 1.000 | 0.875 | 0.933 |

## ML Confusion Matrix

| | Predicted DGA | Predicted legitimate |
|---|---:|---:|
| Actual DGA | 7 | 1 |
| Actual legitimate | 0 | 8 |

## Standardized Feature Weights

| Feature | Weight |
|---|---:|
| `length` | 1.3584 |
| `vowel_ratio` | -1.0766 |
| `entropy` | 0.8595 |
| `label_count` | -0.7718 |
| `max_consonant_run` | 0.7629 |
| `unique_ratio` | -0.7345 |
| `digit_ratio` | 0.6381 |
| `hyphen_ratio` | -0.6087 |

## Misclassified Holdout Samples

| Domain | Actual | DGA probability |
|---|---|---:|
| `silentmeadow.test` | dga | 0.328 |

## Interpretation

This experiment validates the ML training pipeline, not production accuracy.
The dataset is small, balanced and partly synthetic, so the reported metrics
must be confirmed on larger independent DNS datasets.
