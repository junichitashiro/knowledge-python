# get メソッドを使った基本動作

---

## ライブラリの導入

### FastAPIのインストール

```bash
uv add fastapi
```

### Uvicornのインストール

非同期Webサーバ実装に必要なライブラリ

```bash
uv add "uvicorn[standard]"
```

---

## コマンド

### FastAPIプロジェクトで main.py の app インスタンスを起動する

```bash
uv run uvicorn main:app --reload
```

| コマンド / 引数 | 説明                                                         |
| --------------- | ------------------------------------------------------------ |
| uvicorn         | Uvicorn 起動コマンド                                         |
| main:app        | Pythonファイル名とFastAPIインスタンスの変数名                |
| --reload        | ソースコードの変更に対してサーバを自動で再起動するオプション |

## Swagger UI

FastAPIの機能により自動的に作成されるドキュメント

### 参照アドレス

* http://127.0.0.1:8000/docs
