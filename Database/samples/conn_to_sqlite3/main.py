import sqlite3


# SQLiteへの接続
def conn_to_postgres():
    # 接続先データベース
    db_name = "test.db"
    try:
        conn = sqlite3.connect(db_name)
        return conn

    except Exception as e:
        print("Error: データベースに接続できませんでした")
        print(e)
        return None


# テーブルからデータを取得する
def get_data_from_table(conn, table_name, column_name, value):
    try:
        cur = conn.cursor()
        query = f'select * from {table_name} where {column_name} = "{value}"'
        cur.execute(query)
        rows = cur.fetchall()
        return rows

    except Exception as e:
        print("Error: テーブルからデータを取得できませんでした")
        print(e)
        return []


if __name__ == "__main__":
    conn = conn_to_postgres()
    if conn:
        # 取得条件の設定
        table_name = "menu_list"
        column_name = "menu"
        value = "Rooibos tea"

        rows = get_data_from_table(conn, table_name, column_name, value)

        if rows:
            for row in rows:
                print(row)

        # データベースとの接続を終了する
        conn.close()
