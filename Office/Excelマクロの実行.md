# Excelマクロの実行

---

## PythonからExcelのマクロを実行する

## 事前準備

### win32comをインストールする

```cmd
uv add pywin32
```

### マクロの準備

#### test.xlsm を新規作成して次のマクロを定義する

```vb
Sub test()

    MsgBox ("マクロのテスト")

End Sub
```

---

## サンプルコード

### 補足

* 読み取り専用（ReadOnly=1）で開くことで、SaveChanges=1 を指定したとしても保存しない
* 元ファイルを変更させないための対応

```python
# ----------------------------------------
# モジュールのインポート
# ----------------------------------------
import win32com.client


# ----------------------------------------
# 変数の設定
# ----------------------------------------
# ファイルパス
folder_path = 'C:\\temp\\'
macro_file = 'test.xlsm'
file_path = folder_path + macro_file


# ----------------------------------------
# マクロの実行
# ----------------------------------------
# Excelを起動する
app = win32com.client.Dispatch('Excel.Application')

# Excel起動時の表示設定 0:非表示 1:表示
app.Visible = 0

# 指定したブックを開く
app.Workbooks.Open(Filename=file_path, ReadOnly=1)

# マクロ名を指定して実行
app.Application.Run('ThisWorkbook.test')

# ブックを保存せずに閉じる
app.Workbooks(1).Close(SaveChanges=0)

# Excelを終了
app.Application.Quit()
```
