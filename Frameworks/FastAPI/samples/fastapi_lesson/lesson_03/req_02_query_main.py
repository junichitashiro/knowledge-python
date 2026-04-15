from fastapi import FastAPI
from req_02_query_data import get_books_by_category

app = FastAPI()


@app.get("/books/")
async def read_books(category: str | None = None) -> list[dict[str, str]]:
    """
    クエリパラメータで指定されたカテゴリに基づいて書籍情報を検索し、
    結果をJSON形式で返す
    """
    result = get_books_by_category(category)
    return [{"id": book.id, "title": book.title, "category": book.category} for book in result]
