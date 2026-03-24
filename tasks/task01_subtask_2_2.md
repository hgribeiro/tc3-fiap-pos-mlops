# Subtask 2.2 - Validação de Qualidade dos Dados

**Fase:** 2 - EXPLORAÇÃO & VALIDAÇÃO  
**Status:** ❌ Não Iniciada  
**Data de Início:** --  
**Data de Conclusão:** --  
**Tempo Estimado:** 2.0h  

---

## 📋 Objetivo
Identificar problemas de qualidade nos dados: valores missing, duplicatas, inconsistências, outliers e validar integridade referencial entre datasets.

---

## ✅ Checklist de Tarefas

- [ ] Análise de valores nulos/missing (%.isna() por coluna)
- [ ] Identificação de duplicatas (por chaves primárias)
- [ ] Validação de foreign keys:
  - [ ] Airlines: AirlineID presente e válido
  - [ ] Airports: AirportID presente e válido
  - [ ] Flights: UniqueCarrier, Origin, Dest são válidos
- [ ] Detecção de outliers:
  - [ ] ArrDelay outliers (IQR ou Z-score)
  - [ ] DepDelay outliers
  - [ ] Distance outliers
- [ ] Validação de ranges de valores:
  - [ ] Datas válidas (Year, Month, DayofMonth)
  - [ ] Distâncias positivas
  - [ ] Atrasos em ranges razoáveis
- [ ] Identificação de valores incomuns ou impossíveis
- [ ] Documentação de problemas encontrados

---

## 🎯 Critérios de Aceitação

- ✅ % de missing documentado por coluna
- ✅ Integridade referencial validada (>95%)
- ✅ Outliers identificados e justificados
- ✅ Problemas críticos documentados
- ✅ Recomendações de tratamento propostas
- ✅ Relatório de qualidade gerado

---

## 📝 Notas de Implementação

### 1. Análise de Missing Values

```python
# Missing por coluna
missing_analysis = pd.DataFrame({
    'Column': df_flights.columns,
    'Missing_Count': df_flights.isna().sum(),
    'Missing_Percent': (df_flights.isna().sum() / len(df_flights) * 100).round(2)
})
missing_analysis = missing_analysis[missing_analysis['Missing_Count'] > 0].sort_values('Missing_Percent', ascending=False)
print(missing_analysis)
```

### 2. Detecção de Duplicatas

```python
# Duplicatas em chaves primárias
print(f"Duplicatas (todos columns): {df_flights.duplicated().sum()}")
print(f"Duplicatas (Year,Month,Day,FlightNum): {df_flights.duplicated(subset=['Year','Month','DayofMonth','FlightNum']).sum()}")
```

### 3. Validação de Foreign Keys

```python
# Airlines referencias válidas
valid_airlines = df_airlines['AirlineID'].unique()
invalid_carrier = ~df_flights['UniqueCarrier'].isin(valid_airlines)
print(f"Flights com AirlineID inválido: {invalid_carrier.sum()}")

# Airports referencias válidas
valid_airports = df_airports['AirportID'].unique()
invalid_origin = ~df_flights['Origin'].isin(valid_airports)
invalid_dest = ~df_flights['Dest'].isin(valid_airports)
print(f"Flights com Origin inválido: {invalid_origin.sum()}")
print(f"Flights com Dest inválido: {invalid_dest.sum()}")
```

### 4. Detecção de Outliers (IQR Method)

```python
def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

# Aplicar para ArrDelay
arr_outliers, arr_lower, arr_upper = detect_outliers_iqr(df_flights, 'ArrDelay')
print(f"ArrDelay Outliers: {len(arr_outliers)} ({len(arr_outliers)/len(df_flights)*100:.2f}%)")
print(f"  Bounds: [{arr_lower}, {arr_upper}]")
print(f"  Extreme values: min={df_flights['ArrDelay'].min()}, max={df_flights['ArrDelay'].max()}")
```

### 5. Validação de Ranges

```python
# Validar Year
print(f"Year range: {df_flights['Year'].min()}-{df_flights['Year'].max()}")

# Validar Month (1-12)
invalid_months = df_flights[(df_flights['Month'] < 1) | (df_flights['Month'] > 12)]
print(f"Invalid months: {len(invalid_months)}")

# Validar Distance (>0)
invalid_distance = df_flights[df_flights['Distance'] <= 0]
print(f"Invalid distances (<=0): {len(invalid_distance)}")

# Validar datas
import datetime
df_flights['date'] = pd.to_datetime(df_flights[['Year', 'Month', 'DayofMonth']], errors='coerce')
invalid_dates = df_flights[df_flights['date'].isna()]
print(f"Invalid dates: {len(invalid_dates)}")
```

---

## 📊 Matriz de Qualidade dos Dados

Criar tabela de resultado:

| Aspecto | Status | Descrição |
|--------|--------|-----------|
| Missing Values | ✅/⚠️ | %total, colunas críticas |
| Duplicatas | ✅/⚠️ | count, impacto |
| Foreign Keys | ✅/⚠️ | integridade referencial |
| Outliers | ✅/⚠️ | count por coluna |
| Date Ranges | ✅/⚠️ | datas válidas |
| Numeric Ranges | ✅/⚠️ | valores razoáveis |

---

## 🔄 Changelog

| Data | Versão | Mudança | Autor |
|------|--------|---------|-------|
| 2026-03-23 | v1.0 | Criação inicial da subtask | Copilot |
| -- | -- | -- | -- |

---

## 💾 Outputs Esperados

1. Relatório de missing values
2. Relatório de duplicatas
3. Relatório de foreign keys
4. Relatório de outliers
5. Summary JSON da qualidade

---

## 📋 Template de Resultado

Ao completar, preencher:

```
## DATA QUALITY REPORT

### Missing Values
Total rows: ___
Columns with missing:
- ArrDelay: ___ (___%)
- DepDelay: ___ (___%)
- [others]

### Duplicatas
- Total duplicatas: ___
- Por chave primária: ___

### Foreign Keys
- Invalid Airlines: ___
- Invalid Origins: ___
- Invalid Destinations: ___

### Outliers (IQR Method)
- ArrDelay outliers: ___ (___%)
  Bounds: [___, ___]
- DepDelay outliers: ___ (___%)
  
### Data Ranges
- Year: ___ to ___
- Month: Valid? ___
- Day: Valid? ___
- Distance: ___ to ___ miles

### Overall Quality Score: __%
- Green: >95% - Excelente
- Yellow: 85-95% - Bom
- Orange: 70-85% - Aceitável
- Red: <70% - Requer atenção
```

---

## ⚠️ Possíveis Bloqueadores

- [ ] Alto volume de missing values (>50%)
- [ ] Integridade referencial comprometida (<90%)
- [ ] Muitos outliers ilegítimos
- [ ] Datas inválidas em volume
- [ ] Valores negativos ilegítimos

Quando encontrar bloqueadores, documentar abaixo:
```
[BLOQUEADOR] - Descrição do problema
Impacto: ...
Solução proposta: ...
```

