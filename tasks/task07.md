# Task 07: Adicionar Aba de Machine Learning ao Dashboard

## Objetivo
Gerar um plano e implementar uma nova aba "Machine Learning" no dashboard existente. O objetivo é visualizar interativamente os resultados das tarefas de aprendizado de máquina (Supervisionado e Não Supervisionado) gerados nas Tasks 04 e 05.

## Contexto
- **Input:** JSONs gerados em `data/processed/dashboard/` contendo métricas e dados dos modelos (ex: `ml_model_comparison.json`, `ml_feature_importance.json`, `ml_pca_variance.json`, `ml_kmeans_elbow.json`, etc.)
- **Output:** Alterações em `dashboard/index.html`, `dashboard/app.js` e `dashboard/style.css`
- **Ferramentas:** HTML, CSS, JavaScript (Chart.js / bibliotecas de gráficos pré-existentes no dashboard)

---

## Etapas de Implementação

### 1. Atualizar a Estrutura do Dashboard (`dashboard/index.html`)
- [ ] Adicionar botão/link de navegação para a nova aba "Machine Learning".
- [ ] Criar a estrutura HTML base (divs/sections) para a nova aba.
- [ ] Dividir a aba em duas sub-seções visuais:
  - **Aprendizado Supervisionado** (Classificação de Atrasos)
  - **Aprendizado Não Supervisionado** (Agrupamento de Rotas)
- [ ] Inserir os elementos `<canvas>` para renderização dos gráficos de cada métrica.

### 2. Estilizar a Nova Aba (`dashboard/style.css`)
- [ ] Garantir que o layout siga o design (grids, cartões) do dashboard original.
- [ ] Criar classes de layout para exibir múltiplos gráficos lado a lado (ex: matriz de confusão vs importância de features).

### 3. Integração de Dados e Lógica de Gráficos (`dashboard/app.js`)
- [ ] **Carregamento Assíncrono:** Criar funções para buscar os JSONs específicos de MA (`fetch('./data/processed/dashboard/ml_*.json')`).
- [ ] **Aprendizado Supervisionado (Gráficos):**
  - **Comparação de Modelos:** Gráfico de barras (Accuracy, Precision, Recall, F1, ROC-AUC) entre os 3 modelos.
  - **Importância de Features:** Gráfico de barras horizontais mostrando as variáveis mais impactantes (do Random Forest, por ex).
  - **Matriz de Confusão:** Representação em grid ou tabela colorida (Heatmap simplificado).
  - **Curvas ROC / PR:** Gráficos de linha traçando as taxas verdadeiras e falsas.
- [ ] **Aprendizado Não Supervisionado (Gráficos):**
  - **Método do Cotovelo (K-Means):** Gráfico de linha mostrando a inércia por número de clusters.
  - **Variância do PCA:** Gráfico de barras (variância explicada) e linha (acumulada).
  - **Perfil dos Clusters:** Gráfico de radar (Radar Chart) ou barras empilhadas informando o comportamento estatístico de cada grupo.
  - **Distribuição (PCA Scatter):** Gráfico de dispersão (Scatter Plot) das rotas em 2D. (Atenção ao carregamento de `cluster_id` para mapear as cores corretamente).

### 4. Validação e Testes Locais
- [ ] Subir o servidor de teste (ex: `npx serve .`) e abrir o dashboard.
- [ ] Validar a navegação para a aba de Machine Learning.
- [ ] Assegurar que os gráficos são renderizados adequadamente (Chart.js) e exibem *tooltips* com os dados corretos.
- [ ] **Validação PCA (Bug Fix):** Verificar que a plotagem de Distribuição de Rotas mostra todos os clusters na cor certa (front-end deve ler `data.cluster_id`).
- [ ] Verificar a responsividade e o layout das visualizações nos diferentes tamanhos de tela.

---

## Dependências
- Execução prévia da **Task 04** e **Task 05** para geração dos `.json` necessários no diretório `/data/processed/dashboard/`.
- Dependência do frontend (e.g. `Chart.js` já integrado no `index.html`) e estrutura do dashboard original.

## Critérios de Sucesso

| Requisito | Entregável | Status |
|---|---|---|
| Aba "Machine Learning" presente | `dashboard/index.html` e `dashboard/style.css` modificados | ❌ |
| Gráficos Supervisionados implementados | `dashboard/app.js` renderizando (Comparação, Feature Imp., Matriz) | ❌ |
| Gráficos Não Supervisionados implementados | `dashboard/app.js` renderizando (Elbow, PCA Variância, Perfis) | ❌ |
| Integração perfeita dos JSONs | Dados reais mapeados e plotados sem erros de console | ❌ |
