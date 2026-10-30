# Motor de Detección de Lavado de Dinero (Network Analysis)

Motor híbrido para detectar esquemas de *layering* y lavado de activos combinando:
1. **Señal transaccional:** Física de balances y anomalías contables.
2. **Señal de red (Grafos):** Topología origen-destino mediante NetworkX para identificar estructuras complejas de blanqueo.
3. **Explicabilidad (SHAP):** Atribución de variables para respaldar Reportes de Operación Sospechosa (ROS).

## Arquitectura
- **Procesamiento y Grafo:** DuckDB, NetworkX
- **Machine Learning:** XGBoost, Scikit-Learn, SHAP
- **Inferencia:** FastAPI, Pydantic v2

## Limitaciones de la v1
- Entrenado sobre dataset sintético (PaySim).
- El grafo de transacciones se construye offline en el pipeline de entrenamiento. En inferencia se utilizan features topológicas precomputadas por cuenta para garantizar baja latencia.
