import tkinter as tk


# ===================================
# 値を取得して条件判断を実行する関数
# ===================================
def execute_by_selection() -> None:
    selected_value = selected_radio_var.get()
    if selected_value == 1:
        print("設定値：1 が選択されました")
    elif selected_value >= 2:
        print("2以上の設定値が選択されました")
    else:
        print("未選択です")


# --------------------
# GUIの設定
# --------------------
# 基本設定
app = tk.Tk()
app.title("ラジオボタンの選択による条件分岐")
app.geometry("350x200")

# --------------------
# ラジオボタン
# --------------------
# ラジオボタンの値を保持する変数と初期値の設定
# 処理の違いをわかりやすくするため設定値にない 0 を設定する
selected_radio_var = tk.IntVar(value=0)

# リスト形式でラジオボタンのオプションを作成する
radio_options = [
    ("設定値：1", 1),
    ("設定値：2", 2),
    ("設定値：3", 3),
]

# リストを使ってラジオボタンを連続生成する
for text, value in radio_options:
    radio_btn = tk.Radiobutton(app, text=text, value=value, variable=selected_radio_var)
    radio_btn.pack(anchor="center", padx=20, pady=5)

# --------------------
# ボタン
# --------------------
# 関数を実行するボタン
submit_btn = tk.Button(app, text="処理を実行する", command=execute_by_selection)
submit_btn.pack(pady=15)

# ====================
# アプリの実行
# ====================
app.mainloop()
