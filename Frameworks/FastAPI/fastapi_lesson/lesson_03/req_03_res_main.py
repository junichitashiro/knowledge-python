from datetime import datetime

from pydantic import BaseModel


class Event(BaseModel):
    name: str = "未定"
    start_datetime: datetime
    participants: list[str] = []


external_data = {
    "name": "しろたんアニメ化祝賀会",
    "start_datetime": "2026-10-01 18:00",
    "participants": ["しろたん", "らっこいぬ", "しぇる"],
}

event = Event(**external_data)
print("イベント名：", event.name, type(event.name))
print("開催日時：", event.start_datetime, type(event.start_datetime))
print("参加者：", event.participants, type(event.participants))
