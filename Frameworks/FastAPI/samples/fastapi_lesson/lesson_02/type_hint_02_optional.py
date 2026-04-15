from typing import Optional


def get_profile(email: str, username: Optional[str] = None, age: Optional[int] = None) -> dict[str, str | int]:
    """
    ユーザー情報を保持するプロフィールを返却する
    """
    profile: dict[str, str | int] = {"email": email}
    if username:
        profile["username"] = username
    if age:
        profile["age"] = age
    return profile


# 呼び出し

# email だけ指定
user_profile = get_profile(email="shirotan@fuwafuwa.com")
print(user_profile)

# 全て指定
user_profile = get_profile(email="shirotan@fuwafuwa.com", username="しろたん", age=8)
print(user_profile)
