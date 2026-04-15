import pandas as pd
from pathlib import Path
from typing import Any, Optional


def load_file(file_path: Path, file_type: str = 'csv', sheet_name: Optional[str] = None, **kwargs) -> Any | pd.DataFrame | None:
    """
    CSVまたはExcelファイルをエラーハンドリング付きで読み込む共通関数
    ヘッダなし1行のファイルを許容する場合は[**kwargs]に[header=None]を指定する

    Args:
        file_path (Path): 読み込むファイルのパス
        file_type (str): ファイルの種類（'csv' または 'excel'）
        sheet_name (Optional[str], optional): Excelファイルの場合は読み込むシート名、省略時（None）は先頭のシートを使用する
        **kwargs: pandasの読み込み関数に渡す追加のキーワード引数

    Returns:
        pd.DataFrame: 読み込んだデータをDataFrameとして返す

    Raises:
        ValueError: データフレームが空の場合に発生
        FileNotFoundError: ファイルが存在しない場合に発生
        pd.errors.EmptyDataError: ファイルが空の場合に発生
        pd.errors.ParserError: ファイルの解析に問題がある場合に発生（CSVのみ）
    """
    try:
        if file_type == 'csv':
            data = pd.read_csv(file_path, **kwargs)
        elif file_type == 'excel':
            if sheet_name is None:
                raise ValueError('Excelファイルの場合はsheet_nameを指定してください。')
            data = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
        else:
            raise ValueError("サポートされていないファイルタイプです。file_typeは'csv'または'excel'で指定してください。")

        # データフレームが空でないことを確認
        if data.empty:
            raise ValueError('ファイルは正常に読み込まれましたが、データが含まれていません。')

        return data

    except FileNotFoundError:
        print(f'エラー: 指定されたパス {file_path} にファイルが見つかりませんでした。')
        raise

    except pd.errors.EmptyDataError:
        print('エラー: ファイルが空です。')
        raise

    except pd.errors.ParserError as e:
        if file_type == 'csv':
            print(f'エラー: ファイルの解析に失敗しました。詳細: {e}')
            raise

    except ValueError as e:
        print(f'エラー: {e}')
        raise

    except Exception as e:
        print(f'予期しないエラーが発生しました: {e}')
        raise
