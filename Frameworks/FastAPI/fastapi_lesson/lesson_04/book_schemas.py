from pydantic import BaseModel


# 書籍の作成と更新をするスキーマ
class BookSchema(BaseModel):
    title: str
    category: str


# レスポンス用のスキーマ
class BookResponseSchema(BookSchema):
    id: int
