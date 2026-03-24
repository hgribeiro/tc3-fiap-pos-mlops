# Task 01: Subtasks para Validação de Completude

## Overview
Estrutura de 9 subtasks organizadas em 4 fases, cobrindo todo o ciclo de vida da análise exploratória.

---

## FASE 1: SETUP & CARREGAMENTO
### Subtask 1.1 - Preparação do Ambiente
**Objetivo:** Garantir que o ambiente e ferramentas estão prontos
- [ ] Verificar ambiente Python ativado
- [ ] Validar bibliotecas instaladas (pandas, numpy, matplotlib, seaborn, plotly)
- [ ] Criar estrutura de diretórios (`docs/eda_plots/`, `data/processed/`)
- [ ] Definir random seed para reprodutibilidade
- [ ] Validar caminho dos dados

**Critérios de Aceitação:**
- ✅ Todos imports funcionam sem erro
- ✅ Diretórios de output existem
- ✅ Todos os 3 arquivos de dados acessíveis

---

### Subtask 1.2 - Carregamento Otimizado dos Dados
**Objetivo:** Carregar datasets com estratégia apropriada para tamanhos diferentes
- [ ] Carregar `airlines.csv` integralmente
- [ ] Carregar `airports.csv` integralmente
- [ ] Carregar `flights.csv` com otimização:
  - Implementar leitura com dtypes otimizados (int32, category)
  - OU leitura por chunks
  - OU amostragem (documentar % amostrado)
- [ ] Validar dimensões (shape) de cada dataset
- [ ] Listar colunas e tipos de dados
- [ ] Exibir .head() de cada dataset

**Critérios de Aceitação:**
- ✅ 3 DataFrames carregados sem erro memory
- ✅ Dimensões documentadas
- ✅ Estratégia de otimização escolhida e justificada
- ✅ Memory usage dentro de limite razoável

---

## FASE 2: EXPLORAÇÃO & VALIDAÇÃO DE QUALIDADE
### Subtask 2.1 - Análise Descritiva Completa
**Objetivo:** Gerar estatísticas básicas de todos os datasets
- [ ] `.describe()` para variáveis numéricas
- [ ] `.info()` para visão geral
- [ ] `.value_counts()` para variáveis categóricas
- [ ] Cálculo de média, mediana, moda, std, quartis
- [ ] Identificação de range (min/max)
- [ ] Documentar significado de cada coluna principal

**Critérios de Aceitação:**
- ✅ Estatísticas completas para >90% das colunas
- ✅ Interpretação clara de cada métrica
- ✅ Valores fazem sentido no contexto de voos

---

### Subtask 2.2 - Validação de Qualidade dos Dados
**Objetivo:** Identificar problemas de dados (missing, duplicatas, inconsistências)
- [ ] Análise de valores nulos/missing (%.isna())
- [ ] Identificação de duplicatas
- [ ] Validação de foreign keys:
  - Airlines (FlightNum → AirlineID)
  - Airports (Origin → AirportID, Dest → AirportID)
- [ ] Detecção de outliers (IQR ou Z-score)
- [ ] Validação de ranges (datas, distâncias, atrasos)
- [ ] Identificação de valores incomuns ou impossíveis

**Critérios de Aceitação:**
- ✅ % de missing documentado por coluna
- ✅ Integridade referencial validada (>95%)
- ✅ Outliers identificados e justificados
- ✅ Problemas críticos documentados

---

### Subtask 2.3 - Tratamento & Limpeza de Dados
**Objetivo:** Preparar dados para análise (tratamento de issues encontradas)
- [ ] Decisão sobre valores missing:
  - Imputação (método: forward fill, média, mediana)
  - Remoção de linhas
  - Manter como é (justificar)
- [ ] Conversão de tipos de dados (datas, categóricas)
- [ ] Remoção de duplicatas (se validadas)
- [ ] Tratamento de outliers (remover ou transformar)
- [ ] Normalização/Scalização (se aplicável)
- [ ] Criação de variáveis derivadas:
  - Atrasos (de minutos para categorias: no delay, short, long)
  - Features temporais (mês, dia da semana, hora)
  - Distância ou rota

**Critérios de Aceitação:**
- ✅ Decisões documentadas com justificativa
- ✅ Dataset limpo salvo em `data/processed/`
- ✅ Redução de missing <5% (ou justificada)
- ✅ Nenhuma transformação sem contexto de negócio

---

## FASE 3: VISUALIZAÇÕES & INSIGHTS
### Subtask 3.1 - Visualizações Univariadas
**Objetivo:** Entender distribuições individuais de variáveis principais
- [ ] Mínimo 3 histogramas (variáveis numéricas principais)
- [ ] Mínimo 3 gráficos de barras (categóricas relevantes)
- [ ] Mínimo 2 boxplots (para outliers)
- [ ] Pelo menos 1 distribuição por tipo de dados
- [ ] Escalas e labels apropriados
- [ ] Cores e estilo consistentes

**Critérios de Aceitação:**
- ✅ Mínimo 8-10 visualizações univariadas
- ✅ Todas salvas em `docs/eda_plots/`
- ✅ Insights interpretados (qual é a distribuição?)
- ✅ Qualidade visual profissional

---

### Subtask 3.2 - Visualizações Bivariadas & Correlações
**Objetivo:** Explorar relações entre variáveis
- [ ] Matriz de correlação (heatmap) para numéricas
- [ ] Scatter plots para relações numéricas principais
- [ ] Gráficos categóricos × numéricos (boxplot, violinplot)
- [ ] Análise de relações por grupo:
  - Atrasos por companhia aérea
  - Atrasos por aeroporto
  - Padrões por dia da semana/mês
