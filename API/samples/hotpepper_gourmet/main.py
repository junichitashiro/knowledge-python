import pandas as pd
import requests

# 定数の設定
API_URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
API_KEY = "取得したAPIキーを入力する"

# 検索クエリの設定
params = {"key": API_KEY, "keyword": "代々木上原", "count": 20, "format": "json"}

# リクエストの実行
try:
    res = requests.get(API_URL, params=params)

    if res.status_code == 200:
        result = res.json()

        # shopのリスト情報だけ格納し直す
        items = result["results"]["shop"]
        df = pd.DataFrame(items)

        # 必要なカラムのみ抽出する
        df = df[["name", "address", "non_smoking"]]

        # CSVに出力する
        df.to_csv("hotpepper_shop_list.csv", index=False)

    else:
        print(f"リクエストが失敗しました： {res.status_code}")

except requests.exceptions.RequestException as e:
    print(f"リクエストエラーが発生しました: {e}")
except Exception as e:
    print(f"エラーが発生しました: {e}")
