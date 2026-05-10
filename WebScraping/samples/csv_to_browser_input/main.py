import csv
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import chromedriver_binary_sync
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

# ========================================
# 定数
# ========================================
CSV_FILE = Path.cwd() / "input.csv"
TARGET_URL = "https://keisan.casio.jp/exec/system/1183427246/"
CHROMEDRIVER_DIR = "chromedriver"

# 入力フォームの XPath
XPATH = {
    "age": '//*[@id="var_age"]',
    "sex_男": '//*[@id="inparea"]/tbody/tr[2]/td[2]/ul/ol/li[5]/label[1]',
    "sex_女": '//*[@id="inparea"]/tbody/tr[2]/td[2]/ul/ol/li[5]/label[2]',
    "act_低い": '//*[@id="inparea"]/tbody/tr[3]/td[2]/ul/ol/li[1]/label[1]',
    "act_ふつう": '//*[@id="inparea"]/tbody/tr[3]/td[2]/ul/ol/li[1]/label[2]',
    "act_高い": '//*[@id="inparea"]/tbody/tr[3]/td[2]/ul/ol/li[1]/label[3]',
    "weight": '//*[@id="var_kg"]',
    "result": '//*[@id="ans0"]',
    "execute": '//*[@id="executebtn"]',
    "clear": '//*[@id="clearbtn"]',
}


# ========================================
# 初期処理
# ========================================
def load_csv(csv_file: Path) -> list[list[str]]:
    """CSVファイルを読み込んで全行を返す。

    Args:
        csv_file: CSVファイルのパス

    Returns:
        全行データ（1行目はヘッダ行）

    Note:
        ファイルが存在しない場合、またはデータ行が0件の場合はエラーを表示して終了する。
    """
    if not csv_file.exists():
        messagebox.showerror(
            "ファイルチェックエラー",
            "カレントディレクトリに input.csv が存在しないため処理を終了します。",
        )
        raise SystemExit

    with open(csv_file, mode="r", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    # ヘッダ行のみの場合は処理対象なし
    if len(rows) < 2:
        messagebox.showwarning("件数チェックエラー", "処理対象データがないため処理を終了します。")
        raise SystemExit

    return rows


def build_driver() -> WebDriver:
    """ChromeDriver をダウンロードし、WebDriver を生成して返す。"""
    chromedriver_path = chromedriver_binary_sync.download(download_dir=CHROMEDRIVER_DIR)
    service = Service(executable_path=chromedriver_path)

    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

    return WebDriver(service=service, options=options)


# ========================================
# メイン処理
# ========================================
def input_row_to_browser(driver: WebDriver, row: list[str], index: int, total: int) -> None:
    """1行分のデータをブラウザに入力し、計算結果をメッセージボックスで表示する。

    Args:
        driver: 操作対象の WebDriver
        row:    CSVの1行データ（年齢, 性別, 身体活動レベル, 目標体重）
        index:  現在の処理行番号（1始まり）
        total:  処理対象の総件数
    """
    age, sex, act_level, weight = row

    # 年齢・体重の入力
    driver.find_element(By.XPATH, XPATH["age"]).send_keys(age)
    driver.find_element(By.XPATH, XPATH["weight"]).send_keys(weight)

    # 性別の選択（想定外の値は無視）
    sex_key = f"sex_{sex}"
    if sex_key in XPATH:
        driver.find_element(By.XPATH, XPATH[sex_key]).click()

    # 身体活動レベルの選択（想定外の値は「ふつう」を選択）
    act_key = f"act_{act_level}"
    act_xpath = XPATH.get(act_key, XPATH["act_ふつう"])
    driver.find_element(By.XPATH, act_xpath).click()

    # 計算実行
    driver.find_element(By.XPATH, XPATH["execute"]).click()

    # 計算結果の表示
    energy = driver.find_element(By.XPATH, XPATH["result"]).text
    message = f"{index}／{total}件目\n１日に必要なエネルギー量は {energy} Kcalです"
    messagebox.showinfo("計算結果", message)

    driver.find_element(By.XPATH, XPATH["clear"]).click()


def run(rows: list[list[str]], driver: WebDriver) -> None:
    """ヘッダ行を除いた全データ行をブラウザに入力する。

    Args:
        rows:   CSVの全行データ（1行目はヘッダ行）
        driver: 操作対象の WebDriver
    """
    data_rows = rows[1:]  # ヘッダ行を除外
    total = len(data_rows)
    print(f"処理対象件数： {total}")
    print(">>> 処理開始")

    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(TARGET_URL)

    for index, row in enumerate(data_rows, start=1):
        input_row_to_browser(driver, row, index, total)


# ========================================
# 終了処理
# ========================================
def teardown(driver: WebDriver) -> None:
    """処理終了のメッセージを表示し、ブラウザを閉じる。"""
    print("<<< 処理終了")
    messagebox.showinfo("処理終了", "処理が終了しました")
    driver.quit()


# ========================================
# エントリーポイント
# ========================================
if __name__ == "__main__":
    # ※ Tkinter のウィンドウ本体は非表示にしてメッセージボックスのみ使用する
    root = tk.Tk()
    root.withdraw()

    rows = load_csv(CSV_FILE)
    driver = build_driver()

    try:
        run(rows, driver)
    finally:
        # 例外発生時もブラウザを確実に閉じる
        teardown(driver)
