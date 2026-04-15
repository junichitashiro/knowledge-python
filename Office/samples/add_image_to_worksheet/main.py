from openpyxl import load_workbook
from openpyxl.drawing.image import Image

image_file = '/path/to/image.png'  # 画像ファイルのパス
excel_file = '/path/to/excel.xlsx'  # Excelファイルのパス
sheet_name = 'Sheet1'  # ワークシート名
cell_range = 'B11'  # 貼り付けるセル位置

# Excelファイルを読み込む
wb = load_workbook(excel_file)

# 指定した名前のシートが存在しなかったら追加する
if sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
else:
    ws = wb.create_sheet(title=sheet_name)

# 画像をワークシートに貼り付ける
img = Image(image_file)
ws.add_image(img, cell_range)

# Excelファイルを上書き保存する
wb.save(excel_file)
print(f'{sheet_name} シートの {cell_range} セルに画像を追加')
