# Task 02: Modelagem ML — Supervisionada e Não Supervisionada

> [!IMPORTANT]
> **Esta task foi decomposta nas seguintes tasks menores:**
> - **Task 03** — Feature Engineering (`src/02_feature_engineering.py`)
> - **Task 04** — Modelagem Supervisionada (`src/03_supervised_classification.py`)
> - **Task 05** — Modelagem Não Supervisionada (`src/04_unsupervised.py`)
> - **Task 06** — Relatório Crítico (`src/05_model_report.py`)
>
> Consulte os arquivos `tasks/task03.md` a `tasks/task06.md` para os detalhes de cada etapa.

## Objetivo
Implementar os modelos de Machine Learning exigidos pelo Tech Challenge Fase 3, produzindo **artefatos JSON estruturados** que serão consumidos pelo dashboard interativo na Task 03. Toda saída numérica deve ser serializada em JSON — o dashboard não acessa os modelos `.pkl` diretamente.

## Contexto
- **Input principal:** `data/processed/flights_sample_processed.csv`
- **Cenário preditivo:** prever atraso **antes do voo decolar** — portanto, **sem usar** `DEPARTURE_DELAY`, `ARRIVAL_DELAY`, `TAXI_OUT`, `TAXI_IN`, `AIR_TIME` nem `ELAPSED_TIME` como features (data leakage).
- **Pipeline de saída:** cada script gera JSONs em `data/processed/dashboard/` prontos para visualização.

---

## Premissas de Ciência de Dados

### Definição do Problema
- **Classificação binária principal:** `IS_DELAYED` (1 = chegada > **15 min** de atraso)
- A aviação considera atrasos de até 15 minutos como toleráveis — somente acima de 15 min é classificado como atraso real.
- **Regressão auxiliar:** `ARRIVAL_DELAY` em minutos (somente para voos atrasados)
- Foco no cenário **pré-decolagem**: o modelo só usa o que o passageiro/operador sabe antes do voo sair.

### Features Permitidas (sem data leakage)
| Feature | Tipo | Justificativa |
|---|---|---|
| `MONTH` | int | Sazonalidade |
| `DAY_OF_WEEK` | int | Padrão semanal |
| `SCHEDULED_DEPARTURE` | int | Horário planejado |
| `SCHEDULED_ARRIVAL` | int | Horário planejado |
| `DISTANCE` | float | Característica da rota |
| `AIRLINE` | category | Operadora |
| `ORIGIN_AIRPORT` | category | Aeroporto origem |
| `DESTINATION_AIRPORT` | category | Aeroporto destino |
| `DEPARTURE_PERIOD` | category | Período do dia (derivado) |
| `SCHEDULED_TIME` | float | Duração planejada |

### Tratamento de Desbalanceamento
- Verificar razão de classes de `IS_DELAYED` (espera-se ~40-60% atrasados)
- Se desbalanceado (< 30% ou > 70% de uma classe): usar `class_weight='balanced'` e reportar impacto

---

## Script 1: Feature Engineering

**Arquivo:** `src/02_feature_engineering.py`

### 1.1 Carregamento e seleção
- [ ] Carregar `data/processed/flights_sample_processed.csv`
- [ ] Selecionar apenas as features permitidas (sem leakage)
- [ ] Remover linhas com `IS_DELAYED` nulo (target obrigatório)
- [ ] Remover linhas com `CANCELLED == 1` (voo não decolou — diferente de atraso)

### 1.2 Tratamento de nulos
- [ ] Numéricas: imputar com **mediana** do treino (nunca do dataset completo para evitar leakage)
- [ ] Categóricas: imputar com `'UNKNOWN'` como nova categoria

### 1.3 Encoding
- [ ] `AIRLINE` → **Target Encoding** (média de `IS_DELAYED` por companhia no treino)
- [ ] `ORIGIN_AIRPORT`, `DESTINATION_AIRPORT` → **Target Encoding** (mesma lógica)
- [ ] `DEPARTURE_PERIOD` → **One-Hot Encoding** (4 categorias: Morning, Afternoon, Evening, Night)
- [ ] Salvar mapeamentos em `models/encoders.json` para uso em inferência no dashboard

### 1.4 Splitting estratificado
- [ ] Split **estratificado** por `IS_DELAYED` para manter proporção de classes
- [ ] Proporção: **70% treino / 15% validação / 15% teste** com `random_state=42`
- [ ] Verificar e imprimir distribuição de classes em cada split

