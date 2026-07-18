# Episode 01 - Explainable DGA Baseline

## Bai toan

Malware co the dung Domain Generation Algorithm (DGA) de tao nhieu domain va
tim mot domain da duoc attacker dang ky lam Command and Control (C2). Blacklist
co the bo sot domain moi, vi vay can phan tich dac trung cua chinh chuoi domain.

Episode dau tien tao mot baseline rule-based nho, chay hoan toan local va khong
can dich vu ben ngoai. Baseline nay khong thay the model ML. No tao ra moc so
sanh va giup giai thich cac tin hieu nhu do dai, entropy va ty le chu so.

## MITRE ATT&CK mapping

```text
TA0011 - Command and Control
  -> T1568 - Dynamic Resolution
      -> T1568.002 - Domain Generation Algorithms
```

## Cau truc

```text
episode 1/
|-- app.py
|-- data/
|   `-- sample_domains.csv
|-- src/
|   |-- __init__.py
|   |-- domain_features.py
|   `-- heuristic_detector.py
`-- tests/
    `-- test_detector.py
```

## Cach chay

Yeu cau Python 3.9 tro len. Episode nay khong co dependency ben ngoai.

```powershell
cd "Hcriffin/episode 1"
python3 app.py
python3 app.py google.com asdkjhqwekjhzxc.com
python3 -m unittest discover -s tests -v
```

Ket qua CLI gom:

- `score`: diem nghi ngo tu 0 den 1;
- `verdict`: `suspicious` neu score lon hon hoac bang threshold;
- `reasons`: nhung dieu kien da lam tang diem;
- cac feature cua label dai nhat trong domain.

## Pham vi va han che

- Day la heuristic baseline, khong phai Machine Learning.
- Mot domain bi danh dau chi la dau hieu nghi ngo, khong du de ket luan la C2.
- Domain dung tu ghep, CDN hoac tracking co the gay false positive.
- Cach tach label hien tai chua xu ly day du public suffix nhu `co.uk`.
- Can ket hop source IP, tan suat DNS, NXDOMAIN va network flow de dieu tra.

## Ket qua thuc te

Da kiem tra bang Python 3:

```text
Tests: 7 passed

google.com                0.00  likely-legitimate
microsoft.com             0.00  likely-legitimate
asdkjhqwekjhzxc.com       0.70  suspicious
xk3jh2kasdjf.net          0.40  likely-legitimate
```

Nhan xet: baseline tim duoc mot domain mo phong co chuoi dai va entropy cao,
nhung bo sot mau ngan `xk3jh2kasdjf.net`. False negative nay cho thay heuristic
khong du de bao phu DGA va la co so de episode sau bo sung dataset, metrics va
model ML.
