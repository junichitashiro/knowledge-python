# ファイル読み込み時のエラーハンドリング

## file_reader.py

### CSVまたはExcelファイル読み込み時の一般的なエラーハンドリング機能をまとめた関数

### 処理内容

1. CSVまたはExcelファイルをエラーハンドリング付きで読み込む
2. エラーなしで読み込めた場合はデータの内容を返す
3. エラーが発生した場合はエラーハンドリングをしてエラーメッセージを返す

### プログラムの定義

* 関数名: load_file
* 引数
  * file_path (Path): 読み込むファイルのパス
  * file_type (str): ファイルの種類（'csv' または 'excel'）
  * sheet_name (Optional[str], optional): Excelファイルの場合は読み込むシート名、省略時（None）は先頭のシートを使用する
  * **kwargs: pandasの読み込み関数に渡す追加のキーワード引数
* 戻り値
  * pd.DataFrame: 読み込んだデータ

### 使い方

* カレントディレクトリに配置したファイルを対象とした場合のサンプル
* ヘッダのみのファイルを許容する場合は __**kwargs__ に **header=None** を指定する

#### CSVファイルの場合

```python
import file_reader
from pathlib import Path


try:
    csv_file_path = (Path.cwd() / 'sample.csv')
    df_csv = file_reader.load_file(csv_file_path, file_type='csv')
    print('CSVファイルの内容:')
    print(df_csv.head())

except Exception as e:
    print('CSVファイルの読み込みに失敗しました:', e)
```

#### Excelファイルの場合

```python
import file_reader
from pathlib import Path


try:
    excel_file_path = (Path.cwd() / 'sample.xlsx')
    sheet_name = 'Sheet1'
    df_excel = file_reader.load_file(excel_file_path, file_type='excel', sheet_name=sheet_name)
    print('Excelファイルの内容:')
    print(df_excel.head())

except Exception as e:
    print('Excelファイルの読み込みに失敗しました:', e)
```
