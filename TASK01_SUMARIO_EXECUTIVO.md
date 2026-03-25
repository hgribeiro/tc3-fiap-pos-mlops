# 📊 TASK 01 - EDA FLIGHT DELAY PREDICTION
## SUMÁRIO EXECUTIVO - RESULTADOS FINAIS

---

## ✅ STATUS: COMPLETADA COM SUCESSO

**Data:** 23 de Março, 2026  
**Tempo de Execução:** 5 minutos  
**Script Principal:** [src/01_eda.py](src/01_eda.py)  
**Dataset Utilizado:** [data/flights.csv](data/flights.csv) (~592MB)

**Resultado:** 🟢 **PRONTO PARA PRÓXIMA FASE**

---

## 📋 RESUMO DOS RESULTADOS

### Dataset Principal
```
Total de Voos:              582.319 registros
Período:                    Janeiro - Dezembro 2015
Colunas:                    28 variáveis (15 numéricas + 11 categóricas + 2 derivadas)
Taxa de Completude:        >99% (dataset limpo e preparado)
Arquivo Processado:        data/processed/flights_sample_processed.csv (81MB)
```

### Métricas-Chave de Atrasos
```
┌────────────────────────────────────────────────────────┐
│ INDICADOR                          │ VALOR             │
├────────────────────────────────────────────────────────┤
│ Taxa de Atraso (>15 min)           │ 35.73% (208.074) │
│ Taxa de Voos Pontuais              │ 62.40% (374.245) │
│ Taxa de Cancelamentos              │ 1.56%  (~9.100)  │
│ Taxa de Desvios                    │ 0.28%  (~1.600)  │
│ Atraso Médio (quando atrasado)     │ 33.16 minutos    │
│ Atraso Mediano                     │ 15 minutos       │
│ Atraso Máximo                      │ 924 minutos      │
│ Desvio Padrão (Atrasos)            │ 34.96 minutos    │
└────────────────────────────────────────────────────────┘
```

---

## 🎯 TOP INSIGHTS DESCOBERTOS

### 1. **Correlação MUITO FORTE: DEPARTURE_DELAY → ARRIVAL_DELAY**
   - **Correlação de Pearson:** 0.944 (excelente preditor)
   - **Implicação:** Atraso de partida quase garante atraso de chegada
   - **Aplicação:** DEPARTURE_DELAY será feature muito importante no modelo

### 2. **SAZONALIDADE CLARA - Padrão por Mês**
   | Mês | Taxa Atraso | Atraso Médio |
   |-----|-------------|--------------|
   | Junho (6) | 41% | +9.81 min |
   | Janeiro (1) | 38% | +5.93 min |
   | Setembro (9) | 31% | -0.42 min |
   | Dezembro (12) | 37% | +5.93 min |
   
   → **Verão norte-americano = maior congestionamento**

### 3. **DIA DA SEMANA: Segunda-feira é a Pior**
   | Dia | Atraso Médio | Taxa Atraso |
   |-----|--------------|------------|
   | Segunda (1) | +6.07 min | 38.3% |
   | Domingo (7) | +5.93 min | 37.9% |
   | Sexta (6) | +2.00 min | 31.2% |
   
   → **Efeito acumulativo de fim de semana**

### 4. **PERÍODO DO DIA: Manhã É Significativamente Melhor**
   | Período | Atraso Médio | Categoria |
   |---------|--------------|-----------|
   | Evening (17:00-20:59) | +9.75 min | **PIOR** |
   | Night (21:00-04:59) | +8.06 min | |
   | Afternoon (12:00-16:59) | +7.64 min | |
   | Morning (05:00-11:59) | +0.20 min | **MELHOR** |
   
   → **Voos matutinos têm 49x menos atraso**

### 5. **COMPANHIAS AÉREAS: Qualidade Operacional Varia Muito**
   **Top 3 Piores (Atraso Médio):**
   - NK (Spirit): +14.20 min
   - F9 (Frontier): +12.08 min
   - MQ (Endeavor): +11.29 min
   
   **Top 3 Melhores (Atraso Médio):**
   - UA (United): +5.84 min
   - AS (Alaska): +6.07 min
   - DL (Delta): +7.58 min
   
   **Maior Volume:**
   - WN (Southwest): 126.719 voos (21.8% do total)

