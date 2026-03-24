# Task 04: Modelagem Supervisionada (Classificação)

## Objetivo
Treinar e avaliar 3 modelos de classificação binária para prever atrasos de voos (atraso = chegada > **15 min** do previsto), gerando **JSONs estruturados** para o dashboard interativo.

## Contexto
- **Input:** splits Parquet gerados pela Task 03 (`X_train`, `X_val`, `X_test`, `y_train`, `y_val`, `y_test`)
- **Output:** modelos `.pkl` + JSONs em `data/processed/dashboard/`
- **Arquivo:** `src/03_supervised_classification.py`

---

## Etapas

### 1. Modelos a treinar
- [ ] **Modelo A — Regressão Logística** (`LogisticRegression`)
  - `max_iter=1000`, `class_weight='balanced'`, `random_state=42`
  - Serve como **baseline** interpretável
- [ ] **Modelo B — Random Forest** (`RandomForestClassifier`)
  - `n_estimators=200`, `max_depth=15`, `min_samples_leaf=50`, `class_weight='balanced'`, `random_state=42`, `n_jobs=-1`
  - Modelo principal com melhor capacidade preditiva
- [ ] **Modelo C — Gradient Boosting** (`GradientBoostingClassifier` ou `HistGradientBoostingClassifier`)
  - `max_iter=200`, `max_depth=6`, `learning_rate=0.05`, `random_state=42`
  - Alternativa rápida e robusta (HistGradientBoosting suporta nulos nativamente)

### 2. Avaliação rigorosa
Para cada modelo, calcular no **conjunto de teste** (nunca visto durante treino):
- [ ] Acurácia, Precisão, Recall, F1-Score (ponderado e por classe)
- [ ] AUC-ROC (`roc_auc_score`)
- [ ] AUC-PR (`average_precision_score`) — mais informativo para dados desbalanceados
- [ ] Matriz de confusão completa (TN, FP, FN, TP)
- [ ] Curva ROC: pontos `(fpr, tpr, thresholds)` para cada modelo
- [ ] Curva Precision-Recall: pontos `(precision, recall, thresholds)`
- [ ] Comparar métricas em treino vs validação vs teste (detectar overfitting)

### 3. Threshold Optimization
- [ ] Para o melhor modelo, calcular F1/precision/recall para thresholds de 0.1 a 0.9
- [ ] Identificar threshold ótimo (máximo F1) vs threshold padrão 0.5
- [ ] Salvar curva de threshold no JSON para o dashboard permitir ajuste interativo

### 4. Feature Importance
- [ ] **Random Forest:** `feature_importances_` (Gini importance)
- [ ] **Logistic Regression:** coeficientes absolutos como proxy de importância
- [ ] **SHAP Values** (opcional, se `shap` disponível): explicação local por instância
- [ ] Produzir ranking das top-20 features com nome, importância e direção (positivo/negativo no delay)

### 5. Previsões no conjunto de teste (para o dashboard)
- [ ] Salvar sample de previsões (até 5.000 registros) com:
  - Features originais decodificadas (nomes legíveis, não encoded)
  - `y_true`, `y_pred`, `y_prob` (probabilidade de atraso)
  - `AIRLINE_NAME`, `ORIGIN_AIRPORT`, `DESTINATION_AIRPORT` (nomes de negócio)

### 6. Persistência dos modelos
- [ ] `models/logistic_regression.pkl`
- [ ] `models/random_forest.pkl`
- [ ] `models/gradient_boosting.pkl`

---

## JSONs Gerados (output para dashboard)

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

### Estrutura dos JSONs

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
    {"name": "airline_target_enc",  "importance": 0.14, "direction": "positive"}
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

## Dependências
```
scikit-learn>=1.3.0
joblib>=1.3.0
pyarrow>=14.0
shap>=0.44.0        # opcional — SHAP values
```

## Ordem de Execução
```bash
python src/02_feature_engineering.py        # Task 03 (pré-requisito)
python src/03_supervised_classification.py  # ← esta task
```

---

## Critérios de Sucesso

| Requisito (tc3.md) | Entregável | Status |
|---|---|---|
| ≥ 2 algoritmos supervisionados comparados | `ml_model_comparison.json` | ❌ |
| Métricas adequadas (F1, AUC-ROC, AUC-PR) | `ml_roc_curves.json`, `ml_pr_curves.json` | ❌ |
| Sem data leakage | Features pré-voo apenas | ❌ |
| Threshold optimization | `ml_threshold_analysis.json` | ❌ |
| Feature importance com interpretação | `ml_feature_importance.json` | ❌ |
| Outputs prontos para dashboard (Task 06) | Todos os JSONs em `dashboard/` | ❌ |

---

## Notas de DS
- **Leakage:** modelos treinados **apenas** no treino, validação para tuning, teste para avaliação final.
- **Escala:** amostra de 10% do dataset (~590k voos). Scripts devem rodar em < 10 min.
- **Reprodutibilidade:** todo `random_state=42`.
- **Dashboard contrato:** os JSONs são o contrato entre esta task e a Task 06 (dashboard). **Não alterar as chaves** após o dashboard começar.