### 1.5 Escalonamento
- [ ] `StandardScaler` ajustado **apenas** no treino
- [ ] Transformar treino, validação e teste com o mesmo scaler
- [ ] Salvar em `models/scaler.pkl`

### 1.6 Outputs do script
```
data/processed/
├── X_train.parquet    # mais eficiente que CSV para dados grandes
├── X_val.parquet
├── X_test.parquet
├── y_train.parquet
├── y_val.parquet
└── y_test.parquet
models/
├── scaler.pkl
└── encoders.json      # mapeamentos para decodificar no dashboard
```

---

## Script 2: Modelagem Supervisionada

**Arquivo:** `src/03_supervised_classification.py`

### 2.1 Modelos a treinar
- [ ] **Modelo A — Regressão Logística** (`LogisticRegression`)
  - `max_iter=1000`, `class_weight='balanced'`, `random_state=42`
  - Serve como **baseline** interpretável
- [ ] **Modelo B — Random Forest** (`RandomForestClassifier`)
  - `n_estimators=200`, `max_depth=15`, `min_samples_leaf=50`, `class_weight='balanced'`, `random_state=42`, `n_jobs=-1`
  - Modelo principal com melhor capacidade preditiva
- [ ] **Modelo C — Gradient Boosting** (`GradientBoostingClassifier` ou `HistGradientBoostingClassifier`)
  - `max_iter=200`, `max_depth=6`, `learning_rate=0.05`, `random_state=42` 
  - Alternativa rápida e robusta (HistGradientBoosting suporta nulos nativamente)

### 2.2 Avaliação rigorosa
Para cada modelo, calcular no **conjunto de teste** (nunca visto durante treino):
- [ ] Acurácia, Precisão, Recall, F1-Score (ponderado e por classe)
- [ ] AUC-ROC (`roc_auc_score`)
- [ ] AUC-PR (`average_precision_score`) — mais informativo para dados desbalanceados
- [ ] Matriz de confusão completa (TN, FP, FN, TP)
- [ ] Curva ROC: pontos `(fpr, tpr, thresholds)` para cada modelo
- [ ] Curva Precision-Recall: pontos `(precision, recall, thresholds)`
- [ ] Comparar métricas em treino vs validação vs teste (detectar overfitting)

### 2.3 Threshold Optimization
- [ ] Para o melhor modelo, calcular F1/precision/recall para thresholds de 0.1 a 0.9
- [ ] Identificar threshold ótimo (máximo F1) vs threshold padrão 0.5
- [ ] Salvar curva de threshold no JSON para o dashboard permitir ajuste interativo

### 2.4 Feature Importance
- [ ] **Random Forest:** `feature_importances_` (Gini importance)
- [ ] **Logistic Regression:** coeficientes absolutos como proxy de importância
- [ ] **SHAP Values** (opcional, se `shap` disponível): explicação local por instância
- [ ] Produzir ranking das top-20 features com nome, importância e direção (positivo/negativo no delay)

### 2.5 Previsões no conjunto de teste (para o dashboard)
- [ ] Salvar sample de previsões (até 5.000 registros) com:
  - Features originais decodificadas (nomes legíveis, não encoded)
  - `y_true`, `y_pred`, `y_prob` (probabilidade de atraso)
  - `AIRLINE_NAME`, `ORIGIN_AIRPORT`, `DESTINATION_AIRPORT` (nomes de negócio)

### 2.6 Persistência
- [ ] `models/logistic_regression.pkl`
- [ ] `models/random_forest.pkl`
- [ ] `models/gradient_boosting.pkl`

### 2.7 JSONs gerados (output para dashboard)
```
data/processed/dashboard/
├── ml_model_comparison.json        # tabela comparativa de métricas dos 3 modelos
├── ml_roc_curves.json              # pontos (fpr, tpr) de cada modelo para plotar curva ROC
├── ml_pr_curves.json               # pontos (precision, recall) para curva P-R
├── ml_confusion_matrices.json      # matrizes de confusão dos 3 modelos
├── ml_feature_importance.json      # top-20 features com importância e direção
├── ml_threshold_analysis.json      # F1/precision/recall por threshold do melhor modelo
└── ml_test_predictions.json        # sample de previsões com contexto (até 5000 linhas)
```

#### Estrutura dos JSONs

