import flet as ft
import pandas as pd


def main(page: ft.Page) -> None:
    # ページ全体のレイアウト
    page.window.width=600
    page.window.height=600

    # クリップボードにテキストをコピーする関数
    def copy_to_clipboard(e: ft.ControlEvent) -> None:
        text = e.control.text
        page.set_clipboard(text)
        page.open(ft.SnackBar(ft.Text(f'Copied {text} to clipboard')))
        page.update()

    # Excelファイルからデータを読み込む
    excel_data = pd.read_excel('data.xlsx', sheet_name=None, usecols='A,B', header=None, dtype=str)

    # 1列目と2列目の最大文字数を調べる
    max_len_col1 = 0
    max_len_col2 = 0
    for df in excel_data.values():
        max_len_col1 = max(max_len_col1, df[0].dropna().astype(str).map(len).max())
        max_len_col2 = max(max_len_col2, df[1].dropna().astype(str).map(len).max())

    # ピクセル幅に変換（1文字 ≒ 12px で調整）
    char_width_px = 12
    button_width_col1 = max_len_col1 * char_width_px + 20 # +20 は余白
    button_width_col2 = max_len_col2 * char_width_px + 20

    # タブ作成
    tabs = []

    for sheet_name, df in excel_data.items():
        column = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.ElevatedButton(text=row[0], on_click=copy_to_clipboard),
                            width=button_width_col1,
                            padding=5
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(text=row[1], on_click=copy_to_clipboard) if pd.notna(row[1]) else ft.Container(),
                            width=button_width_col2,
                            padding=5
                        )
                    ]
                )
                for _, row in df.iterrows()
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        tabs.append(ft.Tab(text=sheet_name, content=column))

    page.add(ft.Tabs(tabs=tabs, expand=True))


# アプリを実行
ft.app(target=main)
