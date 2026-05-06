import time
import asyncio


# 同期処理の例
def sync_task(name, sleep_time) -> None:
    print(f"タスク開始：{name}, 処理時間：{sleep_time}")
    time.sleep(sleep_time)
    print(f"タスク終了:{name}")


def run_sync_tasks() -> None:
    sync_task("タスク1", 5)
    sync_task("タスク2", 3)
    sync_task("タスク3", 2)


print("同期処理の例：")
run_sync_tasks()


# 非同期処理の例
async def async_task(name, sleep_time) -> None:
    print(f"タスク開始：{name}, 処理時間：{sleep_time}")
    await asyncio.sleep(sleep_time)
    print(f"タスク終了：{name}")


async def run_async_tasks() -> None:
    await asyncio.gather(
        async_task("タスクA", 5),  #
        async_task("タスクB", 3),  #
        async_task("タスクC", 2),  #
    )


print("非同期処理の例：")
asyncio.run(run_async_tasks())
