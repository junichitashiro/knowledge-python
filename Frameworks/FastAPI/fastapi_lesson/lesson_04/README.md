# CRUD 処理

---

## RESTful API

### REST（Representational State Transfer）

- Webサービスの設計思想・アーキテクチャスタイル
- この原則に従って設計されたAPIを **RESTful API** と呼ぶ
- APIの一貫性・拡張性・保守性を高めるための基盤

---

## RESTの4原則

### ステートレス（Stateless）

サーバーはリクエスト間の状態を保持しないという原則

- 各リクエストはそれ単体で完結する
- 認証情報（トークンなど）も毎回送信する
- セッション管理が不要になり、シンプルな構成になる

---

### 統一インターフェース（Uniform Interface）

クライアントとサーバーのやり取りを標準化された方法で行うという原則

- 全てのAPIリソースが一貫した方法で操作される
- APIの使い方が統一されるため、学習コストと実装のばらつきを抑えられる
- 操作はHTTPメソッドで表現する

#### RESTで用いられるHTTPメソッド

| 処理 | HTTPメソッド | CRUD操作 | CRUD処理 | 安全性 | 冪等性 |
| ---- | ------------ | -------- | -------- | :----: | :----: |
| 登録 | POST         | CREATE   | 作成     |   ×    |   ×    |
| 取得 | GET          | READ     | 読み取り |   ○    |   ○    |
| 更新 | PUT          | UPDATE   | 更新     |   ×    |   ○    |
| 削除 | DELETE       | DELETE   | 削除     |   ×    |   ○    |

#### 安全性と冪等性

- 安全性
  - Webサイトやサーバーのデータを変更しない特性
- 冪等性
  - 同じ操作を何度しても最初の1回目の操作と同じ結果になる特性

---

### アドレサビリティ（Addressability）

すべての情報が一意なURIを持つという原則

- 提供する情報をURIで公開できる
- 公開されたリソースにURIでアクセスできる

---

### コネクタビリティ（Connectability）

やりとりされる情報の中にリンク情報を含めることができるという原則

- リンクをたどって別の情報に接続できる
- 異なるシステム間での情報連携が容易になる

---

## Pydanticの利用

### Field関数を使ったチェック機能

| 引数        | 説明                                 |
| ----------- | ------------------------------------ |
| ...,        | この記載がある項目は必須入力値となる |
| default     | デフォルト値                         |
| description | フィールドの説明                     |
| examples    | フィールの入力値の具体例             |
| gt          | greater then                         |
| lt          | less than                            |
| ge          | greater than or equal to             |
| le          | less than or equal to                |
| min_length  | 文字列の最小長さ                     |
| max_length  | 文字列の最大長さ                     |

### Field関数を使ったサンプルプログラム

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


# データ構造
class BookSchema(BaseModel):
    title: str = Field(..., description="タイトルの指定：必須", examples=["しろたんとらっこいぬ"])
    category: str = Field(..., description="カテゴリの指定：必須", examples=["comics"])
    publish_year: int = Field(default=2025, description="出版年の指定：任意", examples=[2025])
    price: float = Field(..., gt=0, le=10000, description="価格の指定：0 < 価格 <=10000：必須", examples=[750])


# エンドポイント
@app.post("/books/", response_model=BookSchema)
async def create_book(book: BookSchema):
    return book
```
