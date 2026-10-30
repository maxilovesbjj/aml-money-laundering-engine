import pandas as pd
from src.features.balance import compute_balance_sensors
from src.graph.metrics import compute_graph_features

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = compute_balance_sensors(df)
    df = compute_graph_features(df)
    return df
