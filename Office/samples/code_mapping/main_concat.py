from __future__ import annotations

import pandas as pd


def main() -> None:

    input_txt = 'input.txt'
    table_xlsx = '読替テーブル.xlsx'
    output_txt = 'output.txt'

    # 入力ファイルをデータフレームに格納する
    df = pd.read_csv(input_txt, sep='\t', dtype=str).fillna('')
    # 読替テーブルをデータフレームに格納する
    replace_table = pd.read_excel(table_xlsx, dtype=str).fillna('')

    # 複数列を連結した新しい列を作る
    replace_table['連結住所'] = (replace_table['市区町村'] + replace_table['住所'])

    # 読替テーブルのキーになる列と、読み替える値の列で辞書を作る
    key_col = '郵便番号'
    replace_col = '連結住所'
    mapping_dict = dict(
        zip(
            replace_table[key_col].astype(str),
            replace_table[replace_col].astype(str)
        )
    )

    # ZIPCODE を 住所 で置換（見つからない場合は元の値を保持）
    df['ZIPCODE'] = (df['ZIPCODE'].astype(str).map(mapping_dict).fillna(df['ZIPCODE']))

    # 読み替え後のファイル出力
    df = df.rename(columns={'ZIPCODE': 'CONCAT_ZIPCODE'})
    df.to_csv(output_txt, sep='\t', index=False, encoding='utf-8')


if __name__ == '__main__':
    main()
