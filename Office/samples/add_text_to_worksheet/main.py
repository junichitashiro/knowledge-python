import pandas as pd

# テキストファイルを読み込む
text_file = '/path/to/text_file.txt'
with open(text_file, 'r') as file:
    lines = file.readlines()

# 読み込んだデータをリストに格納
data = []
for line in lines:
    data.append(line.strip())   # 不要な空白を削除

# データフレームを作成
df = pd.DataFrame(data)

# Excelファイルを読み込む
excel_file = '/path/to/excel_file.xlsx'
book = pd.read_excel(excel_file, sheet_name=None)
sheet_names = pd.ExcelFile(excel_file).sheet_names

# 書き込み用シートにデータフレームを追加する
sheet_name = 'Sheet1'  # 書き込むシート名
book[sheet_name] = df

# Excelファイルに書き込む（シートがない場合は追加する）
if sheet_name not in sheet_names:
    with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
else:
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

print('書き込み完了')