### 6. **DISTÂNCIA ≠ ATRASO (Hipótese Refutada)**
   - **Correlação r(DISTANCE, ARRIVAL_DELAY):** -0.024 (negligível)
   - **Padrão:** Voos longos NÃO são necessariamente mais atrasados
   - **Insight:** Distância não é bom preditor sozinha
   
   ![Scatter plot mostra distribuição aleatória, sem padrão linear]

### 7. **HUBS PRINCIPAIS Concentram Volume Mas Operações Eficientes**
   **Top 3 Aeroportos Origem (Volume):**
   - ATL (Atlanta): 34.953 voos | Atraso médio: ~6 min
   - ORD (Chicago): 28.529 voos | Atraso médio: ~5 min
   - DFW (Dallas): 23.822 voos | Atraso médio: ~4 min
   
   **Aeroportos Pequenos = Variabilidade Alta:**
   - STC (origem): Atraso médio +47.56 min
   - PPG (destino): Atraso médio +64.90 min

---

## 📊 VISUALIZAÇÕES GERADAS

7 gráficos profissionais criados em `docs/eda_plots/`:

| # | Arquivo | Conteúdo |
|---|---------|----------|
| 1 | `01_distribuicao_atrasos.png` | Histograma, boxplot, pie chart, contagem pontual vs atrasado |
| 2 | `02_analise_temporal.png` | Atrasos por mês, dia semana, período do dia, taxa mensal |
| 3 | `03_analise_companhias.png` | Top 10 companhias (atraso), Top 10 companhias (volume) |
| 4 | `04_analise_aeroportos.png` | Aeroportos origem/destino com maior atraso |
| 5 | `05_correlacao.png` | Matriz de correlação heatmap (7×7 variáveis numéricas) |
| 6 | `06_distancia_vs_atraso.png` | Scatter plot: Distância vs Atraso de Chegada |
| 7 | `07_cancelamentos.png` | Taxa cancelamentos/desvios, motivos cancelamento |

---

## 📁 ARTEFATOS CRIADOS

### ✅ Dados Processados
- **[data/processed/flights_sample_processed.csv](data/processed/flights_sample_processed.csv)** (81MB)
  - 582.319 registros × 28 colunas
  - Features derivadas: IS_DELAYED, DELAY_CATEGORY, DEPARTURE_PERIOD
  - Pronto para feature engineering

### ✅ Metadata & Resumo
- **[data/processed/eda_summary.json](data/processed/eda_summary.json)**
  ```json
  {
    "total_flights": 582319,
    "delay_rate": 0.3573,
    "avg_delay_when_delayed": 33.16,
    "cancellation_rate": 0.0156,
    "diversion_rate": 0.0028,
    "worst_month": 6,
    "worst_day_of_week": 1,
    "worst_airline": "NK"
  }
  ```

### ✅ Documentação
- **[TASK01_ANALISE_COMPLETA.md](TASK01_ANALISE_COMPLETA.md)** (Este arquivo com análise detalhada)
- **[docs/eda_plots/](docs/eda_plots/)** (7 visualizações PNG)

---

## 🔬 QUALIDADE DOS DADOS

### Validações Realizadas
- [x] Verificação de valores nulos (documentados)
- [x] Detecção de duplicatas (nenhuma encontrada)
- [x] Análise de outliers (documentados e mantidos)
- [x] Validação de tipos de dados
- [x] Consistência entre datasets relacionados (airlines, airports, flights)

### Problemas Encontrados
- ✅ **Mínimos:** Dataset em boa qualidade geral
- ✅ **Sem blockers:** Pronto para modelagem

---

## 🚀 RECOMENDAÇÕES PARA PRÓXIMAS FASES

### Phase 2: Feature Engineering (Próxima)
```bash
python src/02_feature_engineering.py
```
**Tarefas esperadas:**
- [ ] Normalização/scaling de variáveis numéricas
- [ ] Encoding de categóricas (AIRLINE, ORIGIN, DESTINATION)
- [ ] Feature selection (remover colineares)
- [ ] Train/Val/Test split estratificado 70/15/15
- [ ] Salvamento de encoders/scaler

### Phase 3: Modelagem Supervisionada
**Comandos:**
```bash
python src/03_supervised_classification.py
```

### Phase 4: Modelagem Não Supervisionada
```bash
python src/04_unsupervised.py
```

### Phase 5: Consolidação & Relatório
```bash
python src/05_model_report.py
python src/prepare_dashboard_data.py
```

---

## 💡 FEATURES RECOMENDADAS PARA MODELAGEM

