# Task 05: Modelagem Não Supervisionada (Clustering + PCA)

## Objetivo
Descobrir **grupos naturais de voos** com base em características de rota e operação, sem usar o target. Os clusters devem ter interpretação de negócio clara. Gerar JSONs para visualização no dashboard.

## Contexto
- **Input:** `data/processed/flights_sample_processed.csv` + splits da Task 03
- **Output:** JSONs em `data/processed/dashboard/` com resultados de PCA e K-Means
- **Arquivo:** `src/04_unsupervised.py`

---

## Etapas

### 1. Seleção de features para clustering
Usar features que descrevem a natureza da rota/operação (sem leakage e sem o target):
- `DISTANCE`, `SCHEDULED_TIME`, `MONTH`, `DAY_OF_WEEK`, `SCHEDULED_DEPARTURE`
- Médias por par `(ORIGIN_AIRPORT, DESTINATION_AIRPORT)`: `avg_arrival_delay`, `delay_rate`, `flight_count`
- Resultado: **um vetor por rota** (não por voo individual) — mais semântico para clusterização

### 2. PCA — Redução de Dimensionalidade
- [ ] Ajustar PCA sobre features de rota (escalonadas)
- [ ] Gerar scree plot: variância explicada por componente e acumulada
- [ ] Determinar número de componentes para ≥ 85% da variância
- [ ] Salvar componentes principais (PC1, PC2) de cada rota para visualização
- [ ] Salvar loadings (contribuição de cada feature por componente)

### 3. K-Means sobre rotas
- [ ] Calcular inertia e silhouette score para K = 2 a 10
- [ ] Selecionar K ótimo combinando método Elbow + Silhouette (documentar decisão)
- [ ] Treinar K-Means final com K escolhido, `random_state=42`, `n_init=10`
- [ ] Atribuir cluster a cada rota

### 4. Análise e interpretação dos clusters
Para cada cluster, calcular:
- [ ] Número de rotas e volume total de voos
- [ ] Média e desvio padrão de: `DISTANCE`, `delay_rate`, `avg_arrival_delay`, `flight_count`
- [ ] Companhia predominante e top-3 aeroportos de origem
- [ ] **Rótulo interpretativo em português** (ex: "Rotas Curtas de Alta Pontualidade", "Hubs Congestionados")

---

## JSONs Gerados (output para dashboard)

```
data/processed/dashboard/
├── ml_pca_variance.json            # variância explicada por componente
├── ml_pca_scatter.json             # coordenadas PC1/PC2 de cada rota + cluster label
├── ml_kmeans_elbow.json            # inertia e silhouette por K
├── ml_cluster_profiles.json        # perfil estatístico de cada cluster
└── ml_cluster_routes.json          # lista de rotas com cluster_id, PC1, PC2, delay_rate
```

### Estrutura dos JSONs

**`ml_pca_variance.json`**
```json
{
  "n_components": 8,
  "explained_variance_ratio": [0.31, 0.18, 0.12, "..."],
  "cumulative_variance":       [0.31, 0.49, 0.61, "..."],
  "components_for_85pct": 5,
  "loadings": {
    "PC1": {"DISTANCE": 0.42, "SCHEDULED_TIME": 0.38, "...": "..."},
    "PC2": {"MONTH": 0.51, "DAY_OF_WEEK": 0.29, "...": "..."}
  }
}
```

**`ml_kmeans_elbow.json`**
```json
{
  "k_values":        [2, 3, 4, 5, 6, 7, 8, 9, 10],
  "inertia":         ["..."],
  "silhouette":      ["..."],
  "chosen_k":        4,
  "choice_reason":   "Elbow em K=4 + silhouette máximo em K=4"
}
```

**`ml_cluster_profiles.json`**
```json
{
  "n_clusters": 4,
  "clusters": [
    {
      "id": 0,
      "label": "Rotas Curtas Pontuais",
      "n_routes": 312,
      "n_flights": 48200,
      "avg_distance": 420,
      "avg_delay_rate": 0.31,
      "avg_arrival_delay": 8.2,
      "top_airlines": ["WN", "DL"],
      "top_origins": ["ATL", "ORD"]
    }
  ]
}
```

---

## Dependências
```
scikit-learn>=1.3.0
pyarrow>=14.0
```

## Ordem de Execução
```bash
python src/02_feature_engineering.py   # Task 03 (pré-requisito)
python src/04_unsupervised.py          # ← esta task
```

---

## Critérios de Sucesso

| Requisito (tc3.md) | Entregável | Status |
|---|---|---|
| Modelagem não supervisionada com interpretação | `ml_cluster_profiles.json` | ❌ |
| PCA com variância explicada | `ml_pca_variance.json` | ❌ |
| Clusterização com Elbow + Silhouette | `ml_kmeans_elbow.json` | ❌ |
| Rótulos interpretativos por cluster | Dentro de `ml_cluster_profiles.json` | ❌ |
| Outputs prontos para dashboard (Task 06) | Todos os JSONs em `dashboard/` | ❌ |

---

## Notas de DS
- **Granularidade:** clusterizar por **rota** (par origem-destino), não por voo — mais semântico.
- **Escalonamento:** PCA e K-Means são sensíveis a escala — escalonar antes.
- **Reprodutibilidade:** todo `random_state=42`.
- **Interpretação:** cada cluster deve ter um rótulo de negócio claro em português.
