import psycopg2
from psycopg2.extensions import connection as PostgresConnection

# 接続情報の設定（環境に合わせて変更する）
DB_CONFIG = {
    "database": "postgres",
    "user": "postgres",
    "password": "password",
    "host": "127.0.0.1",
    "port": "5432",
}

# 取得条件の設定
TARGET_TABLE = "test_table"
TARGET_COLUMN = "menu"
TARGET_VALUE = "Espresso coffee"


def connect_to_postgres(db_config: dict) -> PostgresConnection | None:
    """
    PostgreSQLに接続してコネクションオブジェクトを返す。
    この関数の戻り値を fetch_rows_by_column() の conn に渡すことができる。

    Args:
        db_config: 接続情報の辞書（database / user / password / host / port）

    Returns:
        接続済みのコネクションオブジェクト。接続失敗時は None
    """
    try:
        return psycopg2.connect(**db_config)

    except Exception as e:
        print(f"Error: データベースに接続できませんでした: {e}")
        return None


def fetch_rows_by_column(
    conn: PostgresConnection,
    table_name: str,
    column_name: str,
    value: str,
) -> list[tuple]:
    """
    指定テーブルの列名と値を条件にレコードを取得して返す。
    connect_to_postgres() の戻り値をそのまま conn に渡すことができる。

    Args:
        conn: psycopg2のコネクションオブジェクト
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
        query = f"SELECT * FROM {table_name} WHERE {column_name} = %s;"
        cursor.execute(query, (value,))
        return cursor.fetchall()

    except Exception as e:
        print(f"Error: テーブルからデータを取得できませんでした: {e}")
        return []


if __name__ == "__main__":
    conn = connect_to_postgres(DB_CONFIG)

    # ※ connect_to_postgres() が None を返した場合は処理を中断する
    if not conn:
        exit(1)

    rows = fetch_rows_by_column(conn, TARGET_TABLE, TARGET_COLUMN, TARGET_VALUE)

    for row in rows:
        print(row)

    conn.close()
