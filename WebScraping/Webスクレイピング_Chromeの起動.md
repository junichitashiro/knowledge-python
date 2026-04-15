# Webスクレイピング_Chromeの起動

---

## seleniumとChrome DriverでGoogle Chromeを操作する

### 事前準備

#### 必要なモジュールをインストールする

```cmd
uv add selenium
uv add chromedriver_binary_sync
```

## サンプルコード

```python
import time

import chromedriver_binary_sync
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# ========================================
# 初期処理
# ========================================
# ChromeDriverをダウンロードしてパスを定数に格納する
CHROMEDRIVER = chromedriver_binary_sync.download(download_dir='chromedriver')
chrome_service = Service(executable_path=CHROMEDRIVER)


# ========================================
# メイン処理
# ========================================
# ブラウザを起動する
driver = WebDriver(service=chrome_service)

# 指定するURLを開く
driver.get('https://www.google.com/')

# XPathで検索ボックスを特定する
search_box_xpath = '//*[@id="APjFqb"]'
driver.find_element(By.XPATH, search_box_xpath).send_keys('Selenium実践入門')

# NAMEで検索ボックスを特定して入力文字をクリアする
search_box_name = 'q'
driver.find_element(By.NAME, search_box_name).clear()

# 再度検索文字を入力して検索の3秒後にブラウザを閉じる
driver.find_element(By.XPATH, search_box_xpath).send_keys('Selenium実践入門' + Keys.RETURN)
time.sleep(3)
driver.quit()
```

---

## 起動時の設定

### chromedriver_binary_sync.download()

* ブラウザのバージョンに合わせたChromeDriverをダウンロードする
* ダウンロードフォルダの指定が可能
* 実行すると使用するChromeDriverのパスを返す
* 以前使用していた **ChromeDriverManager().install()** から変更
* 下記はダウンロードと同時に定数 **CHROMEDRIVER** に実行ファイルパスを格納する設定

  ```python
  CHROMEDRIVER = chromedriver_binary_sync.download(download_dir='chromedriver')
  ```

### selenium.webdriver.chrome.service.Service(executable_path='ChromeDriverのパス')

* 実行時にChromeDriverのパスを指定するのが推奨となっている
* 指定しないと警告が表示されるので表示されないために設定する
* 下記は **chromedriver_binary_sync.download()** で返ってくるパスを格納した定数を設定している

  ```python
  chrome_service = Service(executable_path=CHROMEDRIVER)
  ```

### selenium.webdriver.chrome.webdriver.WebDriver().implicitly_wait(XX)

* 要素が見つかるまで指定秒数待つ

---

## オプション

### selenium.webdriver.chrome.options.Options()

* オプションを指定するためのクラス

#### add_argument('--headless')

* ヘッドレスモードで起動する関数と引数
* ブラウザを表示させずにバックグラウンドで処理する

#### add_argument('--user-data-dir=' + PROFILE_PATH)

* 起動するChromeのアカウントを指定する

  ```python
  PROFILE_PATH = r'C:\Users\---\AppData\Local\Google\Chrome\User Data'
  chrome_options.add_argument('--user-data-dir=' + PROFILE_PATH)
  ```

#### add_experimental_option('excludeSwitches', ['enable-automation'])

* ブラウザ起動時のテスト実行警告を非表示にする
* 指定しないとブラウザに以下のメッセージが表示される

  ```
  Chrome は 自動テスト ソフトウェアによって制御されています。
  ```

#### add_experimental_option('excludeSwitches', ['enable-logging'])

* DevToolsのログを出力しない
* 指定しないとコンソールに以下のようなログが表示される
* 無視しても良いので非表示にする

  ```bash
  DevTools listening on ws://127.0.0.1:52518/devtools/browser/85b4357a-7fc7-4969-a3f0-e6c235eecc03
  >>> [8244:10016:1215/205133.795:ERROR:device_event_log_impl.cc(215)] [20:30:40.795] USB: usb_device_handle_win.cc:1045 Failed to read descriptor from node connection: システムに接続されたデバイスが機能していません。 (0x1F)
  ```

#### add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])

* 上記のテスト実行警告とDevToolsのログを非表示にする指定の仕方

#### add_experimental_option('prefs', {'download.default_directory': 'ディレクトリパス'})

* ブラウザのダウンロードフォルダを指定する

---

## 各種オプションを指定したサンプルコード

```python
import time

import chromedriver_binary_sync
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# ========================================
# 初期処理
# ========================================
# ChromeDriverをダウンロードしてパスを定数に格納する
CHROMEDRIVER = chromedriver_binary_sync.download(download_dir='chromedriver')
chrome_service = Service(executable_path=CHROMEDRIVER)

# オプションを設定する
chrome_options = Options()
# ヘッドレスモードで起動する
chrome_options.add_argument('--headless')
# テスト実行警告とDevToolsのログを非表示
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
# ファイルのダウンロードフォルダを指定する
dl_folder = 'C:\temp'
chrome_options.add_experimental_option('prefs', {'download.default_directory': dl_folder})


# ========================================
# メイン処理
# ========================================
# ブラウザを起動する
driver = WebDriver(service=chrome_service, options=chrome_options)
# ブラウザを最大化する
driver.maximize_window()
# 要素が見つかるまで最大10秒待つ設定
driver.implicitly_wait(10)

# 指定したURLを開く
driver.get('https://www.google.com/')

# XPathで検索ボックスを特定する
search_box_xpath = '//*[@id="APjFqb"]'
driver.find_element(By.XPATH, search_box_xpath).send_keys('Selenium実践入門')

# NAMEで検索ボックスを特定して入力文字をクリアする
search_box_name = 'q'
driver.find_element(By.NAME, search_box_name).clear()

# 再度検索文字を入力して検索の3秒後にブラウザを閉じる
driver.find_element(By.XPATH, search_box_xpath).send_keys('Selenium実践入門' + Keys.RETURN)
time.sleep(3)
driver.quit()
```
