import sqlite3

import pandas as pd

# CSVをデータフレームに読み込む
df = pd.read_csv("input.csv")

# データフレームをテーブルに書き込む
db_name = "test.db"
conn = sqlite3.connect(db_name)
df.to_sql("menu_list", conn, if_exists="replace")

cur = conn.cursor()

# 確認用のSQLを実行する
query = "select * from menu_list"
for row in cur.execute(query):
    print(row)

conn.close()
