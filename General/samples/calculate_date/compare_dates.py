from datetime import datetime


def compare(date1: str, date2: str) -> str:
    # 日付をyyyy/m/d形式にする
    date_format = '%Y/%m/%d'

    # 日付を変換してから比較する
    d1 = datetime.strptime(date1, date_format)
    d2 = datetime.strptime(date2, date_format)

    if d1 > d2:
        return f'{date1} の方が未来日です'
    elif d1 < d2:
        return f'{date2} の方が未来日です'
    else:
        return '同じ日付です'
