# Task 01: Análise Exploratória de Dados (EDA) - Datasets de Voos

## Objetivo
Realizar análise exploratória completa dos datasets de voos (airlines, airports e flights), com foco especial no arquivo `flights.csv` (~500MB), para entender a estrutura, qualidade dos dados e identificar padrões relevantes.

## Contexto
- **Datasets disponíveis:**
  - `data/airlines.csv` (~359 bytes)
  - `data/airports.csv` (~24KB)
  - `data/flights.csv` (~592MB) ⚠️ **ARQUIVO GRANDE**
  
- **Referência:** Baseado na estrutura de análise em `src/EDA.py`

## Tarefas a Executar

### 1. Carregamento e Exploração Inicial
- [ ] Carregar os três datasets (airlines, airports, flights)
- [ ] Para o arquivo flights.csv, considerar:
  - Carregamento por chunks (chunking) se necessário
  - Uso de dtypes otimizados para reduzir uso de memória
  - Amostragem estratégica se o dataset completo for muito grande
- [ ] Exibir primeiras linhas de cada dataset (`.head()`)
- [ ] Verificar dimensões (`.shape`)
- [ ] Listar tipos de dados de cada coluna (`.dtypes`)
- [ ] Identificar colunas e seus significados

### 2. Análise de Qualidade dos Dados
- [ ] Verificar valores nulos/missing (`.isna().sum()`)
- [ ] Identificar valores duplicados
- [ ] Verificar consistência entre datasets (chaves estrangeiras)
- [ ] Identificar outliers em variáveis numéricas
- [ ] Analisar distribuição de valores categóricos (`.value_counts()`)

### 3. Estatísticas Descritivas
- [ ] Gerar estatísticas descritivas completas (`.describe()`)
- [ ] Para variáveis numéricas principais:
  - Média, mediana, moda
  - Variância e desvio padrão
  - Quartis (Q1, Q2, Q3)
  - Valores mínimos e máximos
- [ ] Para variáveis categóricas:
  - Frequências absolutas e relativas
  - Número de categorias únicas

### 4. Limpeza e Transformação de Dados
- [ ] Renomear colunas para nomes mais descritivos (se necessário)
- [ ] Converter tipos de dados inadequados (ex: datas, numéricos)
- [ ] Tratar valores missing:
  - Identificar padrão de missing
  - Decidir estratégia (imputação, remoção, manter)
- [ ] Remover duplicatas (se aplicável)
- [ ] Remover/filtrar outliers extremos (documentar critério)
- [ ] Criar variáveis derivadas úteis (ex: atrasos, duração de voo)

### 5. Visualizações Exploratórias

#### 5.1 Distribuições Univariadas
- [ ] Histogramas para variáveis numéricas principais
- [ ] Gráficos de barras para variáveis categóricas (top N valores)
- [ ] Boxplots para identificar outliers

#### 5.2 Análises Bivariadas
- [ ] Scatter plots entre variáveis numéricas relevantes
- [ ] Gráficos de barras agrupados (categórica vs numérica)
- [ ] Countplots com hue para relações categóricas

#### 5.3 Análises por Grupos
- [ ] Agregações por grupos relevantes (`.groupby()`)
  - Por companhia aérea
  - Por aeroporto origem/destino
  - Por período temporal (mês, dia da semana)
- [ ] Comparações de médias entre grupos
- [ ] Visualizações de séries temporais (se houver datas)

### 6. Insights e Padrões
- [ ] Documentar padrões identificados
- [ ] Listar anomalias ou comportamentos inesperados
- [ ] Identificar correlações interessantes
- [ ] Sugerir features para modelagem posterior

### 7. Documentação da Análise
- [ ] Criar relatório consolidado com:
  - Resumo executivo dos principais achados
  - Estatísticas-chave de cada dataset
  - Principais visualizações
  - Problemas de qualidade identificados
  - Recomendações para próximas etapas
- [ ] Salvar dataset limpo/tratado (se aplicável)
- [ ] Documentar decisões de tratamento de dados

## Bibliotecas Recomendadas
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

## Considerações Especiais

### Performance com Arquivo Grande (flights.csv)
```python
# Exemplo de leitura otimizada
# Opção 1: Especificar dtypes
dtypes = {
    'col1': 'int32',  # ao invés de int64
    'col2': 'category',  # para categóricas
}
df = pd.read_csv('data/flights.csv', dtype=dtypes)

# Opção 2: Leitura por chunks
chunk_size = 100000
for chunk in pd.read_csv('data/flights.csv', chunksize=chunk_size):
    # Processar cada chunk
    pass

# Opção 3: Amostragem
df_sample = pd.read_csv('data/flights.csv', 
                        skiprows=lambda i: i>0 and np.random.random() > 0.1)
```

## Outputs Esperados
1. Notebook/script Python com análise completa e bem documentada
2. Visualizações salvas em `docs/eda_plots/`
3. Relatório markdown com principais insights em `docs/eda_report.md`
4. Dataset limpo/tratado (opcional) em `data/processed/`

## Critérios de Sucesso
- ✅ Todos os datasets carregados e explorados
- ✅ Qualidade dos dados avaliada e documentada
- ✅ Mínimo de 10 visualizações significativas geradas
- ✅ Insights claros e acionáveis documentados
- ✅ Código executável e reproduzível
- ✅ Performance adequada mesmo com arquivo grande

## Notas
- Priorize entender os dados antes de transformá-los
- Documente todas as suposições e decisões
- Foque em insights que guiarão a modelagem futura
- Considere o contexto de negócio de análise de voos
