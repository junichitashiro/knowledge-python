import datetime
from pathlib import Path

import win32com.client

# ========================================
# 定数
# ========================================
FOLDER_PATH = Path(r"C:\temp")
FILE_PATTERN = "売上報告*_{ymd}.xlsx"
EXPECTED_FILE_COUNT = 3

MAIL_TO = "tokyo@test.com ; nagoya@test.com ; osaka@test.com"
MAIL_SUBJECT_PREFIX = "日時売上報告"
MAIL_BODY_BASE = "売上報告書を送信します。\n"
MAIL_BODY_WARN = "\n※添付ファイルに過不足があります"
MAIL_BODY_FORMAT = 1  # 1:テキスト 2:HTML 3:リッチテキスト


# ========================================
# 関数定義
# ========================================
def get_today_ymd() -> str:
    """処理年月日を yyyymmdd 形式の文字列で返す"""
    return datetime.datetime.today().strftime("%Y%m%d")


def find_attachments(folder: Path, ymd: str) -> list[Path]:
    """
    売上報告ファイルを検索してパスの一覧を返す。

    Args:
        folder: 検索対象のフォルダパス
        ymd: yyyymmdd 形式の処理年月日

    Returns:
        マッチしたファイルパスのリスト
    """
    return list(folder.glob(FILE_PATTERN.format(ymd=ymd)))


def build_mail_body(file_count: int) -> str:
    """
    添付ファイル数に応じたメール本文を返す。

    Args:
        file_count: 添付ファイルの件数

    Returns:
        メール本文の文字列
    """
    body = MAIL_BODY_BASE
    if file_count != EXPECTED_FILE_COUNT:
        body += MAIL_BODY_WARN
    return body


def create_mail(
    outlook,
    ymd: str,
    body: str,
    attachment_paths: list[Path],
):
    """
    Outlookのメールオブジェクトを作成して返す。

    Args:
        outlook: win32com で取得した Outlook.Application オブジェクト
        ymd: 件名に付与する年月日（yyyymmdd）
        body: メール本文
        attachment_paths: 添付するファイルパスのリスト

    Returns:
        設定済みの MailItem オブジェクト
    """
    mail = outlook.CreateItem(0)
    mail.BodyFormat = MAIL_BODY_FORMAT
    mail.To = MAIL_TO
    mail.Subject = MAIL_SUBJECT_PREFIX + ymd
    mail.Body = body

    # 添付ファイルを追加する（win32com は文字列パスを要求するため str() で変換）
    for path in attachment_paths:
        mail.Attachments.Add(str(path))

    return mail


def send_mail(mail) -> None:
    """
    メールを表示して手動送信する。
    自動送信に切り替える場合は display(True) を mail.Send() に変更する。
    """
    mail.display(True)
    # mail.Send()


# ========================================
# メイン処理
# ========================================
def main() -> None:
    ymd = get_today_ymd()
    attachment_paths = find_attachments(FOLDER_PATH, ymd)

    # 添付ファイルの検索結果を表示する
    print("--- 添付ファイル ---")
    for path in attachment_paths:
        print(path)

    # 添付ファイルが0件の場合は送信しない
    if not attachment_paths:
        print("添付ファイルが見つかりませんでした。処理を終了します。")
        return

    body = build_mail_body(len(attachment_paths))
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = create_mail(outlook, ymd, body, attachment_paths)

    send_mail(mail)
    print("--- メール送信完了 ---")


if __name__ == "__main__":
    main()