- [ ] Análises de séries temporais (se data disponível)

**Critérios de Aceitação:**
- ✅ Mínimo 8-10 visualizações bivariadas
- ✅ Correlações numéricas analisadas (>0.3 documentadas)
- ✅ Gráficos de agregação por grupo
- ✅ Descobertas não óbvias documentadas

---

### Subtask 3.3 - Análise de Padrões & Insights
**Objetivo:** Extrair conhecimento acionável dos dados
- [ ] Identificar top N companhias (por volume, atrasos)
- [ ] Identificar top N aeroportos (por volume, atrasos)
- [ ] Padrões temporais:
  - Horários com mais atrasos
  - Dias da semana mais críticos
  - Sazonalidade (por mês/estação)
- [ ] Relações entre variáveis: quais features correlacionam com atrasos?
- [ ] Anomalias ou comportamentos inesperados
- [ ] Recomendações para modelagem futura

**Critérios de Aceitação:**
- ✅ Mínimo 5-7 insights claros e documentados
- ✅ Insights suportados por dados/visualizações
- ✅ Relevância para negócio (contexto de voos)
- ✅ Sugestões de features para próximas etapas

---

## FASE 4: VALIDAÇÃO & DOCUMENTAÇÃO
### Subtask 4.1 - Validação & Testes
**Objetivo:** Garantir correção e reprodutibilidade da análise
- [ ] Executar código fim-a-fim (sem erros)
- [ ] Validar reprodutibilidade (random seed, resultados consistentes)
- [ ] Verificar se all visualizações foram geradas
- [ ] Validar se dados processados estão salvos
- [ ] Verificar integridade de caminhos de arquivos
- [ ] Testar performance (tempo de execução aceitável)
- [ ] Revisar código para best practices (comentários, nomes claros)

**Critérios de Aceitação:**
- ✅ Código executa sem erros
- ✅ Resultados reproduzíveis
- ✅ Tempo de execução <5 minutos (ou documentado se maior)
- ✅ Código limpo e bem comentado
- ✅ Todos os outputs no lugar correto

---

### Subtask 4.2 - Relatório Final & Documentação
**Objetivo:** Consolidar análise em relatório formal
- [ ] Criar `docs/eda_report.md` com:
  - Resumo executivo (2-3 parágrafos principais)
  - Descrição dos datasets (origem, tamanho, colunas)
  - Metodologia (estratégias de limpeza adotadas)
  - Seção de Principais Descobertas (com visualizações)
  - Problemas de Qualidade Identificados
  - Variáveis Chave Para Modelagem
  - Limitações & Próximos Passos
- [ ] Documentar decisões chave em comentários
- [ ] Criar sumário JSON com `eda_summary.json`:
  - Estatísticas-chave
  - Contagem de missing
  - Top valores categóricos
  - Correlações principais
- [ ] Salvaguardar reproducibility:
  - README com instruções de execução
  - Documentar versões de bibliotecas

**Critérios de Aceitação:**
- ✅ Relatório markdown completo (>2000 palavras)
- ✅ Mínimo 5-8 visualizações referenciadas no relatório
- ✅ JSON summary criado
- ✅ Conclusões claramente comunicadas
- ✅ Recomendações para próximas tarefas

---

## Sumário de Checklist por Fase

| Fase | Subtask | Saídas |
|------|---------|--------|
| **1. Setup** | 1.1 + 1.2 | Ambiente pronto, dados carregados |
| **2. Exploração** | 2.1 + 2.2 + 2.3 | Dados validados, limpos, documentados |
| **3. Visualizações** | 3.1 + 3.2 + 3.3 | 15-20 gráficos, 5-7 insights |
| **4. Validação** | 4.1 + 4.2 | Código testado, relatório final |

---

## Critérios Globais de Completude

Para considerar **Task 01 COMPLETA**, validar:

- ✅ **Implementação:** Todas 8 subtasks técnicas finalizadas
- ✅ **Qualidade:** Código limpo, reproduzível, bem documentado
- ✅ **Análise:** Mínimo 10 visualizações significativas
- ✅ **Insights:** 5-7 descobertas documentadas e acionáveis
- ✅ **Documentação:** Relatório formal + dados processados salvos
- ✅ **Performance:** Execução sem erros, tempo aceitável
- ✅ **Contexto:** Insights fazem sentido no domínio de voos

---

## Estimativa de Tempo

| Subtask | Tempo (horas) |
|---------|---------------|
| 1.1 - Preparação | 0.5 |
| 1.2 - Carregamento | 1.0 |
| 2.1 - Análise Descritiva | 1.5 |
| 2.2 - Validação Qualidade | 2.0 |
| 2.3 - Limpeza & Tratamento | 2.0 |
| 3.1 - Viz Univariadas | 1.5 |
| 3.2 - Viz Bivariadas | 2.0 |
| 3.3 - Análise de Padrões | 2.0 |
| 4.1 - Testes & Validação | 1.0 |
| 4.2 - Relatório Final | 2.0 |
| **TOTAL** | **~15-16h** |

---

## Notas Importantes

1. **Ordem de Execução:** Seguir sequência 1.1 → 1.2 → 2.1 → 2.2 → 2.3 → 3.1 → 3.2 → 3.3 → 4.1 → 4.2
2. **Interdependências:** Subtasks posteriores dependem de anteriores
3. **Flexibilidade:** Se dataset muito grande, ajustar 1.2 (amostragem/chunks)
4. **Documentação:** Cada subtask deve ter outputs claros e salvos
5. **Review:** Ao final, validar TODOS os critérios de aceitação antes de marcar completo

