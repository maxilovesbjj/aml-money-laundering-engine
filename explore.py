import duckdb
import networkx as nx
import matplotlib.pyplot as plt
import os

raw_path = "data/raw/paysim.csv"
parquet_path = "data/processed/paysim_filtered.parquet"
image_path = "data/processed/layering_sample.png"

def run_eda():
    # 1. Procesamiento ETL super rapido con DuckDB
    if not os.path.exists(parquet_path):
        print(f"Filtrando {raw_path} a Parquet (TRANSFER y CASH_OUT)...")
        conn = duckdb.connect()
        conn.execute(f"""
            COPY (
                SELECT * FROM read_csv_auto('{raw_path}')
                WHERE type IN ('TRANSFER', 'CASH_OUT')
            ) TO '{parquet_path}' (FORMAT PARQUET);
        """)
        print("Parquet generado con exito en data/processed/")
    else:
        print("Parquet ya existe. Saltando filtrado.")

    # 2. Extraccion de muestra fraudulenta para el grafo
    print("Extrayendo un esquema de lavado para visualizar...")
    conn = duckdb.connect()
    
    # Buscamos transacciones donde origenes fraudulentos envian a destinos, y que hacen esos destinos
    df_graph = conn.execute(f"""
        WITH fraudulent_transfers AS (
            SELECT nameOrig, nameDest, amount, type 
            FROM '{parquet_path}' 
            WHERE isFraud = 1 AND type = 'TRANSFER'
            LIMIT 15
        )
        SELECT * FROM fraudulent_transfers
        UNION
        SELECT p.nameOrig, p.nameDest, p.amount, p.type 
        FROM '{parquet_path}' p
        INNER JOIN fraudulent_transfers f ON p.nameOrig = f.nameDest
    """).df()

    # 3. Construccion de la red dirigida
    G = nx.from_pandas_edgelist(
        df_graph,
        source='nameOrig',
        target='nameDest',
        edge_attr=['amount', 'type'],
        create_using=nx.DiGraph()
    )

    print(f"Grafo construido: {G.number_of_nodes()} nodos y {G.number_of_edges()} transacciones (aristas).")

    # 4. Exportar visualizacion
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5, seed=42)
    
    # Diferenciar colores segun si es origen (rojo) o destino intermedio (azul)
    node_colors = ['red' if node in df_graph['nameOrig'].values else 'skyblue' for node in G.nodes()]
    
    nx.draw(G, pos, with_labels=False, node_size=100, node_color=node_colors, edge_color='gray', arrows=True)
    plt.title("Topologia AML: Esquema de Layering y Cuentas Mula (Rojo=Origen, Azul=Intermediario)")
    
    plt.savefig(image_path)
    print(f"Grafico guardado en: {image_path}. ¡Abrelo para ver la red!")

if __name__ == "__main__":
    run_eda()
