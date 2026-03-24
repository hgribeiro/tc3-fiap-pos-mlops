# Copilot Instructions - Flight Delay Prediction (TC3)

## Scope

Projeto do Tech Challenge 3 (FIAP MLOps) para análise e predição de atrasos de voos nos EUA.
Priorize mudanças mínimas, reprodutíveis e alinhadas com os scripts existentes em `src/`.

## Quick Start (Ordem Obrigatória)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 1) EDA + amostragem + artefatos iniciais
python src/01_eda.py

# 2) Feature engineering + split + encoders/scaler
python src/02_feature_engineering.py

# 3) Modelos supervisionados + métricas JSON
python src/03_supervised_classification.py

# 4) Não supervisionado (PCA/K-Means)
python src/04_unsupervised.py

# 5) Relatório consolidado
python src/05_model_report.py

# 6) Dados finais do dashboard
python src/prepare_dashboard_data.py

# 7) Dashboard estático
npx -y serve . -l 3847
```

Dashboard: `http://localhost:3847/dashboard/`

Opcional (captura de telas):

```bash
node scripts/capture_dashboard_screenshots.mjs
```

## Pipeline e Fronteiras de Componentes

- `data/flights.csv` (~592MB) é a base principal.
- `src/01_eda.py` gera `data/processed/flights_sample_processed.csv`, `data/processed/eda_summary.json` e gráficos em `docs/eda_plots/`.
- `src/02_feature_engineering.py` gera `X_*.parquet`, `y_*.parquet`, `models/encoders.json`, `models/scaler.pkl`.
- `src/03_supervised_classification.py` e `src/04_unsupervised.py` geram JSONs em `data/processed/dashboard/`.
- `src/05_model_report.py` consolida métricas em `docs/model_report.md`.
- `src/prepare_dashboard_data.py` gera/atualiza JSONs `dashboard_*.json` consumidos por `dashboard/app.js`.

Se pular etapas, os scripts seguintes quebram por dependência de arquivos.

## Convenções do Repositório

- Idioma predominante: português (docstrings, mensagens e documentação), com nomes técnicos em inglês.
- Reprodutibilidade: manter `random_state=42` e seeds existentes, salvo solicitação explícita.
- Otimização de memória é mandatória para `flights.csv`: `dtype` enxuto, sampling/chunking quando necessário.
- Evitar data leakage: não usar colunas de atraso real como features preditoras pré-voo.
- Manter caminhos relativos via `pathlib.Path` e criar diretórios com `mkdir(..., exist_ok=True)` quando preciso.
- Para dashboard, preferir saída em JSON já arredondada/cast para tipos nativos Python.

## Regras de Modelagem

- Definição alvo de classificação: `IS_DELAYED = ARRIVAL_DELAY > 15` minutos.
- Split estratificado esperado: 70/15/15 (treino/val/teste).
- Fit de encoders/scaler no treino; aplicar em val/teste sem refit.
- Preservar guardrails de leakage já implementados nos scripts.

## Pitfalls Comuns

- Memória: operações no dataset completo podem estourar RAM; começar por amostra.
- Ordem de execução: outputs ausentes são a causa mais comum de erro.
- Dashboard depende dos JSONs em `data/processed/dashboard/`; verifique geração antes de depurar front.
- `serve` na porta `3847` pode conflitar; troque a porta se necessário.

## Estrutura de Referência (Link, não duplicar)

- Visão geral e execução: `README.md`
- Objetivos oficiais do desafio: `docs/tc3.md`
- Relatório consolidado: `docs/model_report.md`
- Especificações detalhadas por task: `tasks/`
- Contexto do agente DS: `.agent.md`

## O que evitar ao contribuir

- Não alterar escopo de UX do dashboard além do solicitado.
- Não introduzir dependências novas sem necessidade clara.
- Não refatorar scripts inteiros quando a demanda for localizada.
- Não quebrar contratos de artefato (`data/processed/dashboard/*.json`, `models/*.json|*.pkl`).
