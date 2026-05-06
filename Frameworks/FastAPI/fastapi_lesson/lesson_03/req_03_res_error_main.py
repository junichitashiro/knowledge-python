from datetime import datetime

from pydantic import BaseModel, ValidationError


class Event(BaseModel):
    name: str = "未定"
    start_datetime: datetime
    participants: list[str] = []


external_data = {
    "name": "しろたんアニメ化祝賀会",
    # 意図的に不適合の型データを格納する
    "start_datetime": "abcdefg",
    "participants": ["しろたん", "らっこいぬ", "しぇる"],
}

try:
    event = Event(**external_data)
    print("イベント名：", event.name, type(event.name))
    print("開催日時：", event.start_datetime, type(event.start_datetime))
    print("参加者：", event.participants, type(event.participants))
except ValidationError as e:
    print("データのバリデーションエラーが発生しました：", e.errors())
