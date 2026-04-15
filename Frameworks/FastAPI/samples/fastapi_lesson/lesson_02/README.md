# 型ヒント

---

## 型ヒントとFastAPI

### 型ヒントの価値向上

FastAPIでは型ヒントを使うことで

* バリデーション
* ドキュメント生成（OpenAPI）
* JSON変換

が可能になり、型ヒントの価値が向上した。

### 型ヒントによる設計思想の変化

**型ヒント = バリデーション = API仕様** となり、ドキュメントの齟齬がなくなった。

これにより

```mermaid
flowchart LR
A[コードを書く] --> B[仕様書を書く] --> C[バリデーションを書く]
```
から
```mermaid
flowchart LR
A[型を書く] --> B[一連のドキュメントが全てできる]
```
へと変化した。

---

## Optional型

### Opthionalとは

* Optional[T] = 「T または None を許容する型」
* 実体は Union[T, None]

### 主な用途

* **Noneを許容するかどうか** を型で明示する
* Noneを使う場合は必ず分岐を強制する設計にする

```python
from typing import Optional


# None を許容するパターン
def greeting_01(parameter: Optional[str] = None) -> Optional[str]:
    if parameter is None:
        return "名前を入力してください"

    return f"こんにちは、{parameter}さん！"


# None を許容しないパターン
def greeting_02(parameter: str = "ゲスト") -> str:
    if parameter is None:
        raise ValueError("名前を入れてください")

    return f"こんにちは、{parameter}さん！"


# 呼び出し
greeting_01("しろたん")
greeting_01()
greeting_01(None)

greeting_02("しろたん")
greeting_02()
# greeting_02(None)  # 警告が表示される
```


### Python3.10以降の推奨

```python
def func(x: str | None) -> str | None:
    return x
```

### 推奨の書き方による修正（None を許容するパターン）

```python
def greeting_03(parameter: str | None = None) -> str | None:
    if parameter is None:
        return "名前を入力してください"

    return f"こんにちは、{parameter}さん！"


# 呼び出し
greeting_03("しろたん")
greeting_03()
greeting_03(None)
```

---

## Annotated

### Annotatedとは

* 型ヒントの拡張機能
* 型だけでなく書式やフォーマットなどの追加情報を付与できる

```python
from typing import Annotated


def func(user_id: Annotated[str, "8桁の英数字であること"]):
    print(user_id)
```

---

## パイプ演算子

### パイプ演算子とは

* **|** をつかって **または** を表現し型ヒントを読みやすくする
* Python3.10から導入

```python
def greeting_04(name: str | None) -> str:
    if name is None:
        return "こんにちは、ゲストさん！"
    else:
        return f"こんにちは、{name}さん！"


# 呼び出し
greeting_04("しろたん")
greeting_04(None)
```

### Unionによる書き換え

```python
from typing import Union


def greeting_05(name: Union[str, None]) -> str:
    if name is None:
        return "こんにちは、ゲストさん！"
    else:
        return f"こんにちは、{name}さん！"


# 呼び出し
greeting_05("しろたん")
greeting_05(None)
```

## 型ヒント使い分けの目安

* T | None（パイプ演算子）を使うのが基本
* Optional[T]は「None許容」の意図を明示したい場合のみ
* Union[...]は3種類以上の型や旧バージョン対応時のみ

### T | None（パイプ演算子）

* 標準で推奨
* 最も可読性が高い

### Optional

* 可読性よりも意味を強調するために使う
* 非推奨ではないがやや古い

### Union

* **|** で代替可能

使うとすれば
* Python 3.9以前の対応
* 型が動的生成されるケース（※レアケース）
