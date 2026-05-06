from fastapi import FastAPI, HTTPException
from req_01_path_data import User, get_user

app = FastAPI()


@app.get("/users/{user_id}")
async def read_user(user_id: int) -> dict:
    """
    ユーザIDをパスパラメータとして受け取り、ユーザ情報を返すエンドポイント
    """
    user: User | None = get_user(user_id)
    if user is None:
        # ユーザが見つからない場合は404エラー
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.id, "username": user.name}
