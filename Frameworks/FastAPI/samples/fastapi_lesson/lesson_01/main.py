from fastapi import FastAPI

# インスタンス生成
app = FastAPI()


# エンドポイント
@app.get("/")
async def get_hello():
    return {"message": "Hello World"}
