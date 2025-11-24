# data_analysis.py
import pandas as pd

def load_data(path="data/sample_data.csv", parse_dates=["date"]):
    df = pd.read_csv(path, parse_dates=parse_dates)
    return df

def summary(df):
    """Retorna um resumo rápido do dataset"""
    info = {
        "n_rows": len(df),
        "n_columns": df.shape[1],
        "columns": list(df.columns),
        "missing_perc": (df.isna().mean() * 100).round(2).to_dict(),
        "descriptive": df.describe(datetime_is_numeric=True).to_dict()
    }
    return info

def preprocess(df):
    """Exemplo de pré-processamento:
    - cria colunas de período
    - agrega por dia/semana/mês
    """
    df = df.copy()
    if "date" in df.columns:
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day
        df["week"] = df["date"].dt.isocalendar().week
    # Exemplo: remover duplicatas
    df = df.drop_duplicates()
    return df

def aggregate_by(df, group_cols, agg_col="value", agg_func="sum"):
    return df.groupby(group_cols)[agg_col].agg(agg_func).reset_index()
