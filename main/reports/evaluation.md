# Episode 02 Evaluation Report

## Configuration

- Dataset size: 64
- Train split: 48
- Test split: 16
- Test labels: legitimate=8, dga=8
- Detection threshold: 0.55
- Dataset type: manual benign + synthetic DGA (pipeline demo only)

## Confusion Matrix

| | Predicted DGA | Predicted legitimate |
|---|---:|---:|
| Actual DGA | 3 | 5 |
| Actual legitimate | 0 | 8 |

## Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.688 |
| Precision | 1.000 |
| Recall | 0.375 |
| F1 | 0.545 |

## Misclassified Holdout Samples

| Domain | Actual | Score | Predicted |
|---|---|---:|---|
| `dailynewsportal.test` | dga | 0.40 | legitimate |
| `fdkhakshfda.test` | dga | 0.15 | legitimate |
| `greenmarketplace.test` | dga | 0.40 | legitimate |
| `morningweatherdata.test` | dga | 0.40 | legitimate |
| `silentmeadow.test` | dga | 0.25 | legitimate |

## Interpretation

These numbers validate the evaluation pipeline, not production accuracy.
The dataset is small and partly synthetic. Episode 3 will train and compare
an ML baseline using the same metrics.
