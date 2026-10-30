import pandas as pd

def compute_graph_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Fan-out: A cuantas cuentas distintas envia el origen
    out_degree = df.groupby('nameOrig')['nameDest'].nunique().reset_index(name='orig_out_degree')
    
    # Fan-in: De cuantas cuentas distintas recibe el destino
    in_degree = df.groupby('nameDest')['nameOrig'].nunique().reset_index(name='dest_in_degree')
    
    df = df.merge(out_degree, on='nameOrig', how='left')
    df = df.merge(in_degree, on='nameDest', how='left')
    
    df['orig_out_degree'] = df['orig_out_degree'].fillna(0)
    df['dest_in_degree'] = df['dest_in_degree'].fillna(0)
    
    return df
