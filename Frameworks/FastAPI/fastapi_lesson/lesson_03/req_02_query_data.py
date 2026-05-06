# 書籍情報を表わすクラス
class Book:
    def __init__(self, id: str, title: str, category: str) -> None:
        self.id = id
        self.title = title
        self.category = category


# ダミーの書籍情報リスト
books = [
    Book(id="1", title="しろたんの世界へ", category="technical"),
    Book(id="2", title="しろたんナゾトキブック", category="technical"),
    Book(id="3", title="しろたんの大冒険", category="comics"),
    Book(id="4", title="しろたんふわふわなまいにち", category="comics"),
    Book(id="5", title="しろたんのんびりまったり塗り絵", category="magazine"),
    Book(id="6", title="しろたんほわほわお部屋ライトブック", category="magazine"),
]


def get_books_by_category(category: str | None = None) -> list[Book]:
    """
    カテゴリに基づいて書籍を検索する関数
    カテゴリの指定がない場合は全ての書籍を返す
    """
    if category is None:
        return books
    else:
        return [book for book in books if book.category == category]
