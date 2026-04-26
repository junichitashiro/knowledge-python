import tkinter as tk


# ===================================
# メニュー選択時に値を取得する関数
# ===================================
def on_menu_selected(choice) -> None:
    print("メニュー選択で取得した値：", choice)


# ===================================
# ボタンから値を取得する関数
# ===================================
def print_selected_value() -> None:
    selected_value = selected_menu_var.get()
    print(f"ボタン押下で取得した値：{selected_value}")


# --------------------
# GUIの設定
# --------------------
# 基本設定
app = tk.Tk()
app.title("オプションメニューの設定値を取得")
app.geometry("350x200")

# --------------------
# オプションメニュー
# --------------------
# オプションメニューの値を保持する変数と初期値の設定
selected_menu_var = tk.StringVar(value="未選択")
# メニュー本体
menu = tk.OptionMenu(
    app,
    selected_menu_var,
    "メニュー1",
    "メニュー2",
    "メニュー3",
    command=on_menu_selected,  # メニュー選択の都度関数を実行する
)

# --------------------
# ボタン
# --------------------
# 関数を実行するボタン
submit_btn = tk.Button(app, text="値を取得する", command=print_selected_value)

# --------------------
# 配置
# --------------------
menu.pack(anchor="center", padx=20, pady=5)
submit_btn.pack(pady=40)

# ====================
# アプリの実行
# ====================
app.mainloop()
