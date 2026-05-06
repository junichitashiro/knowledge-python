def int_str(num1: int, num2: int) -> str:
    result: str = "計算結果："
    return result + str(num1 + num2)


def str_str(name: str) -> str:
    return f"こんにちは、{name}さん！"


def float_float(num1: float, num2: float) -> float:
    return num1 / num2


def list_none(items: list[str]) -> None:
    for item in items:
        print(item)


def list_dict(word_list: list[str]) -> dict[str, int]:
    count_map: dict[str, int] = {}
    for word in word_list:
        count_map[word] = len(word)
    return count_map


# ------------------------------
# 呼び出し
# ------------------------------
result_int_str = int_str(10, 20)
print(result_int_str)

result_str_str = str_str("ゲスト")
print(result_str_str)

result_float_float = float_float(3, 5)
print(result_float_float)

list_none(["abc", "def", "ghi"])

result_list_dict = list_dict(["a", "bb", "ccc"])
print(f"リスト中の文字列：文字数 -> {result_list_dict}")
