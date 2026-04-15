# メールの送信

---

## Outlookでメールの作成と送信をする

### 事前準備

#### pipからwin32comをインストールする

```cmd
uv add pywin32
```

---

## サンプルコード

### 補足

* 作成したメールを表示して手動で送信する場合 **mail.display(True)** をコメントインする
* 確認せずそのまま送信する場合 **mail.Send()** をコメントインする
* 宛先は **;** 区切りで複数指定することができる

```python
import win32com.client


# ========================================
# 初期処理
# ========================================
# Outlookオブジェクトの設定
outlook = win32com.client.Dispatch('Outlook.Application')
mail = outlook.CreateItem(0)


# ------------------------------
# メール内容の設定
# ------------------------------
# 署名
sign = '''
'''
mail.bodyformat = 1  # 1:テキスト 2:HTML 3:リッチテキスト
mail.to = ''
mail.cc = ''
mail.bcc = ''
mail.subject = '件名'
mail.body = '''
メール本文
''' + '\n' + sign


# ------------------------------
# 添付ファイルの設定
# ------------------------------
# 添付ファイルの絶対パス
add_file1 = 'C:\\...\\...\\file.txt'
mail.attachments.Add(add_file1)

# 必要に応じて増やす
# add_file2 = ''
# mail.attachments.Add(add_file2)


# ========================================
# メイン処理
# ========================================
# メールを送信する
# mail.display(True)
mail.Send()
```
