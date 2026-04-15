from datetime import datetime


def diff(date1: str, date2: str) -> int:
    # 日付をyyyy/m/d形式にする
    date_format = '%Y/%m/%d'

    # 日付を変換してから計算する
    d1 = datetime.strptime(date1, date_format)
    d2 = datetime.strptime(date2, date_format)
    delta = abs((d2 - d1).days)

    return delta
