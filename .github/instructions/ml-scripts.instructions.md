---
name: ml-scripts
description: "Use quando alterar scripts de ML em src para preservar guardrails de leakage, seeds de reprodutibilidade e contratos de JSON consumidos por dashboard/relatório."
applyTo: "src/*.py"
---

# ML Scripts (TC3)

## Escopo

- Aplicar a scripts em `src/` que fazem EDA, feature engineering, treino/avaliação e geração de artefatos para dashboard/relatório.
- Manter mudanças mínimas e compatíveis com o pipeline sequencial (`01_eda.py` → `02_feature_engineering.py` → `03_supervised_classification.py` → `04_unsupervised.py` → `05_model_report.py` → `prepare_dashboard_data.py`).
- Não alterar paths de artefatos sem atualizar todos os consumidores no próprio `src/`.

## Guardrails de leakage

- Preservar a definição de alvo de classificação: `IS_DELAYED = ARRIVAL_DELAY > 15`.
- Não usar como feature preditora colunas que só existem pós-voo ou revelam atraso real (ex.: `ARRIVAL_DELAY`, `DEPARTURE_DELAY`, tempos reais, flags derivadas diretamente do atraso observado).
- Garantir split estratificado 70/15/15 (train/val/test) com separação clara entre ajuste e avaliação.
- Fazer fit de encoders/scaler **apenas** no treino; em validação/teste, aplicar transformação sem refit.
- Evitar criar features a partir de estatísticas globais calculadas com dados de validação/teste.

## Seeds e reprodutibilidade

- Manter `random_state=42` e seeds existentes, salvo solicitação explícita.
- Em operações estocásticas (split, amostragem, modelos com aleatoriedade), explicitar seed para reprodutibilidade.
- Evitar alterações que mudem resultados por efeito colateral (ordenação implícita, sampling sem seed, cast não determinístico).

## Contratos de JSON

- Preservar nomes de arquivos e estrutura de alto nível dos JSONs em `data/processed/dashboard/`.
- Em JSONs já consumidos, não renomear/remover chaves sem atualizar todos os consumidores (`dashboard/app.js` e `src/05_model_report.py`).
- Manter saída serializável em tipos nativos Python (`int`, `float`, `list`, `dict`) e evitar tipos NumPy/Pandas crus no `json.dump`.
- Preferir arredondamento/cast explícito para métricas e séries (como já feito no projeto) para estabilidade entre execuções.
- Arquivos esperados no fluxo atual incluem:
  - Supervisionado: `ml_model_comparison.json`, `ml_roc_curves.json`, `ml_pr_curves.json`, `ml_confusion_matrices.json`, `ml_feature_importance.json`, `ml_threshold_analysis.json`, `ml_test_predictions.json`.
  - Não supervisionado: `ml_pca_variance.json`, `ml_kmeans_elbow.json`, `ml_cluster_profiles.json`, `ml_pca_scatter.json`, `ml_cluster_routes.json`.
  - Dashboard agregado: `dashboard_kpis.json`, `dashboard_delay_distribution.json`, `dashboard_temporal.json`, `dashboard_airlines.json`, `dashboard_airports.json`, `dashboard_correlation.json`, `dashboard_cancellations.json`.

## Qualidade e validação mínima

- Ao alterar contratos/geração, executar ao menos os scripts impactados em ordem para validar dependências de artefatos.
- Se houver mudança em JSON, validar que o dashboard continua carregando sem quebra e que `src/05_model_report.py` consegue consolidar métricas.
- Priorizar robustez de memória para `flights.csv` (dtypes enxutos, sampling/chunking quando necessário).
