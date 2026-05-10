import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import chromedriver_binary_sync
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# ========================================
# 定数
# ========================================
INPUT_FILE = Path.cwd() / "url_list.txt"
CHROMEDRIVER_DIR = "chromedriver"

# ページ読み込み・スクロール待機の秒数
WAIT_PAGE_LOAD = 30
WAIT_SCROLL = 3
WAIT_NEXT_URL = 3

# XPath テンプレート（{i} に行番号を埋め込んで使用する）
XPATH_TITLE = '//*[@id="title"]/h1/yt-formatted-string'
XPATH_GOOD = (
    "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy"
    "/div[4]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer"
    "/div[3]/ytd-comment-thread-renderer[{i}]/div[1]/ytd-comment-view-model"
    "/div[3]/div[2]/ytd-comment-engagement-bar/div[1]/span"
)
XPATH_COMMENT = (
    "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy"
    "/div[4]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer"
    "/div[3]/ytd-comment-thread-renderer[{i}]/div[1]/ytd-comment-view-model"
    "/div[3]/div[2]/ytd-expander/div/yt-attributed-string/span"
)


# ========================================
# 初期処理
# ========================================
def load_url_list(input_file: Path) -> list[str]:
    """URLリストファイルを読み込んでURL一覧を返す。

    Args:
        input_file: 入力ファイルのパス

    Returns:
        URL文字列のリスト（末尾の改行は除去済み）

    Note:
        ファイルが存在しない場合、またはURLが0件の場合はエラーを表示して終了する。
    """
    if not input_file.exists():
        messagebox.showerror(
            "ファイルチェックエラー",
            "カレントディレクトリに url_list.txt が存在しないため処理を終了します。",
        )
        raise SystemExit

    with open(input_file, mode="r", encoding="utf-8") as f:
        url_list = [line.strip() for line in f if line.strip()]

    if len(url_list) < 1:
        messagebox.showwarning("件数チェックエラー", "処理対象データがないため処理を終了します。")
        raise SystemExit

    return url_list


def build_driver() -> WebDriver:
    """ChromeDriver をダウンロードし、ヘッドレスモードの WebDriver を生成して返す。"""
    chromedriver_path = chromedriver_binary_sync.download(download_dir=CHROMEDRIVER_DIR)
    service = Service(executable_path=chromedriver_path)

    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

    return WebDriver(service=service, options=options)


# ========================================
# メイン処理
# ========================================
def scroll_to_bottom(driver: WebDriver) -> None:
    """コメントエリアが展開しきるまでページをスクロールする。

    スクロール前後でコメントエリアの座標が変化しなくなった時点を終端と判定する。

    Args:
        driver: 操作対象の WebDriver
    """
    content = driver.find_element(By.TAG_NAME, "body")
    com_area = driver.find_element(By.ID, "contents")
    before_scroll = com_area.location

    while True:
        print(">> ページスクロール中…")
        content.send_keys(Keys.END)
        time.sleep(WAIT_SCROLL)

        after_scroll = com_area.location
        if before_scroll == after_scroll:
            print("<< ページスクロール終了")
            break
        before_scroll = after_scroll


def scrape_comments(driver: WebDriver) -> list[tuple[str, str]]:
    """Good評価が1つ以上のコメントを取得して返す。

    Args:
        driver: 操作対象の WebDriver

    Returns:
        (good数, コメント本文) のタプルリスト

    Note:
        コメントの取得は2件目から開始する（1件目はピン留めコメントのため除外）。
        コメントが見つからなくなった時点で取得を終了する。
    """
    comments: list[tuple[str, str]] = []
    i = 1

    while True:
        try:
            good_element = driver.find_element(By.XPATH, XPATH_GOOD.format(i=i))

            if good_element.text != "":
                com_element = driver.find_element(By.XPATH, XPATH_COMMENT.format(i=i))
                com_text = com_element.text.replace("\n", "")
                comments.append((good_element.text, com_text))

            i += 1

        except Exception:
            # コメント要素が見つからなくなったら取得終了
            break

    return comments


def process_url(driver: WebDriver, url: str) -> None:
    """1件のURLに対してスクロール・コメント取得・ファイル出力を実行する。

    YouTubeの動画ページ以外のURLはスキップする。

    Args:
        driver: 操作対象の WebDriver
        url:    処理対象のURL
    """
    driver.get(url)
    time.sleep(WAIT_PAGE_LOAD)

    try:
        title = driver.find_element(By.XPATH, XPATH_TITLE).text
        print(f">> ページタイトル：{title}")
    except Exception:
        print("適切なURLではありません")
        return

    scroll_to_bottom(driver)

    print(">>> 書込処理開始")
    comments = scrape_comments(driver)
    write_comments(title, comments)
    print("<<< 書込処理終了")


# ========================================
# 出力処理
# ========================================
def write_comments(title: str, comments: list[tuple[str, str]]) -> None:
    """コメント一覧をテキストファイルに書き出す。

    Args:
        title:    出力ファイル名に使用するページタイトル
        comments: (good数, コメント本文) のタプルリスト
    """
    with open(f"{title}.txt", mode="w", encoding="utf-8") as f:
        for good, comment in comments:
            f.write(f"【{good}】\t{comment}\n")


# ========================================
# 終了処理
# ========================================
def teardown(driver: WebDriver) -> None:
    """処理終了のメッセージを表示し、ブラウザを閉じる。"""
    print("< 処理終了")
    messagebox.showinfo("処理終了", "処理が終了しました")
    driver.quit()


# ========================================
# エントリーポイント
# ========================================
if __name__ == "__main__":
    # ※ Tkinter のウィンドウ本体は非表示にしてメッセージボックスのみ使用する
    root = tk.Tk()
    root.withdraw()

    url_list = load_url_list(INPUT_FILE)
    print(f"処理対象件数： {len(url_list)}")
    print("> 処理開始")

    driver = build_driver()
    driver.maximize_window()
    driver.implicitly_wait(5)

    try:
        for url in url_list:
            process_url(driver, url)
            time.sleep(WAIT_NEXT_URL)
    finally:
        # 例外発生時もブラウザを確実に閉じる
        teardown(driver)
