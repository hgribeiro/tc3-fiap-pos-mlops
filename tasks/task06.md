# Task 06: Relatório Crítico dos Modelos

## Objetivo
Gerar programaticamente um relatório consolidado (`docs/model_report.md`) que documenta todas as decisões, métricas, interpretações e limitações dos modelos treinados nas Tasks 04 e 05.

## Contexto
- **Input:** todos os JSONs em `data/processed/dashboard/` gerados pelas Tasks 04 e 05
- **Output:** `docs/model_report.md`
- **Arquivo:** `src/05_model_report.py`

---

## Etapas

### 1. Carregar JSONs
- [ ] Carregar todos os JSONs supervisionados (`ml_model_comparison.json`, `ml_roc_curves.json`, `ml_pr_curves.json`, `ml_confusion_matrices.json`, `ml_feature_importance.json`, `ml_threshold_analysis.json`)
- [ ] Carregar todos os JSONs não supervisionados (`ml_pca_variance.json`, `ml_kmeans_elbow.json`, `ml_cluster_profiles.json`)

### 2. Gerar `docs/model_report.md` com as seguintes seções
- [ ] **Tabela comparativa de métricas** dos 3 modelos supervisionados
- [ ] **Decisões tomadas e justificativas:**
  - Prevenção de data leakage
  - Tratamento de desbalanceamento
  - Threshold optimization
  - Escolha do melhor modelo
- [ ] **Interpretação de cada cluster** (não supervisionado)
  - Rótulo, perfil estatístico, significado de negócio
- [ ] **Respostas às perguntas norteadoras do tc3.md:**
  - Quais aeroportos são mais críticos em relação a atrasos?
  - Que características aumentam a chance de atraso?
  - Atrasos são mais comuns em certos dias ou horários?
  - É possível agrupar aeroportos com perfis semelhantes?
  - Até que ponto conseguimos prever atrasos com base no histórico?
- [ ] **Limitações e próximos passos**

---

## Dependências
```
# Nenhuma dependência adicional — apenas leitura de JSONs e escrita de markdown
```

## Ordem de Execução
```bash
python src/03_supervised_classification.py  # Task 04 (pré-requisito)
python src/04_unsupervised.py               # Task 05 (pré-requisito)
python src/05_model_report.py               # ← esta task
```

---

## Critérios de Sucesso

| Requisito (tc3.md) | Entregável | Status |
|---|---|---|
| Apresentação crítica dos resultados | `docs/model_report.md` | ❌ |
| Principais conclusões documentadas | Seção de conclusões | ❌ |
| Limitações dos modelos | Seção de limitações | ❌ |
| Propostas de melhorias e próximos passos | Seção de próximos passos | ❌ |
| Respostas às perguntas norteadoras | Seção dedicada | ❌ |
