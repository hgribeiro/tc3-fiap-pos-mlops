# Subtask 1.2 - Carregamento Otimizado dos Dados

**Fase:** 1 - SETUP & CARREGAMENTO  
**Status:** ❌ Não Iniciada  
**Data de Início:** --  
**Data de Conclusão:** --  
**Tempo Estimado:** 1.0h  

---

## 📋 Objetivo
Carregar os três datasets (airlines, airports, flights) com estratégia apropriada para tamanhos diferentes, otimizando memória e performance.

---

## ✅ Checklist de Tarefas

- [ ] Carregar `airlines.csv` integralmente
- [ ] Carregar `airports.csv` integralmente
- [ ] Carregar `flights.csv` com otimização (dtypes, chunks ou amostragem)
- [ ] Validar dimensões (shape) de cada dataset
- [ ] Listar colunas e tipos de dados
- [ ] Exibir .head() de cada dataset (verificar integridade)
- [ ] Documentar estratégia de carregamento escolhida

---

## 🎯 Critérios de Aceitação

- ✅ 3 DataFrames carregados sem erro de memória
- ✅ Dimensões documentadas (shape verificado)
- ✅ Estratégia de otimização escolhida e justificada
- ✅ Memory usage dentro de limite razoável (<4GB)
- ✅ Primeiras linhas verificadas para cada dataset
- ✅ Tipos de dados validados

---

## 📝 Notas de Implementação

### Airlines.csv
- Tamanho: ~359 bytes
- Carregamento: Direto (sem otimização necessária)
- Colunas esperadas: AirlineID, AirlineName, etc.

### Airports.csv
- Tamanho: ~24KB
- Carregamento: Direto (sem otimização necessária)
- Colunas esperadas: AirportID, AirportName, City, Country, etc.

### Flights.csv (⚠️ GRANDE)
- Tamanho: ~592MB
- **Estratégia A: Dtypes Otimizados** (recomendado)
  ```python
  dtypes = {
      'Year': 'int16',
      'Month': 'int8',
      'DayofMonth': 'int8',
      'DayOfWeek': 'int8',
      'DepTime': 'float32',
      'CRSDepTime': 'int16',
      'ArrTime': 'float32',
      'CRSArrTime': 'int16',
      'UniqueCarrier': 'category',
      'FlightNum': 'int32',
      'TailNum': 'category',
      'ActualElapsedTime': 'float32',
      'CRSElapsedTime': 'float32',
      'AirTime': 'float32',
      'ArrDelay': 'float32',
      'DepDelay': 'float32',
      'Origin': 'category',
      'Dest': 'category',
      'Distance': 'int32',
      'TaxiIn': 'float32',
      'TaxiOut': 'float32',
      'Cancelled': 'int8',
      'CancellationCode': 'category',
      'Diverted': 'int8',
      'CarrierDelay': 'float32',
      'WeatherDelay': 'float32',
      'NASDelay': 'float32',
      'SecurityDelay': 'float32',
      'LateAircraftDelay': 'float32'
  }
  df_flights = pd.read_csv('data/flights.csv', dtype=dtypes, na_values=['NA', 'N/A'])
  ```

- **Estratégia B: Amostragem Aleatória** (se dtypes não suficiente)
  ```python
  df_flights = pd.read_csv('data/flights.csv', 
                            skiprows=lambda i: i>0 and np.random.random() > 0.1)
  # Resultado: ~10% do dataset
  ```

- **Estratégia C: Leitura por Chunks** (se processamento incremental necessário)
  ```python
  chunk_size = 100000
  chunks = []
  for chunk in pd.read_csv('data/flights.csv', chunksize=chunk_size):
      chunks.append(chunk)
  df_flights = pd.concat(chunks, ignore_index=True)
  ```

---

## 🔄 Changelog

| Data | Versão | Mudança | Autor |
|------|--------|---------|-------|
| 2026-03-23 | v1.0 | Criação inicial da subtask | Copilot |
| -- | -- | -- | -- |

---

## 💾 Outputs Esperados

1. `df_airlines` - DataFrame com dados de companhias
2. `df_airports` - DataFrame com dados de aeroportos
3. `df_flights` - DataFrame com dados de voos
4. Relatório de shapes e memory usage

---

## 📊 Verificações a Documentar

Após carregamento, documentar:

```
Airlines:shape = ___
Airports.shape = ___
Flights.shape = ___

Memory usage total = ___ MB

Estratégia escolhida: [ ] Dtypes | [ ] Chunks | [ ] Amostragem
Justificativa: _____

Colunas flights.csv:
_____
```

---

## ⚠️ Possíveis Bloqueadores

- [ ] Memory overflow ao carregar flights.csv
- [ ] Arquivo corrompido ou encoding diferente
- [ ] Colunas diferentes das esperadas
- [ ] Valores missing não identificados (usar na_values)

Quando encontrar bloqueadores, documentar abaixo:
```
[BLOQUEADOR] - Descrição do problema
Solução: ...
```

