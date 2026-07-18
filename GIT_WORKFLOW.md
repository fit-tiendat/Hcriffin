# Git workflow cho reconstruction series

## Nguyen tac

- Dung ngay commit thuc te, khong backdate.
- Moi ngay chi commit phan da chay va da hieu.
- Ghi ro code/tap du lieu/model nao la tham khao hoac ma nguon mo.
- Khong commit log runtime, secret, file `.env`, cache Python hay du lieu nhay cam.
- Truoc khi push, luon xem `git status` va `git diff --staged`.

## Ngay 1 - Episode 01

```powershell
cd Hcriffin
git status
git add README.md GIT_WORKFLOW.md .gitignore "episode 1"
git diff --staged
git commit -m "feat: add explainable DGA heuristic baseline"
git push -u origin main
```

Noi dung co the mo ta trong commit/README:

```text
- Define the DGA detection scope and MITRE ATT&CK mapping.
- Add lexical domain feature extraction.
- Add an explainable heuristic baseline and CLI demo.
- Add synthetic samples and seven unit tests.
```

## Lo trinh commit de xuat

| Ngay | Commit message | Bang chung can co |
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

Nen noi:

> Em bat dau tu mot prototype HCRiffin/SELKS co san, sau do tach lai he thong
> thanh tung milestone de hieu, kiem thu va cai tien phan DGA. Git series ghi
> lai qua trinh reconstruction va engineering cua em tu thoi diem nay.

Khong nen noi:

> Em tu viet toan bo Suricata, Elasticsearch, Scirius va 49 nghin ET rules.

Phan co gia tri nhat de HR danh gia la kha nang ban giai thich data flow, viet
test, do metrics, neu duoc han che va chi ra ro dong gop cua minh.
