# HCRiffin DGA Detection

HCRiffin la project nghien cuu phat hien dau hieu Domain Generation Algorithm
(DGA) tu DNS traffic. Repository nay duoc phat trien lien tuc trong mot cay ma
nguon chinh tai `main/`; moi commit bo sung hoac cai tien truc tiep code hien tai.

## Muc tieu kien truc

```text
DNS traffic -> Suricata -> EVE JSON -> Logstash -> Elasticsearch
                                                    |
                                                    v
                                             DGA detector
                                                    |
                                                    v
                                             Dashboard/alert
```

He thong tap trung vao detection va investigation. Chuc nang tu dong chan
domain, IP hoac co lap may tram chua nam trong pham vi ban dau.

## Cau truc repository

```text
Hcriffin/
|-- main/                  # Code hien tai va duy nhat cua project
|   |-- data/              # Raw data va dataset da chuan hoa
|   |-- reports/           # Ket qua danh gia co the lap lai
|   |-- src/               # Feature extraction, detector, data, metrics
|   |-- tests/             # Unit tests
|   |-- app.py             # CLI phan tich domain
|   |-- prepare_dataset.py # Tao labelled dataset
|   |-- evaluate.py        # Danh gia heuristic tren holdout
|   |-- train_model.py     # Train va so sanh ML baseline
|   `-- predict_ml.py      # Chay inference tu model da train
`-- README.md
```

## Tien do

| Milestone | Noi dung | Ket qua kiem chung | Trang thai |
|---|---|---|---|
| 01 | Problem framing va heuristic baseline | CLI phan tich domain, 7 tests | Done |
| 02 | Dataset pipeline va metrics | Split, confusion matrix, precision/recall/F1 | Done |
| 03 | Train model ML baseline | Logistic Regression, report, 18 tests | Done |
| 04 | Tich hop sequence model | Vector hoa ky tu, load/save model, threshold | Planned |
| 05 | Doc DNS event cua Suricata | Parse `eve.json`, loc va khu trung domain | Planned |
| 06 | Tich hop Elasticsearch | Doc `logstash-dns-*`, ghi `classify_domains` | Planned |
| 07 | Hoan thien Logstash pipeline | EVE JSON duoc dua dung vao cac index | Planned |
| 08 | Tich hop Suricata va ET Open | Tao traffic lab va doi chieu alert/rule | Planned |
| 09 | Docker Compose | Dong goi cac service va health check | Planned |
| 10 | Dashboard va danh gia end-to-end | Demo, metrics, MITRE mapping, han che | Planned |

## Chay nhanh

Yeu cau Python 3.9 tro len.

```bash
cd main
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py google.com asdkjhqwekjhzxc.test
python3 prepare_dataset.py
python3 evaluate.py
python3 train_model.py
python3 predict_ml.py google.com asdkjhqwekjhzxc.test
python3 -m unittest discover -s tests -v
```

## Ranh gio dong gop

- SELKS, Suricata, Elastic Stack, Scirius, EveBox va Arkime la cac project ma
  nguon mo duoc nghien cuu de tich hop o cac milestone sau.
- ET Open rules la signature cua cong dong, khong phai du lieu huan luyen va
  khong phai rules do nhom tu viet.
- Model `trained_model_7_2_1.h5` trong prototype tham khao la model co san.
- Phan code trong repository nay tap trung vao pipeline du lieu, baseline,
  metrics, tests va cac buoc tich hop co the giai thich va kiem chung.
