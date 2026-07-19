# Git workflow

## Nguyen tac

- Tat ca code hien tai nam trong `main/`; khong tao snapshot theo episode.
- Moi commit chi gom mot thay doi logic co the giai thich va kiem thu.
- Dung ngay commit thuc te, khong backdate.
- Ghi ro code, dataset, model va rules nao la tham khao hoac ma nguon mo.
- Khong commit log runtime, secret, `.env`, cache Python hay du lieu nhay cam.

## Quy trinh truoc moi commit

```powershell
cd Hcriffin
python3 -m unittest discover -s main/tests -v
git status
git diff

# Chi stage cac file thuoc thay doi hien tai, vi du:
git add main/src/model.py main/tests/test_model.py main/README.md
git diff --staged
git commit -m "feat: train baseline ML domain classifier"
git push origin main
```

Khong nen mac dinh dung `git add .` khi trong workspace con log, dataset lon
hoac file thu nghiem chua kiem tra.

## Lo trinh commit de xuat

| Moc | Commit message | Bang chung can co |
|---|---|---|
| 1 | `feat: add explainable DGA heuristic baseline` | CLI va 7 unit tests |
| 2 | `feat: add dataset preparation and evaluation metrics` | Dataset report, precision/recall/F1 |
| 3 | `feat: train baseline ML domain classifier` | Model artifact va comparison report |
| 4 | `feat: add character sequence inference pipeline` | Batch inference va threshold config |
| 5 | `feat: parse DNS events from Suricata EVE JSON` | Fixture EVE va parser tests |
| 6 | `feat: integrate Elasticsearch DNS source and result sink` | Mapping va integration test |
| 7 | `chore: add Logstash DNS ingestion pipeline` | Config validation va sample index |
| 8 | `feat: integrate Suricata ET Open detection` | Rule source, alert evidence, limitations |
| 9 | `chore: containerize the end-to-end stack` | Compose validation va health checks |
| 10 | `docs: add dashboard, evaluation and MITRE case study` | Screenshots, metrics va demo script |

## Cach trinh bay voi HR

> Em bat dau tu bai toan DGA va mot baseline nho, sau do bo sung dataset,
> metrics, model va tung thanh phan cua network monitoring pipeline. Moi commit
> tren Git the hien mot thay doi da duoc test trong cung codebase `main`.

Khong nhan la tu viet Suricata, Elasticsearch, Scirius hay ET Open rules.
Gia tri dong gop nam o cach tich hop, xu ly du lieu, danh gia, kiem thu va neu
ro han che cua he thong.