**`ml_model_comparison.json`**
```json
{
  "models": ["Logistic Regression", "Random Forest", "Gradient Boosting"],
  "metrics": {
    "accuracy":        [0.72, 0.81, 0.83],
    "f1_weighted":     [0.71, 0.80, 0.82],
    "roc_auc":         [0.78, 0.88, 0.90],
    "avg_precision":   [0.75, 0.86, 0.88],
    "precision_1":     [0.68, 0.79, 0.81],
    "recall_1":        [0.74, 0.83, 0.85],
    "train_accuracy":  [0.73, 0.89, 0.91],
    "val_accuracy":    [0.72, 0.82, 0.83]
  },
  "best_model": "Gradient Boosting",
  "class_balance": {"0": 0.42, "1": 0.58}
}
```

**`ml_roc_curves.json`**
```json
{
  "Logistic Regression": {"fpr": [...], "tpr": [...], "auc": 0.78},
  "Random Forest":        {"fpr": [...], "tpr": [...], "auc": 0.88},
  "Gradient Boosting":    {"fpr": [...], "tpr": [...], "auc": 0.90}
}
```

**`ml_feature_importance.json`**
```json
{
  "model": "Random Forest",
  "features": [
    {"name": "SCHEDULED_DEPARTURE", "importance": 0.18, "direction": "positive"},
    {"name": "airline_target_enc",  "importance": 0.14, "direction": "positive"},
    ...
  ]
}
```

**`ml_test_predictions.json`**
```json
{
  "sample_size": 5000,
  "columns": ["AIRLINE", "ORIGIN", "DESTINATION", "MONTH", "DAY_OF_WEEK",
               "SCHEDULED_DEPARTURE", "DISTANCE", "y_true", "y_pred", "y_prob"],
  "data": [[...], ...]
}
```

---

## Script 3: Modelagem Não Supervisionada

**Arquivo:** `src/04_unsupervised.py`

> Objetivo: descobrir **grupos naturais de voos** com base em características de rota e operação, sem usar o target. Os clusters devem ter interpretação de negócio clara.

### 3.1 Seleção de features para clustering
Usar features que descrevem a natureza da rota/operação (sem leakage e sem o target):
- `DISTANCE`, `SCHEDULED_TIME`, `MONTH`, `DAY_OF_WEEK`, `SCHEDULED_DEPARTURE`
- Médias por par `(ORIGIN_AIRPORT, DESTINATION_AIRPORT)`: `avg_arrival_delay`, `delay_rate`, `flight_count`
- Resultado: **um vetor por rota** (não por voo individual) — mais semântico para clusterização

### 3.2 PCA — Redução de Dimensionalidade
- [ ] Ajustar PCA sobre features de rota (escalonadas)
- [ ] Gerar scree plot: variância explicada por componente e acumulada
- [ ] Determinar número de componentes para ≥ 85% da variância
- [ ] Salvar componentes principais (PC1, PC2) de cada rota para visualização
- [ ] Salvar loadings (contribuição de cada feature por componente)

### 3.3 K-Means sobre rotas
- [ ] Calcular inertia e silhouette score para K = 2 a 10
- [ ] Selecionar K ótimo combinando método Elbow + Silhouette (documentar decisão)
- [ ] Treinar K-Means final com K escolhido, `random_state=42`, `n_init=10`
- [ ] Atribuir cluster a cada rota

### 3.4 Análise e interpretação dos clusters
Para cada cluster, calcular:
- [ ] Número de rotas e volume total de voos
- [ ] Média e desvio padrão de: `DISTANCE`, `delay_rate`, `avg_arrival_delay`, `flight_count`
- [ ] Companhia predominante e top-3 aeroportos de origem
- [ ] **Rótulo interpretativo em português** (ex: "Rotas Curtas de Alta Pontualidade", "Hubs Congestionados")

### 3.5 JSONs gerados (output para dashboard)
```
data/processed/dashboard/
├── ml_pca_variance.json            # variância explicada por componente
├── ml_pca_scatter.json             # coordenadas PC1/PC2 de cada rota + cluster label
├── ml_kmeans_elbow.json            # inertia e silhouette por K
├── ml_cluster_profiles.json        # perfil estatístico de cada cluster
└── ml_cluster_routes.json          # lista de rotas com cluster_id, PC1, PC2, delay_rate
```

#### Estrutura dos JSONs

