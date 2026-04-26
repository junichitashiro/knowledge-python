import customtkinter as ctk


# ====================
# 値を取得する関数
# ====================
def print_selected_value() -> None:
    selected_value = selected_menu_var.get()
    print(f"取得値：{selected_value}")


# --------------------
# GUIの設定
# --------------------
# 基本設定
app = ctk.CTk()
app.title("オプションメニューの設定値を取得")
app.geometry("350x200")

# --------------------
# オプションメニュー
# --------------------
# オプションメニューの値を保持する変数と初期値の設定
selected_menu_var = ctk.StringVar(value="未選択")
# メニュー本体
menu = ctk.CTkOptionMenu(
    app,
    values=[
        "メニュー1",
        "メニュー2",
        "メニュー3",
    ],
    variable=selected_menu_var,
)

# --------------------
# ボタン
# --------------------
# 関数を実行するボタン
submit_btn = ctk.CTkButton(app, text="値を取得する", command=print_selected_value)

# --------------------
# 配置
# --------------------
menu.pack(anchor="center", padx=20, pady=5)
submit_btn.pack(pady=40)

# ====================
# アプリの実行
# ====================
app.mainloop()
