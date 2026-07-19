# Episode 02 - Dataset Pipeline and Evaluation Metrics

## Muc tieu

Episode 1 chi cho thay detector chay duoc tren vai domain. Episode 2 bo sung
quy trinh danh gia co the lap lai:

```text
raw domain lists
    -> normalize + validate + deduplicate
    -> labelled CSV
    -> stratified train/test split
    -> heuristic prediction
    -> confusion matrix + precision/recall/F1
```

Baseline hien tai van la rule-based, chua phai Machine Learning. Train split
duoc tao de chuan bi cho Episode 3; heuristic khong hoc tu train split.

## Dataset

Dataset demo gom hai file dau vao:

- `data/raw_legitimate.txt`: domain thong dung va mot so hostname benign mo
  phong co chuoi dai;
- `data/raw_dga_synthetic.txt`: domain DGA mo phong, dung TLD `.test` de tranh
  vo tinh tro den dich vu that.

Day la dataset nho de kiem thu pipeline, khong dai dien cho Internet thuc va
khong du de cong bo do chinh xac cua mot san pham an ninh mang.

Schema cua `data/domains.csv`:

| Field | Y nghia |
|---|---|
| `domain` | Domain da normalize |
| `label` | `legitimate` hoac `dga` |
| `source` | Nguon/loai du lieu |

## Cach chay

Yeu cau Python 3.9 tro len, khong co dependency ben ngoai.

```powershell
cd "Hcriffin/episode 2"

python3 prepare_dataset.py
python3 evaluate.py
python3 evaluate.py --threshold 0.40 --report reports/evaluation-threshold-040.md
python3 -m unittest discover -s tests -v
```

## Y nghia metrics

- True Positive (TP): DGA duoc canh bao dung.
- False Positive (FP): domain benign bi canh bao nham.
- True Negative (TN): domain benign duoc bo qua dung.
- False Negative (FN): DGA bi bo sot.
- Precision: trong cac canh bao, co bao nhieu canh bao dung.
- Recall: trong cac DGA, detector tim thay duoc bao nhieu.
- F1: trung binh dieu hoa giua precision va recall.

Trong IDS, accuracy khong du vi du lieu thuc thuong lech lop. Precision, recall,
F1 va confusion matrix cho thay ro hon chi phi cua canh bao nham va bo sot.

## Ket qua thuc te

Dataset sau khi prepare co 64 mau can bang: 32 `legitimate` va 32 `dga`. Split
co dinh voi seed 42 tao 48 mau train va 16 mau test.

| Threshold | Accuracy | Precision | Recall | F1 |
|---:|---:|---:|---:|---:|
| 0.55 | 0.688 | 1.000 | 0.375 | 0.545 |
| 0.40 | 0.875 | 1.000 | 0.750 | 0.857 |

Kiem thu tu dong: `15/15` test passed.

- [evaluation.md](reports/evaluation.md): threshold mac dinh 0.55.
- [evaluation-threshold-040.md](reports/evaluation-threshold-040.md): threshold 0.40.

Threshold 0.55 bo sot 5/8 DGA trong holdout. Ha threshold xuong 0.40 tang
recall, nhung viec chua co false positive trong 8 mau benign khong chung minh
precision thuc te se la 100%. Episode 3 se dung cung split va metrics de so
sanh voi model ML.

## Han che da biet

- Dataset nho va phan lon duoc chuan bi/mô phong thu cong.
- Domain DGA dang dictionary-based co the trong giong domain thong thuong.
- Hostname benign cua CDN/tracking co the trong ngau nhien va gay false positive.
- Chua co du lieu DNS context nhu source IP, NXDOMAIN, tan suat va network flow.
- Chua co cross-validation hay tap du lieu ben ngoai doc lap.
