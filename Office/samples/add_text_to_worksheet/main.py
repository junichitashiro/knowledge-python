import pandas as pd
from pathlib import Path

# 読み込み対象ファイル
TEXT_FILE = Path("sample.txt")
EXCEL_FILE = Path("sample.xlsx")
SHEET_NAME = "Sheet1"


# テキストファイルの読み込み（区切り文字を自動判定）
def detect_separator(file_path: Path) -> str | None:
    """先頭行を読んで区切り文字を判定する。"""
    with open(file_path, encoding="utf-8") as f:
        first_line = f.readline()
    if "\t" in first_line:
        return "\t"
    if "," in first_line:
        return ","
    return None


def load_text_as_dataframe(file_path: Path) -> pd.DataFrame:
    """
    テキストファイルをDataFrameとして返す。

    区切り文字（タブ or カンマ）が検出された場合は複数列に分割する。
    検出されない場合は1列のDataFrameとして返す。
    """
    sep = detect_separator(file_path)
    if sep:
        return pd.read_csv(file_path, sep=sep, header=None, encoding="utf-8")

    # 区切り文字なし：1列データとして読み込む
    lines = file_path.read_text(encoding="utf-8").splitlines()
    return pd.DataFrame([line.strip() for line in lines if line.strip()])


# Excelへの書き込み
def write_to_excel(df: pd.DataFrame, excel_path: Path, sheet_name: str) -> None:
    """DataFrameをExcelの指定シートに書き込む。"""
    # シートの存在有無に関わらず mode="a" + if_sheet_exists で統一処理
    write_mode = "a" if excel_path.exists() else "w"
    with pd.ExcelWriter(
        excel_path,
        engine="openpyxl",
        mode=write_mode,
        if_sheet_exists="replace",  # 既存シートは上書き
    ) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)


# --------------------
# メイン処理
# --------------------
df = load_text_as_dataframe(TEXT_FILE)
write_to_excel(df, EXCEL_FILE, SHEET_NAME)

print("書き込み完了")
