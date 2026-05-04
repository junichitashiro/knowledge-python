# 営業日対応を含む日付計算機能

---

## date_difference.py

### 与えられた2つの日付データから日数の差を計算して返す関数

- 関数名: diff
- 引数
  - date1(str)
  - date2(str)
- 形式: 'yyyy/m/d' または 'yyyy/mm/dd'
- 戻り値
  - int: 日数

### 使い方

```python
import date_difference as dd

date1 = "2026/5/4"
date2 = "2026/5/14"
print(dd.diff(date1, date2))
```

### 実行結果

> 10

---

## compare_dates.py

### 与えられた2つの日付データからどちらが未来日であるか判定して結果を返す

- 関数名: compare
- 引数
  - date1(str)
  - date2(str)
- 形式: 'yyyy/m/d' または 'yyyy/mm/dd'
- 戻り値
  - str: 判定結果のメッセージ

### 使い方

```python
import compare_dates as cd

date1 = "2026/5/4"
date2 = "2026/5/14"
print(cd.compare(date1, date2))
```

### 実行結果

> 2026/5/14 の方が未来日です

---

## business_days.py

### 与えられた未来日までの営業日を返す関数

- 関数名: count
- 引数
  - file_path (Path): 非営業日一覧を記載したExcelファイルのパス
  - future_date (str): yyyy/mm/dd 形式の未来日
- 戻り値
  - int: 今日から未来日までの営業日数、過去日の場合は符号がマイナスになる

### インプットとなるExcelファイル

- 非営業日の一覧をExcelファイルのA列に記載する
- シート名を **非営業日** とする
- A1セルはヘッダ名として **非営業日** を記載する
- A2セル以降にyyyy/m/d形式で非営業日を記載する
  - 入力例

    |       |     A     |
    | :---: | :-------: |
    |   1   | 非営業日  |
    |   2   | 2026/1/1  |
    |   3   | 2026/1/2  |
    |   4   | 2026/1/3  |
    |   5   | 2026/1/4  |
    |   6   | 2026/1/10 |
    |   7   | 2026/1/11 |
    |   8   | 2026/1/12 |
    |   …   |     …     |
    |  41   | 2026/4/26 |
    |  42   | 2026/4/29 |
    |  43   | 2026/5/2  |
    |  44   | 2026/5/3  |
    |  45   | 2026/5/4  |
    |  46   | 2026/5/5  |
    |  47   | 2026/5/6  |
    |  48   | 2026/5/9  |
    |  49   | 2026/5/10 |



### 使い方

- 2025年5月4日に実行した場合

```python
import business_days as bd
from pathlib import Path

file_path = Path.cwd() / "non_business_days.xlsx"
future_date = "2026/06/5"
print(bd.count(file_path, future_date))
```

### 実行結果

> 22

---

## business_days.py

### 指定した日付から指定した営業日数を引いた日付を返す関数

- 関数名: calc_minus
- 引数
  - file_path (Path): 非営業日一覧を記載したExcelファイルのパス
  - target_date (str): yyyy/mm/dd 形式のターゲット日
  - business_days_to_subtract (int): 営業日として引く日数
- 戻り値
  - str: 営業日を差し引いた日付 or 非営業日である旨のメッセージ

### インプットとなるExcelファイル

- インプットに関してはcountと同じ

### 使い方

```python
import business_days as bd
from pathlib import Path

file_path = Path.cwd() / "non_business_days.xlsx"
target_date = "2026/05/07"
days_to_subtract = 3

print(bd.calc_minus(file_path, target_date, days_to_subtract))
```

### 実行結果

> 2025/04/28

---

## business_days.py

### 指定した日付に指定した営業日数を足した日付を返す関数

- 関数名: calc_plus
- 引数
  - file_path (Path): 非営業日一覧を記載したExcelファイルのパス
  - target_date (str): yyyy/mm/dd 形式のターゲット日
  - days_to_addition (int): 営業日として加算する日数
- 戻り値
  - str: 営業日を加算した日付 または 非営業日である旨のメッセージ

### インプットとなるExcelファイル

- インプットに関してはcountと同じ

### 使い方

```python
import business_days as bd
from pathlib import Path

file_path = Path.cwd() / "non_business_days.xlsx"
target_date = "2026/05/01"
days_to_addition = 3

print(bd.calc_plus(file_path, target_date, days_to_addition))
```

### 実行結果

> 2026/05/11
