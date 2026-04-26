def parse_input(value: int | str) -> str:
    if isinstance(value, int):
        return f"値は整数型です => {value}:{type(value)}"
    elif isinstance(value, str):
        return f"値は文字列型です => {value}:{type(value)}"
    else:
        raise ValueError(f"引数が整数型、文字列型ではありません => {value}:{type(value)}")


# 呼び出し
parse_input(123)
parse_input("abc")

# 警告が表示されるパターン
# parse_input(123.4)
