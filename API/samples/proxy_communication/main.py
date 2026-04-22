import subprocess
import time

import requests

# Torの起動を待つ時間（秒）
TOR_STARTUP_WAIT_SECONDS = 3

# TorプロセスのパスとSOCKS5プロキシの設定
TOR_EXE_PATH = r"C:\Users\junichi\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe"
TOR_PROXY_URL = "socks5://127.0.0.1:9050"
IP_CHECK_URL = "https://ipinfo.io"


def start_tor_process(tor_path: str) -> subprocess.Popen:
    """
    Torプロセスを起動して返す。

    Args:
        tor_path: tor.exeの絶対パス

    Returns:
        起動したsubprocess.Popenオブジェクト
    """
    return subprocess.Popen([tor_path], shell=True, text=True)


def build_tor_proxies(proxy_url: str) -> dict[str, str]:
    """
    requestsライブラリに渡すプロキシ設定を構築して返す。

    Args:
        proxy_url: SOCKS5プロキシのURL（例: socks5://127.0.0.1:9050）

    Returns:
        httpとhttpsをキーに持つプロキシ設定辞書
    """
    return {"http": proxy_url, "https": proxy_url}


def fetch_ip_info(url: str, proxies: dict[str, str] | None = None) -> dict:
    """
    IPアドレス情報を取得して返す。
    build_tor_proxies() の戻り値をそのまま proxies に渡すことができる。

    Args:
        url: IPアドレス確認APIのURL
        proxies: requestsに渡すプロキシ設定。Noneの場合はプロキシなしで接続する

    Returns:
        APIのレスポンスをパースしたdict
    """
    response = requests.get(url, proxies=proxies)
    return response.json()


# ※ 簡略化のため例外処理は省略

# Torを起動し、接続が安定するまで待機する
tor_process = start_tor_process(TOR_EXE_PATH)
time.sleep(TOR_STARTUP_WAIT_SECONDS)

# プロキシなしのIPアドレスを確認する（本来のグローバルIP）
ip_info_direct = fetch_ip_info(IP_CHECK_URL)
print("Direct:", ip_info_direct)

# プロキシあり（Tor経由）のIPアドレスを確認する
tor_proxies = build_tor_proxies(TOR_PROXY_URL)
ip_info_via_tor = fetch_ip_info(IP_CHECK_URL, proxies=tor_proxies)
print("Via Tor:", ip_info_via_tor)
