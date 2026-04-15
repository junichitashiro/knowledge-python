from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


def non_business_days_read(file_path: Path) -> pd.DataFrame:
    """
    Excelファイルから「非営業日マスタ」シートを読み取り、非営業日の一覧をDataFrameとして返す関数。
    シートが存在しない場合、または「非営業日」列がない場合はエラーを発生させる。

    Returns:
        pd.DataFrame: 非営業日（yyyy/mm/dd 形式）のDataFrame

    Raises:
        ValueError: シートまたは必要な列が存在しない場合
    """
    sheet_name = '非営業日マスタ'

    # Excelファイル内のシート一覧を取得して存在確認
    try:
        sheet_names = pd.ExcelFile(file_path).sheet_names
    except Exception as e:
        raise ValueError(f'Excelファイルの読み込みに失敗しました: {e}')

    if sheet_name not in sheet_names:
        raise ValueError(f'【{sheet_name}】シートがありません')

    # 指定シートからA列を読み込む
    df = pd.read_excel(file_path, sheet_name=sheet_name, usecols='A')

    if '非営業日' not in df.columns:
        raise ValueError(f'【{sheet_name}】シートのA列に「非営業日」ヘッダが必要です')

    df['非営業日'] = pd.to_datetime(df['非営業日']).dt.strftime('%Y/%m/%d')
    return df


def count(file_path: Path, future_date: str) -> int:
    """
    与えられた未来日までの営業日数を返す関数。

    Args:
        file_path (Path): 非営業日一覧を記載したExcelファイルのパス
        future_date (str): yyyy/mm/dd 形式の未来日

    Returns:
        int: 今日から未来日までの営業日数
    """
    today = datetime.now().date()
    future_date_obj = datetime.strptime(future_date, '%Y/%m/%d').date()

    # 非営業日一覧を取得し、datetime型に変換する
    df = non_business_days_read(file_path)
    non_business_days = pd.to_datetime(df.iloc[:, 0], format='%Y/%m/%d').dt.date

    count = sum(today <= d <= future_date_obj for d in non_business_days)
    # 未来日までの日数を計算する　※営業日の考え方で加算日数を調整する
    total_days = (future_date_obj - today).days + 1

    return total_days - count


def calc_minus(file_path: Path, target_date: str, days_to_subtract: int) -> str:
    """
    指定日から営業日ベースで指定日数を引いた日付を返す関数。
    対象日が非営業日の場合はその旨を表示する。

    Args:
        file_path (Path): Excelファイルのパス
        target_date (str): yyyy/mm/dd 形式のターゲット日
        days_to_subtract (int): 営業日として引く日数

    Returns:
        str: 営業日を差し引いた日付
    """
    # 非営業日一覧を取得し、datetime型に変換する
    df = non_business_days_read(file_path)
    non_business_days = pd.to_datetime(df.iloc[:, 0], format='%Y/%m/%d').dt.strftime('%Y/%m/%d').tolist()

    # 指定日の非営業日チェック
    if target_date in non_business_days:
        print('指定した日付は非営業日です')

    target_date_obj = datetime.strptime(target_date, '%Y/%m/%d')

    while days_to_subtract > 0:
        target_date_obj -= timedelta(days=1)
        if target_date_obj.strftime('%Y/%m/%d') not in non_business_days:
            days_to_subtract -= 1

    return target_date_obj.strftime('%Y/%m/%d')


def calc_plus(file_path: Path, target_date: str, days_to_addition: int) -> str:
    """
    指定日から営業日ベースで指定日数を足した日付を返す関数。
    対象日が非営業日の場合はその旨を表示する。

    Args:
        file_path (Path): 非営業日一覧が記載されたExcelファイルのパス
        target_date (str): yyyy/mm/dd 形式のターゲット日
        days_to_addition (int): 営業日として加算する日数

    Returns:
        str: 営業日を加算した日付
    """
    # 非営業日一覧を取得し、datetime型に変換する
    df = non_business_days_read(file_path)
    non_business_days = pd.to_datetime(df.iloc[:, 0], format='%Y/%m/%d').dt.strftime('%Y/%m/%d').tolist()

    # 指定日の非営業日チェック
    if target_date in non_business_days:
        print('指定した日付は非営業日です')

    target_date_obj = datetime.strptime(target_date, '%Y/%m/%d')

    while days_to_addition > 0:
        target_date_obj += timedelta(days=1)
        if target_date_obj.strftime('%Y/%m/%d') not in non_business_days:
            days_to_addition -= 1

    return target_date_obj.strftime('%Y/%m/%d')


from pathlib import Path

file_path = Path.cwd() / 'non_business_days.xlsx'
target_date = '2025/11/29'
days_to_subtract = 3

print(calc_minus(file_path, target_date, days_to_subtract))
print(calc_plus(file_path, target_date, days_to_subtract))

future_date = '2025/11/30'
print(count(file_path, future_date))

