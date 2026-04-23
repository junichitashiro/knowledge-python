import sqlite3

import pandas as pd

# 定数の設定
INPUT_CSV = "input.csv"
DB_NAME = "test.db"
TABLE_NAME = "menu_list"


def load_csv(file_path: str) -> pd.DataFrame:
    """
    CSVファイルを読み込んでDataFrameを返す。

    Args:
        file_path: 読み込むCSVファイルのパス

    Returns:
        読み込んだDataFrame
    """
    return pd.read_csv(file_path)


def write_to_sqlite(df: pd.DataFrame, db_name: str, table_name: str) -> None:
    """
    DataFrameをSQLiteのテーブルに書き込む。
    テーブルが既に存在する場合は上書きする。

    Args:
        df: 書き込むDataFrame
        db_name: 接続先のデータベースファイル名
        table_name: 書き込み先のテーブル名
    """
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()


def verify_table(db_name: str, table_name: str) -> None:
    """
    テーブルの全レコードを取得して表示する（書き込み結果の確認用）。

    Args:
        db_name: 接続先のデータベースファイル名
        table_name: 確認対象のテーブル名
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for row in cursor.execute(f"SELECT * FROM {table_name};"):
        print(row)

    conn.close()


if __name__ == "__main__":
    # CSVを読み込んでSQLiteのテーブルに書き込む
    menu_df = load_csv(INPUT_CSV)
    write_to_sqlite(menu_df, DB_NAME, TABLE_NAME)

    # 書き込み結果を確認する
    verify_table(DB_NAME, TABLE_NAME)
