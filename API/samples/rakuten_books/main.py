import pandas as pd
import requests

# 定数の設定
API_URL = "https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404"
APP_ID = "取得したアプリIDを入力する"

# 検索クエリの設定
SEARCH_PARAMS = {
    "applicationId": APP_ID,
    "format": "json",
    "keyword": "荒木飛呂彦",
}

# 出力するカラムと日本語名の対応
COLUMN_RENAME_MAP = {
    "title": "商品",
    "itemCaption": "キャッチコピー",
    "itemPrice": "価格",
    "availability": "販売可能",
}

# 高額商品の抽出に使う価格の閾値
HIGH_PRICE_THRESHOLD = 2000


def fetch_book_list(url: str, params: dict) -> list[dict]:
    """
    楽天ブックス総合検索APIを呼び出して商品リストを返す。
    この関数の戻り値を convert_to_dataframe() に渡すことで整形できる。

    Args:
        url: APIのエンドポイントURL
        params: 検索クエリパラメータ

    Returns:
        商品情報の辞書リスト

    Raises:
        requests.exceptions.RequestException: 通信エラーが発生した場合
        ValueError: レスポンスのステータスコードが200以外の場合
    """
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise ValueError(f"リクエストが失敗しました： {response.status_code}")

    # レスポンスの構造が {"Items": [{"Item": {...}}, ...]} のため、内側のItemを取り出す
    raw_items = response.json()["Items"]
    return [item["Item"] for item in raw_items]


def convert_to_dataframe(book_list: list[dict], column_rename_map: dict) -> pd.DataFrame:
    """
    商品リストから必要なカラムのみを持つDataFrameを返す。
    fetch_book_list() の戻り値をそのまま book_list に渡すことができる。

    Args:
        book_list: 商品情報の辞書リスト
        column_rename_map: 抽出・リネームするカラムの対応辞書（英語名: 日本語名）

    Returns:
        指定カラムのみを日本語名で持つDataFrame
    """
    df = pd.DataFrame(book_list)
    df = df[list(column_rename_map.keys())]
    return df.rename(columns=column_rename_map)


def analyze_book_data(df: pd.DataFrame, high_price_threshold: int) -> None:
    """
    DataFrameの統計情報の確認と条件抽出を行う。
    convert_to_dataframe() の戻り値をそのまま df に渡すことができる。

    Args:
        df: 商品情報のDataFrame
        high_price_threshold: 高額商品とみなす価格の閾値
    """
    # 商品名で降順に並び替える
    sorted_df = df.sort_values("商品", ascending=False)
    print(sorted_df)

    # 統計量を確認する
    print(df.describe())

    # 閾値を超える高額商品を抽出する
    high_price_df = df[df["価格"] > high_price_threshold]
    print(high_price_df)


# APIから商品リストを取得する
try:
    book_list = fetch_book_list(API_URL, SEARCH_PARAMS)

    # DataFrameに変換して必要なカラムのみ抽出する
    book_df = convert_to_dataframe(book_list, COLUMN_RENAME_MAP)

    # データの確認と操作を行う
    analyze_book_data(book_df, HIGH_PRICE_THRESHOLD)

except (requests.exceptions.RequestException, ValueError) as e:
    print(f"エラーが発生しました: {e}")
