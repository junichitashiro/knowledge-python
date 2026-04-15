# ユーザIDと名前の属性を持つクラス
class User:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name


# データベースのダミー
user_list = [
    User(id=1, name="しろたん"),
    User(id=2, name="らっこいぬ"),
    User(id=3, name="しぇる"),
]


def get_user(user_id: int) -> User | None:
    """
    指定されたユーザIDに対するユーザを
    user_list から検索して返す
    """
    for user in user_list:
        if user.id == user_id:
            return user

    return None
