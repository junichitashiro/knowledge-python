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
