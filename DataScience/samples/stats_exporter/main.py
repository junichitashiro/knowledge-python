from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

# 入出力ファイルの設定
INPUT_FILE = "input.tsv"
OUTPUT_STATS_FILE = "基本統計量.xlsx"
OUTPUT_CORR_FILE = "相関係数.xlsx"
OUTPUT_HEATMAP_FILE = "相関係数.png"

# ダミー変数化の対象列を示すプレフィックス
DUMMY_TARGET_PREFIX = "★"

# ヒートマップの設定
HEATMAP_CMAP = sns.color_palette("Blues", 20, as_cmap=True)
HEATMAP_VMIN = -1
HEATMAP_VMAX = 1

# matplotlibの日本語フォント設定
# Windowsの場合はMS Gothic、MacはHiragino Sans、Linuxはいずれかのインストール済みフォントを指定する
plt.rcParams["font.family"] = "MS Gothic"


def load_tsv(file_path: str) -> pd.DataFrame:
    """
    TSVファイルを読み込んでDataFrameを返す。

    Args:
        file_path: 読み込むTSVファイルのパス

    Returns:
        読み込んだDataFrame
    """
    return pd.read_csv(file_path, sep="\t")


def apply_dummies(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    """
    指定のプレフィックスで始まる列をダミー変数化して返す。

    Args:
        df: 処理対象のDataFrame
        prefix: ダミー変数化の対象列を示すプレフィックス

    Returns:
        ダミー変数化後のDataFrame
    """
    target_columns = [col for col in df.columns if col.startswith(prefix)]
    return pd.get_dummies(df, columns=target_columns)


def export_stats(df: pd.DataFrame, output_path: str) -> None:
    """
    基本統計量をExcelファイルに出力する。

    Args:
        df: 集計対象のDataFrame
        output_path: 出力先のファイルパス
    """
    df.describe().to_excel(output_path)
    print(f"基本統計量を出力しました: {output_path}")


def export_correlation(df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    """
    相関係数をExcelファイルに出力して相関係数のDataFrameを返す。
    この関数の戻り値を export_heatmap() の corr_df に渡すことができる。

    Args:
        df: 集計対象のDataFrame
        output_path: 出力先のファイルパス

    Returns:
        相関係数のDataFrame
    """
    corr_df = df.corr()
    corr_df.to_excel(output_path)
    print(f"相関係数を出力しました: {output_path}")
    return corr_df


def export_heatmap(corr_df: pd.DataFrame, output_path: str) -> None:
    """
    相関係数のヒートマップを画像ファイルに出力する。
    export_correlation() の戻り値をそのまま corr_df に渡すことができる。

    Args:
        corr_df: 相関係数のDataFrame
        output_path: 出力先のファイルパス
    """
    sns.heatmap(
        corr_df,
        cmap=HEATMAP_CMAP,
        annot=True,
        fmt=".2f",
        vmin=HEATMAP_VMIN,
        vmax=HEATMAP_VMAX,
    )
    plt.savefig(output_path, bbox_inches="tight")
    print(f"ヒートマップを出力しました: {output_path}")


if __name__ == "__main__":
    print(">>> 処理開始")

    # TSVを読み込んでダミー変数化する
    df = load_tsv(INPUT_FILE)
    df = apply_dummies(df, DUMMY_TARGET_PREFIX)

    # 基本統計量・相関係数・ヒートマップを出力する
    export_stats(df, OUTPUT_STATS_FILE)
    corr_df = export_correlation(df, OUTPUT_CORR_FILE)
    export_heatmap(corr_df, OUTPUT_HEATMAP_FILE)

    print(">>> 処理終了")
