import sqlite3
from sqlite3 import Connection

# 接続先データベースの設定
DB_NAME = "test.db"

# 取得条件の設定
TARGET_TABLE = "menu_list"
TARGET_COLUMN = "menu"
TARGET_VALUE = "Rooibos tea"


def connect_to_sqlite(db_name: str) -> Connection | None:
    """
    SQLiteに接続してコネクションオブジェクトを返す。
    この関数の戻り値を fetch_rows_by_column() の conn に渡すことができる。

    Args:
        db_name: 接続先のデータベースファイル名

    Returns:
        接続済みのコネクションオブジェクト。接続失敗時は None
    """
    try:
        return sqlite3.connect(db_name)

    except Exception as e:
        print(f"Error: データベースに接続できませんでした: {e}")
        return None


def fetch_rows_by_column(
    conn: Connection,
    table_name: str,
    column_name: str,
    value: str,
) -> list[tuple]:
    """
    指定テーブルの列名と値を条件にレコードを取得して返す。
    connect_to_sqlite() の戻り値をそのまま conn に渡すことができる。

    Args:
        conn: sqlite3のコネクションオブジェクト
        table_name: 検索対象のテーブル名
        column_name: 検索条件に使う列名
        value: 検索条件の値

    Returns:
        取得したレコードのリスト。取得失敗時は空リスト
    """
    try:
        cursor = conn.cursor()

        # テーブル名・列名はプレースホルダーが使えないため文字列フォーマットで埋め込む
        # ※ 外部入力をそのまま渡す場合はSQLインジェクションに注意すること
        query = f"SELECT * FROM {table_name} WHERE {column_name} = ?;"
        cursor.execute(query, (value,))
        return cursor.fetchall()

    except Exception as e:
        print(f"Error: テーブルからデータを取得できませんでした: {e}")
        return []


if __name__ == "__main__":
    conn = connect_to_sqlite(DB_NAME)

    if not conn:
        exit(1)

    rows = fetch_rows_by_column(conn, TARGET_TABLE, TARGET_COLUMN, TARGET_VALUE)

    for row in rows:
        print(row)

    conn.close()
