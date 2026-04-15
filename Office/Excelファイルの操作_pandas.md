# Excelファイルの操作_pandas

## テストデータの内容

### Sheet1

  | 行＼列 |   A    |   B    |   C    |
  | :----: | :----: | :----: | :----: |
  |   1    | HEAD_A | HEAD_B | HEAD_C |
  |   2    |   AA   |   BB   |   CC   |
  |   3    |  AAA   |  BBB   |  CCC   |

### Sheet2

  | 行＼列 |    A    |    B    |    C    |
  | :----: | :-----: | :-----: | :-----: |
  |   1    | HEAD_A2 | HEAD_B2 | HEAD_C2 |
  |   2    |   AA2   |   BB2   |   CC2   |
  |   3    |  AAA2   |  BBB2   |  CCC2   |

---

## read_excel()関数 を使った基本動作

* 1回の関数呼び出しで直接データフレームを取得する
* 毎回Excelファイルを開くため複数シートを読む場合は非効率

### シートを指定してデータフレームに格納する

```python
import pandas as pd

df = pd.read_excel('test.xlsx', sheet_name='Sheet1', header=None)
print(df)
```

### 実行結果

```
        0       1       2
0  HEAD_A  HEAD_B  HEAD_C
1      AA      BB      CC
2     AAA     BBB     CCC
```

### 特定のセルの値を取得する

* ヘッダの有無で扱いが変わるためここでは header=None を指定する

```python
import pandas as pd

df = pd.read_excel('test.xlsx', sheet_name='Sheet1', header=None)
print(df.iloc[1, 1])
```
### 実行結果

> BB

### 全シートを辞書形式で取得する

#### シート名の一覧を表示する

```python
import pandas as pd

dfs = pd.read_excel('test.xlsx', sheet_name=None)
print(dfs.keys())
```
#### 実行結果

> dict_keys(['Sheet1', 'Sheet2'])

#### 特定のシートのデータフレームを表示する

```python
import pandas as pd

dfs = pd.read_excel('test.xlsx', sheet_name=None)
print(dfs['Sheet2'])
```
#### 実行結果

```
  HEAD_A2 HEAD_B2 HEAD_C2
0     AA2     BB2     CC2
1    AAA2    BBB2    CCC2
```

---

## ExcelFile()関数 を使った基本動作

* 最初にExcelファイル全体を読み込んでメモリ上に展開し、必要なシートを後で取得できる
* シート名の一覧を取得できる
* 複数のシートを読むときに高速

### Excelファイル（全体）を読み込む

#### シート名の一覧を表示する

```python
import pandas as pd

wb = pd.ExcelFile('test.xlsx')
wb.sheet_names
```

#### 実行結果

> ['Sheet1', 'Sheet2']
