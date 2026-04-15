from typing import Annotated


def process_value(value: Annotated[int, "範囲: 0 <= value <= 100"]) -> None:
    if 0 <= value <= 100:
        print(f"値は範囲内です：{value}")
    else:
        raise ValueError(f"範囲外の値です： {value}")


# 呼び出し

# 正常値
process_value(50)

# 異常値
try:
    process_value(150)
except ValueError as e:
    print(e)
