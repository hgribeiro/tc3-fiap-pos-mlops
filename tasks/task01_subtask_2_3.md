# Subtask 2.3 - Tratamento & Limpeza de Dados

**Fase:** 2 - EXPLORAÇÃO & VALIDAÇÃO  
**Status:** ❌ Não Iniciada  
**Data de Início:** --  
**Data de Conclusão:** --  
**Tempo Estimado:** 2.0h  

---

## 📋 Objetivo
Preparar e limpar os dados para análise segundo decisões documentadas: tratamento de missing, tipos de dados, duplicatas, outliers, e criação de variáveis derivadas.

---

## ✅ Checklist de Tarefas

- [ ] Tratar valores missing:
  - [ ] Decidir estratégia por coluna (imputação, remoção, manter)
  - [ ] Implementar imputação (forward fill, média, mediana)
  - [ ] Documentar justificativa de cada decisão
- [ ] Converter tipos de dados:
  - [ ] Datas (Year, Month, Day → datetime)
  - [ ] Categóricas apropriadas (carrier codes, airport codes)
- [ ] Remover/lidar com duplicatas
- [ ] Tratar outliers:
  - [ ] Decidir: remover ou transformar
  - [ ] Documentar critério
- [ ] Normalização/Scalização (se aplicável)
- [ ] Criar variáveis derivadas:
  - [ ] Atrasos categorizados (On-time, Short, Long delay)
  - [ ] Features temporais (mês, dia da semana, hora, estação)
  - [ ] Features de rota (se aplicável)
- [ ] Salvar dataset limpo
- [ ] Documentar todas as transformações

---

## 🎯 Critérios de Aceitação

- ✅ Decisões documentadas com justificativa
- ✅ Dataset limpo salvo em `data/processed/flights_cleaned.csv`
- ✅ Redução de missing <5% (ou justificada)
- ✅ Nenhuma transformação sem contexto de negócio
- ✅ Reproducibilidade garantida (mesmos resultados)
- ✅ Log de transformações criado

---

## 📝 Notas de Implementação

### 1. Tratamento de Missing Values

```python
# Estratégia por coluna (exemplo)
missing_strategy = {
    'ArrDelay': 'mean',      # Imputar com média
    'DepDelay': 'mean',      # Imputar com média
    'AirTime': 'mean',       # Imputar com média
    'TaxiIn': 'median',      # Imputar com mediana
    'TaxiOut': 'median',     # Imputar com mediana
    'ArrTime': 'drop',       # Remover linhas
    'DepTime': 'drop',       # Remover linhas
    'TailNum': 'drop',       # Remover se <1%
    'CancellationCode': 'drop'  # Remover se relacionado a Cancelled
}

# Implementar
for col, strategy in missing_strategy.items():
    if strategy == 'mean':
        df_flights[col].fillna(df_flights[col].mean(), inplace=True)
    elif strategy == 'median':
        df_flights[col].fillna(df_flights[col].median(), inplace=True)
    elif strategy == 'drop':
        df_flights.dropna(subset=[col], inplace=True)

# Validar
print(f"Total missing após tratamento: {df_flights.isna().sum().sum()}")
```

### 2. Converter Tipos de Dados

```python
# Criar datetime
df_flights['FlightDate'] = pd.to_datetime(
    df_flights[['Year', 'Month', 'DayofMonth']]
)

# Converter para category (economia de memória)
categorical_cols = ['UniqueCarrier', 'Origin', 'Dest', 'TailNum', 'CancellationCode']
for col in categorical_cols:
    df_flights[col] = df_flights[col].astype('category')

# Converter para int32/int16
df_flights['DepTime'] = df_flights['DepTime'].astype('int32')
df_flights['ArrTime'] = df_flights['ArrTime'].astype('int32')
```

### 3. Remover Duplicatas

```python
# Identificar duplicatas por chave primária
before = len(df_flights)
df_flights = df_flights.drop_duplicates(
    subset=['FlightDate', 'FlightNum', 'UniqueCarrier'],
    keep='first'
)
after = len(df_flights)
print(f"Duplicatas removidas: {before - after}")
```

### 4. Tratar Outliers (Exemplo: ArrDelay)

