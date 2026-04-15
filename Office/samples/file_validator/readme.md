# Excelファイル読み込み時のチェック処理

## excel_file_validator.py

### 指定されたExcelファイルとシートの存在を確認し、読み込み可能かを検証する関数

### 処理内容

1. Excelファイルが存在するか確認する
2. 存在する場合はファイルを読み込んでシートが存在するか確認する
3. ファイルとシートの存在チェック結果、読み込みチェック結果を返す

### プログラムの定義

* 関数名: check_excel_file
* 引数
  * file_path (Path): チェックするExcelファイルのパス（Pathオブジェクト）
  * check_sheet_names (list): 存在を確認したいシート名のリスト（デフォルトは['Sheet1']）
* 戻り値
  * bool: ファイルとシートが存在し読み込み可能であれば True、エラーがあれば False

### 補足

* 引数に Path オブジェクトを想定しているが念のため変換処理を行う
* 例外発生時も False を返す

### 使い方

* カレントディレクトリに配置したファイルを対象とした場合のサンプル

```python
import pandas as pd
from pathlib import Path

file_path = Path.cwd() / 'test.xlsx'
check_sheet_names = ['Sheet1', 'Sheet2', 'SheetA', 'SheetB']
file_is_safe = check_excel_file(file_path, check_sheet_names)
print('チェック結果:', file_is_safe)
```
### 可読性を優先した書き方

* 各シートの存在確認処理は別の書き方に変更ができる

```python
sheet_is_exist = {sheet: sheet in excel_file.sheet_names for sheet in check_sheet_names}
```

#### 処理をすべて分解したパターン

```python
sheet_is_exist = {}  # 空の辞書を作成

for sheet in check_sheet_names:  # check_sheet_names の各シートを順に処理
    if sheet in excel_file.sheet_names:  # シートが Excel 内に存在するか判定
        sheet_is_exist[sheet] = True   # 存在する場合 True
    else:
        sheet_is_exist[sheet] = False  # 存在しない場合 False

print(sheet_is_exist)
```

#### 分解を簡易化したパターン

```python
sheet_is_exist = {}

for sheet in check_sheet_names:
    sheet_is_exist[sheet] = sheet in excel_file.sheet_names  # 判定結果を直接格納

print(sheet_is_exist)
```
