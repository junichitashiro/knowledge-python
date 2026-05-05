from fastapi import FastAPI, HTTPException
from book_schemas import BookSchema, BookResponseSchema

app = FastAPI()

# ------------------------------
# データベースのダミー
# ------------------------------
books: list[BookResponseSchema] = [
    BookResponseSchema(id=1, title="しろたんの世界へ", category="technical"),
    BookResponseSchema(id=2, title="しろたんナゾトキブック", category="technical"),
    BookResponseSchema(id=3, title="しろたんの大冒険", category="comics"),
    BookResponseSchema(id=4, title="しろたんふわふわなまいにち", category="comics"),
    BookResponseSchema(id=5, title="しろたんのんびりまったり塗り絵", category="magazine"),
    BookResponseSchema(id=6, title="しろたんほわほわお部屋ライトブック", category="magazine"),
]


# 追加用エンドポイント
@app.post("/books/", response_model=BookResponseSchema)
def create_book(book: BookSchema) -> BookResponseSchema:
    """
    書籍を追加するためのエンドポイント

    Args:
        book (BookSchema): ダミーの書籍データ

    Returns:
        BookResponseSchema: 登録した書籍データ
    """
    # 書籍IDを作成
    new_book_id = max([book.id for book in books], default=0) + 1
    # 新しい書籍を作成
    new_book = BookResponseSchema(id=new_book_id, **book.model_dump())
    # ダミーデータに追加
    books.append(new_book)

    return new_book


# 全件取得用エンドポイント
@app.get("/books/", response_model=list[BookResponseSchema])
def read_books() -> list[BookResponseSchema]:
    """
    書籍情報を全件取得するエンドポイント

    Returns:
        list[BookResponseSchema]: ダミーの書籍データ
    """
    return books


# 抽出用エンドポイント
@app.get("/books/{book_id}", response_model=BookResponseSchema)
def read_book(book_id: int) -> BookResponseSchema:
    """
    IDに対応する書籍情報を取得するエンドポイント

    Args:
        book_id (int): 書籍ID

    Raises:
        HTTPException: 書籍が見つからなかった場合の返却値

    Returns:
        BookResponseSchema: 対応するIDの書籍データ
    """
    for book in books:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")


# 更新用エンドポイント
@app.put("/books/{book_id}", response_model=BookResponseSchema)
def update_book(book_id: int, book: BookSchema) -> BookResponseSchema:
    """
    IDに対応する書籍情報を更新するエンドポイント

    Args:
        book_id (int): 書籍ID
        book (BookSchema): ダミーの書籍データ

    Raises:
        HTTPException: 書籍が見つからなかった場合の返却値

    Returns:
        BookResponseSchema: 更新した書籍のデータ
    """
    for index, existing_book in enumerate(books):
        if existing_book.id == book_id:
            updated_book = BookResponseSchema(id=book_id, **book.model_dump())
            books[index] = updated_book
            return updated_book

    raise HTTPException(status_code=404, detail="Book not found")


# 削除用エンドポイント
@app.delete("/books/{book_id}", response_model=BookResponseSchema)
def delete_book(book_id: int) -> BookResponseSchema:
    """
    IDに対応する書籍情報を削除するエンドポイント

    Args:
        book_id (int): 書籍ID

    Raises:
        HTTPException: 書籍が見つからなかった場合の返却値

    Returns:
        BookResponseSchema: 削除した書籍のデータ
    """
    for index, book in enumerate(books):
        if book.id == book_id:
            books.pop(index)
            return book

    raise HTTPException(status_code=404, detail="Book not found")
