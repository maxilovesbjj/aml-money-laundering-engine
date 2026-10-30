import pandas as pd
import numpy as np

def compute_balance_sensors(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Errores contables
    df['error_balance_origen'] = df['newbalanceOrig'] + df['amount'] - df['oldbalanceOrg']
    df['error_balance_destino'] = df['oldbalanceDest'] + df['amount'] - df['newbalanceDest']
    
    # Firma de cuenta mula (vaciado total)
    df['flag_vaciado'] = np.where(df['amount'] == df['oldbalanceOrg'], 1, 0)
    
    # Encoding canal vulnerable
    df['type_encoded'] = np.where(df['type'] == 'TRANSFER', 1, 0)
    return df
