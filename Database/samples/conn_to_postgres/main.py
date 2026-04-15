import psycopg2


# PostgreSQLへの接続
def conn_to_postgres():
    try:
        conn = psycopg2.connect(
            # 接続情報は適宜修正する
            database="postgres",
            user="postgres",
            password="password",
            host="127.0.0.1",
            port="5432",
        )
        return conn

    except Exception as e:
        print("Error: データベースに接続できませんでした")
        print(e)
        return None


# テーブルからデータを取得する
def get_data_from_table(conn, table_name, column_name, value):
    try:
        cur = conn.cursor()
        query = f"select * from {table_name} where {column_name} = %s;"
        cur.execute(query, (value,))
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
        table_name = "test_table"
        column_name = "menu"
        value = "Espresso coffee"

        rows = get_data_from_table(conn, table_name, column_name, value)

        if rows:
            for row in rows:
                print(row)

        # データベースとの接続を終了する
        conn.close()
