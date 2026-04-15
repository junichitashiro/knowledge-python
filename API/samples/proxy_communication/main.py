import subprocess

import requests

# Torのデフォルトポート
proxies = {"http": "socks5://127.0.0.1:9050", "https": "socks5://127.0.0.1:9050"}

# Torを起動する
# subprocess.Popen(["path\to\tor.exe"], shell=True, text=True)
subprocess.Popen(["C:\\Users\\junichi\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe"], shell=True, text=True)

# プロキシを使用せずIPアドレス表示のAPIを実行する
res = requests.get("https://ipinfo.io")
print(res.json())

# プロキシを使用して再度実行する
res_proxy = requests.get("https://ipinfo.io", proxies=proxies)
print(res_proxy.json())
