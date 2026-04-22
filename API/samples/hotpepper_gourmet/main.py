import pandas as pd
import requests

# 定数の設定
API_URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
API_KEY = "取得したAPIキーを入力する"
OUTPUT_FILE = "hotpepper_shop_list.csv"

# 検索クエリの設定
SEARCH_PARAMS = {
    "key": API_KEY,
    "keyword": "代々木上原",
    "count": 20,
    "format": "json",
}

# 出力するカラムの設定
OUTPUT_COLUMNS = ["name", "address", "non_smoking"]


def fetch_shop_list(url: str, params: dict) -> list[dict]:
    """
    ホットペッパーグルメサーチAPIを呼び出してお店のリストを返す。
    この関数の戻り値を convert_to_dataframe() に渡すことで整形できる。

    Args:
        url: APIのエンドポイントURL
        params: 検索クエリパラメータ

    Returns:
        お店情報の辞書リスト

    Raises:
        requests.exceptions.RequestException: 通信エラーが発生した場合
        ValueError: レスポンスのステータスコードが200以外の場合
    """
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise ValueError(f"リクエストが失敗しました： {response.status_code}")

    return response.json()["results"]["shop"]


def convert_to_dataframe(shop_list: list[dict], columns: list[str]) -> pd.DataFrame:
    """
    お店のリストから必要なカラムのみを持つDataFrameを返す。
    fetch_shop_list() の戻り値をそのまま shop_list に渡すことができる。

    Args:
        shop_list: お店情報の辞書リスト
        columns: 抽出するカラム名のリスト

    Returns:
        指定カラムのみを持つDataFrame
    """
    df = pd.DataFrame(shop_list)
    return df[columns]


def save_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    DataFrameをCSVファイルに保存する。

    Args:
        df: 保存するDataFrame
        output_path: 出力先のファイルパス
    """
    df.to_csv(output_path, index=False)
    print(f"CSVを出力しました： {output_path}")


# APIからお店リストを取得する
try:
    shop_list = fetch_shop_list(API_URL, SEARCH_PARAMS)

    # DataFrameに変換して必要なカラムのみ抽出する
    shop_df = convert_to_dataframe(shop_list, OUTPUT_COLUMNS)

    # CSVに出力する
    save_to_csv(shop_df, OUTPUT_FILE)

except (requests.exceptions.RequestException, ValueError) as e:
    print(f"エラーが発生しました: {e}")
