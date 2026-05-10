import re
import time
import tkinter as tk
from tkinter import messagebox

import chromedriver_binary_sync
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# ========================================
# 定数
# ========================================
TARGET_URL = "https://store.starbucks.co.jp/"
CHROMEDRIVER_DIR = "chromedriver"

# 処理対象の都道府県ID範囲（1:北海道 ～ 47:沖縄）
# range(1, 48) で全都道府県が対象になる
TODOFUKEN_ID_RANGE = range(1, 2)

# 待機秒数
WAIT_PAGE_LOAD = 3
WAIT_SELECT = 3
WAIT_MORE_BUTTON = 1
WAIT_NEXT = 1

# XPath
XPATH = {
    # ※ セレクトボックスのoption番号はselect_by_valueの値（1始まり）より1大きい
    "option": '//*[@id="selectbox"]/option[{option_index}]',
    "result_count": '//*[@id="vue-search"]/div[3]/div[1]/div/div[2]/div[1]/div[3]/div[1]',
    "more_button": '//*[@id="vue-search"]/div[3]/div[1]/div/div[2]/div[1]/div[3]/div[2]/div[2]/button',
    "store_item": '//*[@id="store-list"]/li[{i}]/div',
}


# ========================================
# 初期処理
# ========================================
def build_driver() -> WebDriver:
    """ChromeDriver をダウンロードし、ヘッドレスモードの WebDriver を生成して返す。"""
    chromedriver_path = chromedriver_binary_sync.download(download_dir=CHROMEDRIVER_DIR)
    service = Service(executable_path=chromedriver_path)

    options = Options()
    # options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

    return WebDriver(service=service, options=options)


# ========================================
# メイン処理
# ========================================
def expand_all_stores(driver: WebDriver) -> None:
    """「もっと見る」ボタンを押せなくなるまでクリックし、全店舗を表示させる。

    ※2026年5月時点でこのボタンはなくなっている。

    Args:
        driver: 操作対象の WebDriver
    """
    while True:
        try:
            more_buttons = driver.find_elements(By.XPATH, XPATH["more_button"])
            if len(more_buttons) == 0:
                break
            driver.find_element(By.XPATH, XPATH["more_button"]).click()
            time.sleep(WAIT_MORE_BUTTON)
        except Exception:
            break


def scrape_stores(driver: WebDriver, result_cnt: int) -> list[str]:
    """表示されている全店舗のテキスト情報を取得して返す。

    Args:
        driver:     操作対象の WebDriver
        result_cnt: 取得対象の店舗件数

    Returns:
        店舗情報テキストのリスト
    """
    return [driver.find_element(By.XPATH, XPATH["store_item"].format(i=i)).text for i in range(1, result_cnt + 1)]


def process_todofuken(driver: WebDriver, selectbox_element, todofuken_id: int) -> None:
    """1つの都道府県に対して店舗情報の取得とファイル出力を実行する。

    Args:
        driver:            操作対象の WebDriver
        selectbox_element: 都道府県セレクトボックスの要素
        todofuken_id:      都道府県ID（1:北海道 ～ 47:沖縄）
    """
    Select(selectbox_element).select_by_value(str(todofuken_id))
    time.sleep(WAIT_SELECT)

    # ※ option番号は select_by_value の値より1大きいためインクリメントして使用する
    option_index = todofuken_id + 1
    target = driver.find_element(By.XPATH, XPATH["option"].format(option_index=option_index)).text
    print(f">> 処理対象：{target}")

    # 都道府県名から件数表記（例：" (25)"）を除去する
    todofuken_name = re.sub(r" \(\d+\)", "", target)

    result_text = driver.find_element(By.XPATH, XPATH["result_count"]).text
    result_cnt = int(result_text.replace("件", ""))

    expand_all_stores(driver)

    print(">>> 書込処理開始")
    stores = scrape_stores(driver, result_cnt)
    write_stores(todofuken_name, stores)
    print("<<< 書込処理終了")


# ========================================
# 出力処理
# ========================================
def write_stores(todofuken_name: str, stores: list[str]) -> None:
    """店舗情報をテキストファイルに書き出す。

    Args:
        todofuken_name: 出力ファイル名に使用する都道府県名
        stores:         店舗情報テキストのリスト
    """
    with open(f"{todofuken_name}.txt", mode="w", encoding="utf-8") as f:
        for i, store_text in enumerate(stores, start=1):
            f.write(f"<{i}>\n{store_text}\n")


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

    print("> 処理開始")
    driver = build_driver()
    driver.maximize_window()
    driver.implicitly_wait(10)

    try:
        driver.get(TARGET_URL)
        time.sleep(WAIT_PAGE_LOAD)

        selectbox_element = driver.find_element(By.ID, "selectbox")

        for todofuken_id in TODOFUKEN_ID_RANGE:
            process_todofuken(driver, selectbox_element, todofuken_id)
            time.sleep(WAIT_NEXT)
    finally:
        # 例外発生時もブラウザを確実に閉じる
        teardown(driver)
