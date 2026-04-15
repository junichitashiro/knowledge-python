from pathlib import Path
from typing import Sequence

import pandas as pd


def check_excel_file(file_path: Path, check_sheet_names: Sequence[str] | None = None) -> bool:
    """
    指定されたExcelファイルが存在し、必要に応じて特定のシートが含まれているかを確認する。

    Args:
        file_path (Path): チェック対象のExcelファイルのパス（Pathオブジェクト）。
        check_sheet_names (Sequence[str] | None, optional): 存在を確認したいシート名のリスト。
            指定がない場合はファイルの存在と読み込みのみをチェックする。

    Returns:
        bool: ファイルが存在し、必要なシートがすべて存在する場合は True。
            ファイルが存在しない、開けない、または指定シートが不足している場合は False。
    """
    if check_sheet_names is None:
        check_sheet_names = ['Sheet1']

    file_path = Path(file_path)

    if not file_path.exists():
        print(f'エラー: ファイルが見つかりません -> {file_path}')
        return False

    try:
        with pd.ExcelFile(file_path) as xlsx:
            print(f'ファイルを正常に読み込みました -> {file_path.name}')

            sheet_names = xlsx.sheet_names
            sheet_is_exist = {sheet: sheet in sheet_names for sheet in check_sheet_names}

            if not all(sheet_is_exist.values()):
                print('エラー: 存在しないシートがあります')
                print(sheet_is_exist)
                return False

            print('チェック対象シートはすべて存在します')
            print(check_sheet_names)
            return True

    except FileNotFoundError:
        print(f'エラー: ファイルが見つかりません -> {file_path}')
    except PermissionError:
        print(f'エラー: ファイルへのアクセスが拒否されました -> {file_path}')
    except ValueError as e:
        print(f'エラー: {e}')
    except Exception as e:
        print(f'予期しないエラーが発生しました: {e}')

    return False