**`ml_pca_variance.json`**
```json
{
  "n_components": 8,
  "explained_variance_ratio": [0.31, 0.18, 0.12, ...],
  "cumulative_variance":       [0.31, 0.49, 0.61, ...],
  "components_for_85pct": 5,
  "loadings": {
    "PC1": {"DISTANCE": 0.42, "SCHEDULED_TIME": 0.38, ...},
    "PC2": {"MONTH": 0.51, "DAY_OF_WEEK": 0.29, ...}
  }
}
```

**`ml_kmeans_elbow.json`**
```json
{
  "k_values":        [2, 3, 4, 5, 6, 7, 8, 9, 10],
  "inertia":         [...],
  "silhouette":      [...],
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

## Script 4: Relatório Crítico

**Arquivo:** `src/05_model_report.py` → gera `docs/model_report.md`

- [ ] Carregar todos os JSONs gerados anteriormente
- [ ] Gerar `docs/model_report.md` programaticamente com:
  - Tabela comparativa de métricas
  - Decisões tomadas e justificativas (leakage, desbalanceamento, threshold)
  - Interpretação de cada cluster
  - Respostas às perguntas norteadoras do tc3.md
  - Limitações e próximos passos

---

## Estrutura Final de Saída

```
data/processed/dashboard/
│
│  ── Supervisionado ──────────────────────────────────────
├── ml_model_comparison.json      # métricas comparativas
├── ml_roc_curves.json            # curvas ROC dos modelos
├── ml_pr_curves.json             # curvas Precision-Recall
├── ml_confusion_matrices.json    # matrizes de confusão
├── ml_feature_importance.json    # importância de features
├── ml_threshold_analysis.json    # análise de threshold ótimo
├── ml_test_predictions.json      # amostra de previsões com contexto
│
│  ── Não supervisionado ──────────────────────────────────
├── ml_pca_variance.json          # variância explicada PCA
├── ml_pca_scatter.json           # scatter PC1 x PC2 por rota
├── ml_kmeans_elbow.json          # inertia/silhouette por K
├── ml_cluster_profiles.json      # perfil de cada cluster
└── ml_cluster_routes.json        # rotas com cluster_id e coords PCA

models/
├── logistic_regression.pkl
├── random_forest.pkl
├── gradient_boosting.pkl
├── scaler.pkl
└── encoders.json

docs/
└── model_report.md
```

---

## Dependências

```
# Adicionar ao requirements.txt
scikit-learn>=1.3.0
joblib>=1.3.0
pyarrow>=14.0       # para .parquet
shap>=0.44.0        # opcional — SHAP values
```

---

## Ordem de Execução

```bash
python src/01_eda.py                        # Task 01 — gera flights_sample_processed.csv
python src/02_feature_engineering.py        # splits, encoding, scaler
python src/03_supervised_classification.py  # treina modelos, gera JSONs supervisionados
python src/04_unsupervised.py               # PCA, K-Means, gera JSONs não supervisionados
python src/05_model_report.py               # gera docs/model_report.md
```

---

## Critérios de Sucesso

| Requisito (tc3.md) | Entregável | Status |
|---|---|---|
| ≥ 2 algoritmos supervisionados comparados | `ml_model_comparison.json` | ❌ |
| Métricas adequadas (F1, AUC-ROC, AUC-PR) | `ml_roc_curves.json`, `ml_pr_curves.json` | ❌ |
| Sem data leakage | features pré-voo apenas | ❌ |
| Modelagem não supervisionada com interpretação | `ml_cluster_profiles.json` | ❌ |
| PCA com variância explicada | `ml_pca_variance.json` | ❌ |
| Outputs prontos para dashboard (Task 03) | todos os JSONs em `dashboard/` | ❌ |
| Relatório crítico com limitações | `docs/model_report.md` | ❌ |

---

## Notas de DS

- **Leakage:** `DEPARTURE_DELAY` é o principal risco — **não usar** como feature de entrada.
- **Escala:** amostra de 10% do dataset (~590k voos). Scripts devem rodar em < 10 min.
- **Reprodutibilidade:** todo `random_state=42`.
- **Parquet:** usar `.parquet` em vez de `.csv` para os splits intermediários (10x menor, 5x mais rápido para ler).
- **Target Encoding:** calcular **somente no treino** e aplicar no val/teste — evita leakage de grupo.
- **Dashboard contrato:** os JSONs são o contrato entre Task 02 e Task 03. A estrutura dos JSONs define o que o dashboard pode exibir — **não alterar as chaves** após a Task 03 começar.
