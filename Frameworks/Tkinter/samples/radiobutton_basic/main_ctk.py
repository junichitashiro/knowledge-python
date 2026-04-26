import customtkinter as ctk


# ====================
# 値を取得する関数
# ====================
def print_selected_value() -> None:
    selected_value = selected_radio_var.get()
    print(f"取得値：{selected_value}")


# --------------------
# GUIの設定
# --------------------
# 基本設定
app = ctk.CTk()
app.title("ラジオボタンの設定値を取得")
app.geometry("350x200")

# --------------------
# ラジオボタン
# --------------------
# ラジオボタンの値を保持する変数と初期値の設定
selected_radio_var = ctk.StringVar(value="a")

# リスト形式でラジオボタンのオプションを作成する
radio_options = [
    ("設定値：a", "a"),
    ("設定値：b", "b"),
    ("設定値：c", "c"),
]

# リストを使ってラジオボタンを連続生成する
for text, value in radio_options:
    radio_btn = ctk.CTkRadioButton(app, text=text, value=value, variable=selected_radio_var)
    radio_btn.pack(anchor="center", padx=20, pady=5)

# --------------------
# ボタン
# --------------------
# 関数を実行するボタン
submit_btn = ctk.CTkButton(app, text="値を取得する", command=print_selected_value)
submit_btn.pack(pady=15)

# ====================
# アプリの実行
# ====================
app.mainloop()
