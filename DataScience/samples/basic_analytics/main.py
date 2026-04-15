import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns

print('>>> 処理開始')

# TSVファイルを読み込む
df = pd.read_csv('input.tsv', sep='\t')

# ★から始まる列をダミー変数化する
columns = df.columns

for col in df.columns:
    if col.startswith('★'):
        df = pd.get_dummies(df, columns=[col])

print('>>> データ出力中・・・')

# 基本統計量をエクセルに出力する
df.describe().to_excel('基本統計量.xlsx')

# 相関係数を変数に格納する
cor = df.corr()

# 相関係数をエクセルに出力する
cor.to_excel('相関係数.xlsx')

# 相関係数のヒートマップを変数に格納する
heatmap = sns.heatmap(cor, cmap=sns.color_palette('Blues', 20, as_cmap=True), annot=True, fmt='.2f', vmin=-1, vmax=1)

# ヒートマップを出力する
plt.savefig('相関係数.png', bbox_inches='tight')

print('>>> 処理終了')
