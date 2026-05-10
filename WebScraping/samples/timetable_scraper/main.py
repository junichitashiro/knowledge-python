import chromedriver_binary_sync
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

# ========================================
# 定数
# ========================================
TARGET_URL = "https://www.jorudan.co.jp/norikae/"
CHROMEDRIVER_DIR = "chromedriver"
OUTPUT_FILE = "timetable.txt"

DEPARTURE = "新宿"
ARRIVAL = "東京"

# 入力フォームの XPath
XPATH = {
    "departure_input": '//*[@id="eki1_in"]',
    "arrival_input": '//*[@id="eki2_in"]',
    "search_button": '//*[@id="search_body"]/div[3]/input',
    # 検索結果行：{i} に行番号を埋め込んで使用する
    "result_row": '//*[@id="left"]/div[4]/div[2]/table/tbody/tr[{i}]/td[2]',
}


# ========================================
# 初期処理
# ========================================
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
def search_timetable(driver: WebDriver, departure: str, arrival: str) -> list[str]:
    """ジョルダンで経路検索を実行し、検索結果の時刻一覧を返す。

    Args:
        driver:    操作対象の WebDriver
        departure: 出発地名
        arrival:   到着地名

    Returns:
        時刻文字列のリスト（例: ["14:46発 → 15:00着", ...]）
    """
    driver.get(TARGET_URL)

    # 出発地・到着地を入力して検索を実行
    driver.find_element(By.XPATH, XPATH["departure_input"]).send_keys(departure)
    driver.find_element(By.XPATH, XPATH["arrival_input"]).send_keys(arrival)
    driver.find_element(By.XPATH, XPATH["search_button"]).click()

    # 検索結果の件数を取得（補足：出発時刻が過ぎていても結果は必ず存在する前提）
    result_count = len(driver.find_elements(By.CLASS_NAME, "t1"))

    # 各行の時刻テキストを取得
    timetable = [
        driver.find_element(By.XPATH, XPATH["result_row"].format(i=i)).text for i in range(1, result_count + 1)
    ]
    return timetable


# ========================================
# 出力処理
# ========================================
def write_timetable(timetable: list[str], output_file: str) -> None:
    """時刻一覧をテキストファイルに書き出す。

    Args:
        timetable:   時刻文字列のリスト
        output_file: 出力先ファイルパス
    """
    with open(output_file, mode="w", encoding="utf-8") as f:
        f.write("\n".join(timetable) + "\n")


# ========================================
# 終了処理
# ========================================
def teardown(driver: WebDriver) -> None:
    """ブラウザを閉じる。"""
    driver.quit()


# ========================================
# エントリーポイント
# ========================================
if __name__ == "__main__":
    print("> 処理開始")
    driver = build_driver()
    driver.maximize_window()
    driver.implicitly_wait(10)

    try:
        timetable = search_timetable(driver, DEPARTURE, ARRIVAL)
        write_timetable(timetable, OUTPUT_FILE)
    finally:
        # 例外発生時もブラウザを確実に閉じる
        teardown(driver)

    print("< 処理終了")
