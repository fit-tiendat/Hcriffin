# HCRiffin DGA - Reconstruction Series

Thu muc nay ghi lai qua trinh xay dung lai module phat hien DGA theo tung moc
co the chay va kiem chung doc lap. Day la lo trinh tai cau truc bat dau tu
ngay hien tai, khong phai lich su commit goc cua `Hcriffin-main`.

## Muc tieu

Xay dung he thong phat hien dau hieu Domain Generation Algorithm (DGA) tu DNS
traffic, sau do tich hop vao pipeline giam sat mang:

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

## Ranh gio dong gop

- `Hcriffin-main` la project tham khao dua tren SELKS va cac thanh phan ma
  nguon mo nhu Suricata, Elastic Stack, Scirius, EveBox va Arkime.
- ET Open rules la tap signature cua cong dong, khong phai du lieu huan luyen
  va khong phai rules do nhom tu viet.
- Model `trained_model_7_2_1.h5` trong project tham khao la model co san.
- Chuoi episode nay tap trung vao phan nhom co the tu giai thich, tu kiem thu va
  cai tien: xu ly domain, baseline, danh gia model, doc DNS log, tich hop du
  lieu va trien khai lab.

## Lo trinh episode

| Episode | Noi dung | Ket qua kiem chung | Trang thai |
|---|---|---|---|
| 01 | Problem framing va heuristic baseline | CLI phan tich domain, unit test | Done |
| 02 | Dataset pipeline va metrics | Chia train/test, precision, recall, F1 | Done |
| 03 | Train model ML baseline | Model tu train va bao cao so sanh heuristic | Planned |
| 04 | Tich hop sequence model | Vector hoa ky tu, load/save model, threshold | Planned |
| 05 | Doc DNS event cua Suricata | Parse `eve.json`, loc va khu trung domain | Planned |
| 06 | Tich hop Elasticsearch | Doc `logstash-dns-*`, ghi `classify_domains` | Planned |
| 07 | Hoan thien Logstash pipeline | EVE JSON duoc dua dung vao cac index | Planned |
| 08 | Tich hop Suricata va ET Open | Tao traffic lab va doi chieu alert/rule | Planned |
| 09 | Docker Compose | Dong goi cac service va health check | Planned |
| 10 | Dashboard va danh gia end-to-end | Demo, bang metrics, MITRE mapping, han che | Planned |

Moi episode chi nen duoc commit sau khi da chay test va bo sung phan
`Ket qua thuc te` trong README cua episode do.

Moi thu muc episode la mot snapshot doc lap de reviewer co the chay lai tung
moc. Vi vay mot so code nen tang co the duoc lap lai giua hai episode lien ke.

## Cach dung repository voi nha tuyen dung

Trinh bay day la mot reconstruction series: ban da co mot prototype tich hop,
sau do quay lai tach he thong thanh cac moc nho de kiem thu, tai lieu hoa va
cai tien co he thong. Cach trinh bay nay minh bach hon viec tao commit lui ngay
hoac khang dinh toan bo SELKS la code tu viet.
