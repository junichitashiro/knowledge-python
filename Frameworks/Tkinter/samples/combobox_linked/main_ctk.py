import customtkinter as ctk

# メニューAとメニューBの表示リスト
PREF_TO_CITIES = {
    '東京都': ['千代田区', '新宿区', '渋谷区'],
    '神奈川県': ['横浜市', '川崎市', '相模原市'],
    '大阪府': ['大阪市', '堺市', '吹田市'],
}


# =============================================
# メニューAの選択でメニューBの内容を更新する
# =============================================
def on_pref_changed(selected_pref: str) -> None:
    cities = PREF_TO_CITIES.get(selected_pref, [])

    # Bの候補を差し替え
    city_menu.configure(values=cities)

    # 候補があれば先頭、なければブランクにする
    if cities:
        city_var.set(cities[0])
    else:
        city_var.set('')


# --------------------
# GUIの設定
# --------------------
# 基本設定
app = ctk.CTk()
app.title('オプションメニューの設定値による制御')
app.geometry('350x200')
# 2列目を伸縮させる
app.grid_columnconfigure(1, weight=1)

# --------------------
# オプションメニュー
# --------------------
# メニューA：都道府県
pref_var = ctk.StringVar(value='東京都')
pref_menu = ctk.CTkOptionMenu(
    app,
    values=list(PREF_TO_CITIES.keys()),
    variable=pref_var,
    command=on_pref_changed,   # 変更時に呼ばれる（選択した都道府県を渡す）
)

# メニューB：市区町村（初期は東京都に合わせる）
city_var = ctk.StringVar()
city_menu = ctk.CTkOptionMenu(
    app,
    values=[],
    variable=city_var
)

# --------------------
# ラベル
# --------------------
# 都道府県ラベル
label_pref = ctk.CTkLabel(app, text='【都道府県】')
# 市区町村ラベル
label_city = ctk.CTkLabel(app, text='【市区町村】')

# --------------------
# 配置
# --------------------
# グリッド1行目に配置
label_pref.grid(row=0, column=0, padx=12, pady=(24, 16), sticky='w')
pref_menu.grid(row=0, column=1, padx=12, pady=(24, 16), sticky='ew')

# グリッド2行目に配置
label_city.grid(row=1, column=0, padx=12, pady=16, sticky='w')
city_menu.grid(row=1, column=1, padx=12, pady=16, sticky='ew')

# ====================
# アプリの実行
# ====================
# 初期同期でメニューBを埋めておく
on_pref_changed(pref_var.get())

app.mainloop()