### Features Obrigatórias (Alta Importância)
- `MONTH` - Sazonalidade clara
- `DAY_OF_WEEK` - Padrão semanal
- `DEPARTURE_PERIOD` - 4.9x diferença entre periods
- `AIRLINE` - Variação de 14.20 min a 5.84 min
- `ORIGIN_AIRPORT` - Efeito de hub vs aeroporto pequeno
- `DESTINATION_AIRPORT` - Congestão destino
- `SCHEDULED_DEPARTURE` - Correlação com período

### Features Optativas
- `DISTANCE` - Considerar para interações
- `SCHEDULED_TIME` - Tempo esperado de voo
- `TAIL_NUMBER` - Aeronave específica (se disponível para dados futuros)

### Features a Evitar
- ❌ `AIR_TIME` - Colinear com DISTANCE (r=0.99)
- ❌ `ELAPSED_TIME` - Colinear com SCHEDULED_TIME
- ❌ Atrasos reais (WHEELS_OFF, TAXI_OUT, etc) - DATA LEAKAGE

### Target Variable
- `IS_DELAYED = ARRIVAL_DELAY > 15 minutos`
- Distribuição: 35.7% classe positiva (levemente desbalanceada)
- Recomendação: Usar stratified split + AUC-ROC como métrica

---

## 📈 ESTATÍSTICAS DETALHADAS

### Distribuição por Hora de Partida
```
Morning   (05:00-11:59):  Atraso médio 0.20 min    (MELHOR)
Afternoon (12:00-16:59):  Atraso médio 7.64 min
Evening   (17:00-20:59):  Atraso médio 9.75 min    (PIOR)
Night     (21:00-04:59):  Atraso médio 8.06 min
```

### Distribuição por Companhia
- **WN (Southwest):** 126.719 voos | Taxa atraso 33.2%
- **DL (Delta):** 87.400 voos | Taxa atraso 34.8%
- **AA (American):** 72.838 voos | Taxa atraso 37.1%

### Matriz de Correlação (Principais)
```
DEPARTURE_DELAY ↔ ARRIVAL_DELAY:  r = 0.944  [MUITO FORTE]
AIR_TIME ↔ DISTANCE:              r = 0.99   [PERFEITA]
DISTANCE ↔ ATRASO:                r = -0.02  [NULA]
TAXI_OUT ↔ ATRASO:                r = 0.23   [FRACO]
```

---

## ✨ CONCLUSÕES

### Principais Achados
1. **35.7% dos voos têm atraso > 15 minutos** → Oportunidade clara para predictions
2. **DEPARTURE_DELAY é forte preditor de ARRIVAL_DELAY** (r=0.944)
3. **Sazonalidade, dia da semana e período do dia têm efeito significativo**
4. **Qualidade varია muito por companhia aérea** (14.20 min vs 5.84 min)
5. **Distância não é fator determinante de atraso** (correlação ~0)

### Recomendações de Modeling
- ✅ Usar features temporais (MONTH, DAY_OF_WEEK, DEPARTURE_PERIOD)
- ✅ Incluir AIRLINE como preditor (variação de 8.3 min entre melhores/piores)
- ✅ Considerar aeroportos de origem (efeito de entrada vs saída)
- ✅ Usar stratified split para preservar distribuição de classes
- ✅ Métrica principal: AUC-ROC (melhor para desbalanceamento)
- ❌ Remover AIR_TIME (colinear) e variáveis com data leakage

### Dataset Readiness
- **Status:** ✅ PRONTO PARA FEATURE ENGINEERING
- **Qualidade:** BOA (>99% completude)
- **Tamanho:** Adequado (582k registros)
- **Próxima fase:** [src/02_feature_engineering.py](src/02_feature_engineering.py)

---

## 📌 CHECKLIST FINAL

- [x] Carregamento dos 3 datasets (airlines, airports, flights)
- [x] Análise descritiva completa
- [x] Validação de qualidade dos dados
- [x] Criação de features derivadas
- [x] 7 visualizações exploratórias geradas
- [x] 6+ insights principais identificados
- [x] Dataset processado salvo (flights_sample_processed.csv)
- [x] Metadata salva (eda_summary.json)
- [x] Documentação consolidada
- [x] README atualizado com achados

**TASK 01: ✅ COMPLETADA COM SUCESSO**

---

*Gerado em 2026-03-23*  
*Pipeline: EDA → Feature Engineering → Supervised Models → Unsupervised → Dashboard*
