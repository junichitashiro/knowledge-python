import pandas as pd
import requests

# 定数の設定
API_URL = "https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404"
APP_ID = "取得したアプリIDを入力する"

# ----------------------------------------
# 検索クエリの設定
# ----------------------------------------
params = {"applicationId": APP_ID, "format": "json", "keyword": "荒木飛呂彦"}

# リクエストの実行
try:
    res = requests.get(API_URL, params)

    if res.status_code == 200:
        result = res.json()

        # itemsのリスト情報だけ格納し直す
        items = result["Items"]

        # そのままデータフレームに格納するとすべて1カラムに入ってしまうため編集する
        items = [item["Item"] for item in items]
        df = pd.DataFrame(items)

        # 必要なカラムのみ抽出する
        df = df[["title", "itemCaption", "itemPrice", "availability"]]

        # カラム名を変更する
        new_columns = ["商品", "キャッチコピー", "価格", "販売可能"]
        df.columns = new_columns

        # データを商品名で並び替える
        df.sort_values("商品", ascending=False)

        # 統計量を確認する
        df.describe()

        # データを抽出する
        df[df["価格"] > 2000]

    else:
        print(f"リクエストが失敗しました： {res.status_code}")

except requests.exceptions.RequestException as e:
    print(f"リクエストエラーが発生しました: {e}")
except Exception as e:
    print(f"エラーが発生しました: {e}")
