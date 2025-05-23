import pandas as pd

def drop_empty_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove colunas que são todas NaN."""
    return df.dropna(axis=1, how='all')

def normalize_dates(df: pd.DataFrame, date_cols: list[str]) -> pd.DataFrame:
    """Converte colunas de data para datetime padrão."""
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def flatten_nested_json(df: pd.DataFrame, field: str) -> pd.DataFrame:
    """Explode um campo JSON aninhado em colunas planas."""
    nested = pd.json_normalize(df[field])
    return pd.concat([df.drop(columns=[field]), nested], axis=1)
