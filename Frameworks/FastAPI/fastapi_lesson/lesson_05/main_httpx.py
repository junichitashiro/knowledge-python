from typing import Any

from fastapi import FastAPI
import asyncio
import httpx

app = FastAPI()


# 郵便番号API実行関数
async def fetch_address(zip_code: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://zipcloud.ibsnet.co.jp/api/search?zipcode={zip_code}")
    return response.json()


# エンドポイント
@app.get("/addresses/")
async def get_addresses() -> list[Any]:
    zip_codes = ["0600000", "1000001", "9000000"]
    return await asyncio.gather(*(fetch_address(zip_code) for zip_code in zip_codes))
