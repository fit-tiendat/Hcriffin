# HCRiffin DGA Detector

Day la code hien tai cua module phat hien domain co dau hieu DGA. Phien ban
hien tai gom mot baseline heuristic co the giai thich va pipeline danh gia co
the lap lai. Chua co Suricata, Elasticsearch hay model ML trong runtime nay.

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
       lexical heuristic detector
                    |
                    v
  confusion matrix + precision/recall/F1
```

Train split duoc tao de san sang cho model o milestone tiep theo. Baseline
heuristic hien tai khong hoc tu train split.

## Cau truc

```text
main/
|-- app.py
|-- prepare_dataset.py
|-- evaluate.py
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
|   `-- metrics.py
`-- tests/
    |-- test_detector.py
    |-- test_dataset.py
    `-- test_metrics.py
```

## Cach chay

Yeu cau Python 3.9 tro len, khong co dependency ben ngoai.

```powershell
cd main

python3 app.py google.com asdkjhqwekjhzxc.test
python3 prepare_dataset.py
python3 evaluate.py
python3 evaluate.py --threshold 0.40 --report reports/evaluation-threshold-040.md
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

## Han che

- Detector hien tai la rule-based, chua phai Machine Learning.
- Dataset nho va phan lon duoc chuan bi/mô phong thu cong.
- Dictionary DGA co the trong giong domain thong thuong.
- Hostname CDN/tracking co the trong ngau nhien va gay false positive.
- Chua dung DNS context nhu source IP, NXDOMAIN, tan suat va network flow.
