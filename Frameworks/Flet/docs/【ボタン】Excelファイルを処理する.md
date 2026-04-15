# Excelファイルを処理する

---

## Excelファイルの内容をページ内に表示する

### 概要

* ボタンをクリックしてファイルの選択ダイアログを表示する
* 選択したファイルの内容をページ内に表示する

### 補足

* file_picker は画面に表示される UI ではないため overlay への追加のみでよい

```python
import flet as ft
import pandas as pd


def main(page: ft.Page) -> None:
    # ボタンがクリックされたときに実行される関数
    def pick_file(e: ft.ControlEvent) -> None:
        file_picker.pick_files(allow_multiple=False, allowed_extensions=['xlsx'])

    # ファイルが選択されたときに実行される関数
    def on_file_picked(e: ft.FilePickerResultEvent) -> None:
        if e.files:
            file_path = e.files[0].path
            df = pd.read_excel(file_path)

            # データテーブルの作成
            columns = [ft.DataColumn(ft.Text(col)) for col in df.columns]
            rows = [
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row])
                for row in df.values
            ]

            data_table.columns = columns
            data_table.rows = rows
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    # ボタンとデータテーブルを作成
    pick_button = ft.ElevatedButton('ファイルを選択', on_click=pick_file)
    data_table = ft.DataTable(
        columns=[ft.DataColumn(label=ft.Text('ファイル読み込み待ち'))],
        rows=[]
)

    # 画面サイズ
    page.window.width = 500
    page.window.height = 500

    # ページにボタンとデータテーブルを追加
    page.add(pick_button, data_table)


# Fletアプリケーションを実行
ft.app(target=main)
```

---

## Excelのアプリケーションからファイルを開く

### 概要

* ボタンをクリックしてファイルの選択ダイアログを表示する
* 選択したファイルをExcelのアプリケーションから開く

### 補足

* 実行環境の判定では外部コマンドにパスを渡すことになるため安全のためダブルクォートで囲んでいる

```python
import os
import platform

import flet as ft


def main(page: ft.Page) -> None:
    # ファイル選択ボタンクリック時の処理
    def pick_file(e: ft.ControlEvent) -> None:
        file_picker.pick_files(allow_multiple=False, allowed_extensions=['xlsx'])

    # ファイル選択後の処理
    def open_file(e: ft.FilePickerResultEvent) -> None:
        if file_picker.result and file_picker.result.files:
            file_path = file_picker.result.files[0].path
            print(f'選択したファイルのパス: {file_path}')

            # 実行環境の判定
            try:
                if platform.system() == 'Windows':
                    os.startfile(file_path)
                elif platform.system() == 'Darwin':  # macOS
                    os.system(f'open "{file_path}"')
                else:  # Linux
                    os.system(f'xdg-open "{file_path}"')
            except Exception as ex:
                print(f'ファイルの読み込み中にエラーが発生しました: {ex}')
        else:
            print('ファイルが選択されませんでした')

    # ファイルピッカーとボタンの作成
    file_picker = ft.FilePicker(on_result=open_file)
    page.overlay.append(file_picker)

    pick_file_button = ft.ElevatedButton(text='ファイルを選択', on_click=pick_file)

    # ウィンドウサイズの設定（デスクトップ用）
    page.window.width = 350
    page.window.height = 350

    # ページにボタンのみ追加
    page.add(pick_file_button)


# Fletアプリケーションを実行
ft.app(target=main)
```
