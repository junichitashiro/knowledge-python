# APIリクエスト送信

---

## プロキシを経由してAPIリクエストを送信する

### プロキシ設定を直接行う場合

* **proxies** にプロキシの情報を設定する

```python
import requests

proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080'
}

API_URL = 'http://api.example.com/endpoint'

res = requests.get(API_URL, proxies=proxies)
data = res.json()

if res.status_code == 200:
    print('APIリクエスト成功')
    print('レスポンスデータ:', data)
else:
    print('APIリクエストエラー')
    print('ステータスコード:', res.status_code)
    print('エラーメッセージ:', data)
```

---

### プロキシの認証が必要な場合

* **auth** パラメータに認証情報を設定する

```python
import requests

proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080'
}

# プロキシ認証情報
proxy_username = 'username'
proxy_password = 'password'

API_URL = 'http://api.example.com/endpoint'

res = requests.get(API_URL, proxies=proxies, auth=(proxy_username, proxy_password))
data = res.json()

if res.status_code == 200:
    print('APIリクエスト成功')
    print('レスポンスデータ:', data)
else:
    print('APIリクエストエラー')
    print('ステータスコード:', res.status_code)
    print('エラーメッセージ:', data)
```

---

### プロキシ設定ファイル（PACファイル）を使用してプロキシ経由でAPIリクエストを送信する

* **requests** の代わりに **PACSession** を使用する
* PACファイルの指定はURLでも可能

```python
from pypac import PACSession

PAC_FILE = '/path/to/PACfile'
# PAC_FILE = 'http://example.com/proxy.pac'
session = PACSession(proxy_pac_url)

# プロキシ認証情報（必要な場合のみ指定）
proxy_username = 'username'
proxy_password = 'password'
session.auth = (proxy_username, proxy_password)

API_URL = 'http://api.example.com/endpoint'

res = session.get(API_URL)
data = res.json()

if res.status_code == 200:
    print('APIリクエスト成功')
    print('レスポンスデータ:', data)
else:
    print('APIリクエストエラー')
    print('ステータスコード:', res.status_code)
    print('エラーメッセージ:', data)
```

---

## 何らかの情報を付与してAPIリクエストを送信する

### ログイン情報を付与してAPIリクエストを送信する

* **requests.Session** でセッションを作成する
* **session.post** でログインリクエストを送信する
* **session.post(API_URL)** でログイン情報を付与したAPIリクエストを送信する

```python
import requests

# セッションの作成
session = requests.Session()

# ログイン情報
login_url = 'http://example.com/login'
username = 'username'
password = 'password'
login_data = {
    'username': username,
    'password': password
}

# ログインリクエストの送信
res = session.post(login_url, data=login_data)

if res.status_code == 200:
    print('ログイン成功')
else:
    print('ログイン失敗')

# ログイン情報を付与してAPIリクエストを送信
API_URL = 'http://example.com/api'

res = session.post(API_URL)

if res.status_code == 200:
    print('APIリクエスト成功')
    data = res.json()
    print('レスポンスデータ:', data)
else:
    print('APIリクエストエラー')
    print('ステータスコード:', res.status_code)

```

---

### Cookie情報を付与してAPIリクエストを送信する

* **PACSession** を使用してプロキシ設定を行いログインリクエストを送信する
* ログインが成功した場合 **session.cookies.get_dict()** を使用してCookie情報を取得する
* APIリクエストを送信する際に **cookies** パラメータに取得したCookie情報を付与することで、セッションの状態（ログイン状態）を維持しながらAPIリクエストを行う

```python
from pypac import PACSession

PAC_FILE = '/path/to/PACfile'
session = PACSession(proxy_pac_url)

# プロキシ認証情報（必要な場合のみ）
proxy_username = 'username'
proxy_password = 'password'
session.auth = (proxy_username, proxy_password)

# ログイン情報
login_url = 'http://example.com/login'
username = 'username'
password = 'password'
login_data = {
    'username': username,
    'password': password
}

# ログインリクエストの送信
res = session.post(login_url, data=login_data)

if res.status_code == 200:
    print('ログイン成功')
else:
    print('ログイン失敗')

# Cookie情報の取得
cookies = session.cookies.get_dict()

API_URL = 'http://example.com/api'

# Cookie情報を付与してAPIリクエストを送信
res = session.get(API_URL, cookies=cookies)
data = res.json()

if res.status_code == 200:
    print('APIリクエスト成功')
    print('レスポンスデータ:', data)
else:
    print('APIリクエストエラー')
    print('ステータスコード:', res.status_code)
```
