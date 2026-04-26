import customtkinter as ctk

# 処理内容の対応表
HANDLERS: dict[str, str] = {
    "opt1": "ラジオボタン1が選択されました",
    "opt2": "ラジオボタン2が選択されました",
    "opt3": "ラジオボタン3が選択されました",
}

DEFAULT_MESSAGE = "未定義の選択肢です"


# ========================================
# 値を取得して対応する文字列を表示する関数
# ========================================
def dispatch_by_selection() -> None:
    selected_value = selected_radio_var.get()
    print(HANDLERS.get(selected_value, DEFAULT_MESSAGE))


# --------------------
# GUIの設定
# --------------------
# 基本設定
app = ctk.CTk()
app.title("ラジオボタンの選択による条件分岐")
app.geometry("350x220")

# --------------------
# ラジオボタン
# --------------------
# ラジオボタンの値を保持する変数と初期値の設定
selected_radio_var = ctk.StringVar(value="opt1")

# リスト形式でラジオボタンのオプションを作成する
radio_options = [
    ("ラジオボタン1", "opt1"),
    ("ラジオボタン2", "opt2"),
    ("ラジオボタン3", "opt3"),
]

# リストを使ってラジオボタンを連続生成する
for text, value in radio_options:
    radio_btn = ctk.CTkRadioButton(app, text=text, variable=selected_radio_var, value=value)
    radio_btn.pack(anchor="center", padx=20, pady=5)

# --------------------
# ボタン
# --------------------
# 関数を実行するボタン
submit_btn = ctk.CTkButton(app, text="処理を実行する", command=dispatch_by_selection)
submit_btn.pack(pady=15)

# ====================
# アプリの実行
# ====================
app.mainloop()
