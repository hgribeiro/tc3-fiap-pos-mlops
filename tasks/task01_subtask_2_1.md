# Subtask 2.1 - Análise Descritiva Completa

**Fase:** 2 - EXPLORAÇÃO & VALIDAÇÃO  
**Status:** ❌ Não Iniciada  
**Data de Início:** --  
**Data de Conclusão:** --  
**Tempo Estimado:** 1.5h  

---

## 📋 Objetivo
Gerar estatísticas básicas de todos os datasets para entender distribuições, ranges e características principales das variáveis.

---

## ✅ Checklist de Tarefas

- [ ] Executar `.describe()` para variáveis numéricas de cada dataset
- [ ] Executar `.info()` para visão geral (dtypes, memory, non-null)
- [ ] Executar `.value_counts()` para variáveis categóricas principais
- [ ] Calcular média, mediana, moda para variáveis numéricas
- [ ] Calcular std, quartis (Q1, Q2, Q3) para variáveis numéricas
- [ ] Identificar range (min/max) de cada variável
- [ ] Documentar significado de cada coluna principal
- [ ] Criar resumo consolidado das estatísticas

---

## 🎯 Critérios de Aceitação

- ✅ Estatísticas completas para >90% das colunas
- ✅ Interpretação clara de cada métrica documentada
- ✅ Valores fazem sentido no contexto de voos
- ✅ Tabelas bem formatadas (readáveis)
- ✅ Resultados salvos em arquivo (CSV ou JSON)

---

## 📝 Notas de Implementação

### Estatísticas por Dataset

#### Airlines
```python
print("AIRLINES DATASET:")
print(df_airlines.shape)
print(df_airlines.info())
print(df_airlines.describe(include='all'))
print(df_airlines.head(10))
```

#### Airports
```python
print("AIRPORTS DATASET:")
print(df_airports.shape)
print(df_airports.info())
print(df_airports.describe(include='all'))
print(df_airports[['AirportID', 'AirportName', 'City', 'Country']].head(10))
```

#### Flights (principais colunas)
```python
print("FLIGHTS DATASET:")
print(df_flights.shape)
print(df_flights.info())
print(df_flights[['ArrDelay', 'DepDelay', 'Distance', 'AirTime']].describe())

# Value counts para categóricas
print("\nTop 10 Airlines:")
print(df_flights['UniqueCarrier'].value_counts().head(10))

print("\nTop 10 Origin Airports:")
print(df_flights['Origin'].value_counts().head(10))

print("\nTop 10 Destination Airports:")
print(df_flights['Dest'].value_counts().head(10))

print("\nMonths Distribution:")
print(df_flights['Month'].value_counts().sort_index())
```

### Métricas Recomendadas por Coluna

| Coluna | Tipo | Métricas |
|--------|------|---------|
| ArrDelay | numérica | mean, median, std, min, max, Q1, Q3 |
| DepDelay | numérica | mean, median, std, min, max, Q1, Q3 |
| Distance | numérica | mean, median, std, min, max |
| UniqueCarrier | categórica | value_counts, nunique |
| Origin/Dest | categórica | value_counts, nunique |
| Month/DayOfWeek | categórica | value_counts.sort_index() |
| Cancelled | numérica | sum, %, nunique values |

---

## 🔄 Changelog

| Data | Versão | Mudança | Autor |
|------|--------|---------|-------|
| 2026-03-23 | v1.0 | Criação inicial da subtask | Copilot |
| -- | -- | -- | -- |

---

## 💾 Outputs Esperados

1. Estatísticas descritivas em formato tabular
2. Resumo JSON: `data/processed/eda_summary.json`
3. CSV com estatísticas principais
4. Screenshots das primeiras análises

---

## 📊 Template de Documentação

Ao completar, preencher:

```
## DATASETS OVERVIEW

### Airlines
- Shape: ___
- Colunas: ___
- Memória: ___

### Airports
- Shape: ___
- Colunas: ___
- Memória: ___

### Flights
- Shape: ___
- Colunas: ___
- Memória: ___

## VARIÁVEIS NUMÉRICAS CHAVE

### ArrDelay (Arrival Delay em minutos)
- Mean: ___ min
- Median: ___ min
- Std: ___ min
- Min: ___ min
- Max: ___ min
- Q1/Q3: ___ / ___

### DepDelay (Departure Delay)
- Mean: ___ min
- Median: ___ min
- [other stats]

### Distance
- Mean: ___ miles
- Min: ___ miles
- Max: ___ miles

## VARIÁVEIS CATEGÓRICAS CHAVE

### Top 5 Airlines (por volume)
1. ___ (counts: ___)
2. ___
3. ___
4. ___
5. ___

### Top 5 Origin Airports
1. ___ (counts: ___)
2. ___
3. ___
4. ___
5. ___

### Distribuição Temporal
- Months: Uniform? Seasonal?
- Days of Week: Padrão?
```

---

## ⚠️ Possíveis Bloqueadores

- [ ] Dataset muito grande para .describe() em memória
- [ ] Colunas com tipos de dados incorretos
- [ ] Valores missing difíceis de interpretar
- [ ] Outliers extremos distortem estatísticas

Quando encontrar bloqueadores, documentar abaixo:
```
[BLOQUEADOR] - Descrição do problema
Solução: ...
```

