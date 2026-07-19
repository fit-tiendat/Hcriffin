# HCRiffin DGA Detector

Day la code hien tai cua module phat hien domain co dau hieu DGA. Phien ban
hien tai gom heuristic co the giai thich, Logistic Regression baseline va
pipeline danh gia co the lap lai. Suricata va Elasticsearch chua duoc tich hop
vao runtime nay.

## MITRE ATT&CK mapping

```text
TA0011 - Command and Control
  -> T1568 - Dynamic Resolution
      -> T1568.002 - Domain Generation Algorithms
```

## Data flow hien tai

```text
raw_legitimate.txt + raw_dga_synthetic.txt
                    |
                    v
          prepare_dataset.py
                    |
                    v
             domains.csv
                    |
         stratified train/test split
                    |
                    v
       lexical feature extraction
              /             \
             v               v
       heuristic       Logistic Regression
              \             /
               v           v
         comparison report + metrics
```

Heuristic khong hoc tu train split. Logistic Regression duoc fit tren 48 mau
train va danh gia tren cung 16 mau holdout dung de do heuristic.

## Cau truc

```text
main/
|-- app.py
|-- prepare_dataset.py
|-- evaluate.py
|-- train_model.py
|-- predict_ml.py
|-- requirements.txt
|-- artifacts/
|   `-- model_metadata.json
|-- data/
|   |-- raw_legitimate.txt
|   |-- raw_dga_synthetic.txt
|   `-- domains.csv
|-- reports/
|   |-- evaluation.md
|   `-- evaluation-threshold-040.md
|-- src/
|   |-- domain_features.py
|   |-- heuristic_detector.py
|   |-- dataset.py
|   |-- metrics.py
|   `-- ml_model.py
`-- tests/
    |-- test_detector.py
    |-- test_dataset.py
    |-- test_metrics.py
    `-- test_ml_model.py
```

## Cach chay

Yeu cau Python 3.9 tro len.

```bash
cd main

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

python3 app.py google.com asdkjhqwekjhzxc.test
python3 prepare_dataset.py
python3 evaluate.py
python3 evaluate.py --threshold 0.40 --report reports/evaluation-threshold-040.md
python3 train_model.py
python3 predict_ml.py google.com asdkjhqwekjhzxc.test
python3 -m unittest discover -s tests -v
```

## Dataset demo

Dataset co 64 mau can bang:

- 32 domain legitimate, gom domain thong dung va hostname benign mo phong;
- 32 domain DGA mo phong tren reserved TLD `.test`.

Dataset nay chi dung de kiem thu pipeline. No khong dai dien cho DNS traffic
thuc va khong du de cong bo do chinh xac cua san pham an ninh mang.

## Ket qua baseline

Split co dinh voi seed 42 tao 48 mau train va 16 mau test.

| Threshold | Accuracy | Precision | Recall | F1 |
|---:|---:|---:|---:|---:|
| 0.55 | 0.688 | 1.000 | 0.375 | 0.545 |
| 0.40 | 0.875 | 1.000 | 0.750 | 0.857 |

Threshold 0.55 bo sot 5/8 DGA trong holdout. Ket qua chua co false positive
chi phan anh tap test benign rat nho, khong chung minh precision thuc te 100%.

## Ket qua ML baseline

Logistic Regression dung cung holdout va threshold 0.50:

| Detector | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Heuristic | 0.688 | 1.000 | 0.375 | 0.545 |
| Logistic Regression | 0.938 | 1.000 | 0.875 | 0.933 |

Model ML tim duoc 7/8 DGA va bo sot `silentmeadow.test`. File `.joblib` duoc
tao lai bang `train_model.py` va bi Git ignore; repository chi luu metadata,
feature weights va [bao cao danh gia](reports/ml_baseline.md).

## Han che

- Dataset nho va phan lon duoc chuan bi/mô phong thu cong.
- ML baseline moi hoc lexical features, chua hoc chuoi ky tu truc tiep.
- Dictionary DGA co the trong giong domain thong thuong.
- Hostname CDN/tracking co the trong ngau nhien va gay false positive.
- Chua dung DNS context nhu source IP, NXDOMAIN, tan suat va network flow.
