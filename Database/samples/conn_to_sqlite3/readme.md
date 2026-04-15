# SQLite3に接続するためのサンプルコード

---

## create_table_from_csv.py

### 処理概要

CSVファイルからSQLite3のDBを作成する

#### 処理内容

1. CSVファイルの内容をPandasのデータフレームに読み込む
2. DBを新規に作成し、テーブルにデータフレームを書き込む
   1. 既存のテーブル名だった場合は置き換える
3. 確認用のSQLを実行する

#### 作成情報

* DB名：test.db
* テーブル名：menu_list
* カラム名
  * menu
  * category
  * price
  * cal

---

## main.py

### 処理概要

上記 **create_table_from_csv.py** で作成したDBに接続する

#### 処理内容

1. PythonからSQLite3に接続する
2. テーブル名、列名、値を変数に格納する
3. 上記の変数を引数に指定してデータ取得関数を実行する
4. 実行結果を表示する

#### 対象テーブル名

* 上記 create_table_from_csv.py で作成した **menu_list** を対象とする

#### 実行SQL

* 変数 **query** に格納する