```python
# Opção A: Remover extremos
Q1 = df_flights['ArrDelay'].quantile(0.25)
Q3 = df_flights['ArrDelay'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 3 * IQR  # 3x para ser mais tolerante
upper_bound = Q3 + 3 * IQR

before = len(df_flights)
df_flights = df_flights[
    (df_flights['ArrDelay'] >= lower_bound) & 
    (df_flights['ArrDelay'] <= upper_bound)
]
after = len(df_flights)
print(f"Linhas com outliers removidas: {before - after}")

# Opção B: Transformar (se preferir manter dados)
# df_flights['ArrDelay_transformed'] = df_flights['ArrDelay'].apply(lambda x: np.log(x+1) if x >= 0 else -np.log(abs(x)+1))
```

### 5. Criar Variáveis Derivadas

```python
# Categorizar atrasos
def categorize_delay(minutes):
    if pd.isna(minutes):
        return 'Unknown'
    elif minutes <= 0:
        return 'On-time'
    elif minutes <= 15:
        return 'Short (1-15 min)'
    elif minutes <= 60:
        return 'Medium (16-60 min)'
    else:
        return 'Long (>60 min)'

df_flights['DelayCategory'] = df_flights['ArrDelay'].apply(categorize_delay)

# Features temporais
df_flights['Month'] = df_flights['FlightDate'].dt.month
df_flights['DayOfWeek'] = df_flights['FlightDate'].dt.dayofweek  # 0=Monday, 6=Sunday
df_flights['Hour'] = (df_flights['DepTime'] // 100).astype('int8')

# Estação
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

df_flights['Season'] = df_flights['Month'].apply(get_season)
df_flights['Season'] = df_flights['Season'].astype('category')

print(f"\nDelay distribution:")
print(df_flights['DelayCategory'].value_counts())
```

---

## 📊 Log de Transformações

Manter log estruturado:

```python
transformation_log = {
    'timestamp': datetime.now().isoformat(),
    'total_rows_before': 123456789,
    'total_rows_after': 123000000,
    'transformations': [
        {
            'step': 1,
            'name': 'Drop missing ArrTime',
            'rows_affected': 10000,
            'rows_removed': 50000
        },
        {
            'step': 2,
            'name': 'Remove ArrDelay outliers (Q1-3IQR < x < Q3+3IQR)',
            'rows_affected': 200000
        },
        {
            'step': 3,
            'name': 'Create DelayCategory',
            'type': 'derivation'
        }
    ],
    'memory_before_mb': 2000,
    'memory_after_mb': 1200
}

import json
with open('data/processed/transformation_log.json', 'w') as f:
    json.dump(transformation_log, f, indent=2)
```

---

## 🔄 Changelog

| Data | Versão | Mudança | Autor |
|------|--------|---------|-------|
| 2026-03-23 | v1.0 | Criação inicial da subtask | Copilot |
| -- | -- | -- | -- |

---

## 💾 Outputs Esperados

1. `data/processed/flights_cleaned.csv` - Dataset limpo
2. `data/processed/transformation_log.json` - Log de transformações
3. Relatório de antes/depois (shapes, memory, missing)
4. Estatísticas das novas variáveis derivadas

---

## 📋 Template de Documentação

```
## DATA CLEANING REPORT

### Rows Before/After
- Before: ___
- After: ___
- Removed: ___ (___%)

### Missing Values Treatment
Column | Strategy | Rows Affected | Status
-------|----------|---------------|---------
ArrDelay | Mean imputation | ___ | ✅
DepDelay | Mean imputation | ___ | ✅
[...]

### Outliers Removed
- ArrDelay: ___ rows (Q1-3IQR to Q3+3IQR)
- DepDelay: ___ rows
- Distance: ___ rows

### New Variables Created
✅ DelayCategory (4 classes: On-time, Short, Medium, Long)
✅ Month (extracted from date)
✅ DayOfWeek (0-6)
✅ Hour (0-23)
✅ Season (Winter/Spring/Summer/Fall)

### Memory Usage
- Before: ___ MB
- After: ___ MB
- Reduction: ___% ✅
```

---

## ⚠️ Possíveis Bloqueadores

- [ ] Imputação cria viés nos dados
- [ ] Remoção de outliers remove muitos dados legítimos
- [ ] Variáveis derivadas não fazem sentido no contexto
- [ ] Memory ainda não suficiente após otimizações
- [ ] Reprodutibilidade comprometida (random seed)

Quando encontrar bloqueadores, documentar abaixo:
```
[BLOQUEADOR] - Descrição do problema
Impacto: ...
Alternativa testada: ...
```

