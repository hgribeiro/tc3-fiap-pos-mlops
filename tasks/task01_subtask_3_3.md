# Subtask 3.3 - Análise de Padrões & Insights

**Fase:** 3 - VISUALIZAÇÕES & INSIGHTS  
**Status:** ❌ Não Iniciada  
**Data de Início:** --  
**Data de Conclusão:** --  
**Tempo Estimado:** 2.0h  

---

## 📋 Objetivo
Extrair conhecimento acionável dos dados através de análises aprofundadas, identificar padrões, anomalias e gerar recomendações para modelagem futura com base em descobertas.

---

## ✅ Checklist de Tarefas

- [ ] Identificar companhias aéreas principais:
  - [ ] Top N por volume de voos
  - [ ] Top N por atrasos percentuais
  - [ ] Top N por taxa de cancelamento
- [ ] Identificar aeroportos principais:
  - [ ] Top N origem por volume
  - [ ] Top N destino por volume
  - [ ] Aeroportos mais complexos (maior atraso)
- [ ] Analisar padrões temporais:
  - [ ] Horários com mais atrasos (trend intraday)
  - [ ] Dias da semana mais críticos
  - [ ] Sazonalidade (por mês/trimestre)
- [ ] Identificar relações entre variáveis:
  - [ ] Quais features correlacionam com atrasos
  - [ ] Efeito de distância em atrasos
  - [ ] Efeito de horário em atrasos
- [ ] Detectar anomalias/comportamentos inesperados
- [ ] Documentar mínimo 5-7 insights claros

---

## 🎯 Critérios de Aceitação

- ✅ Mínimo 5-7 insights claros e documentados
- ✅ Insights suportados por dados/visualizações
- ✅ Relevância para negócio (contexto de voos)
- ✅ Sugestões de features para próximas etapas
- ✅ Anomalias limitadas e explicadas
- ✅ Impacto de negócio estimado (quando aplicável)

---

## 📝 Notas de Implementação

### Análises por Tema

#### 1. Companhias Aéreas - Análise Detalhada

```python
# Resumo por companhia
airline_summary = df_flights.groupby('UniqueCarrier').agg({
    'FlightNum': 'count',  # Total de voos
    'ArrDelay': ['mean', 'median', 'std'],
    'DepDelay': ['mean', 'median'],
    'Cancelled': lambda x: (x.sum() / len(x) * 100),  # % cancelamento
    'Diverted': 'sum',
    'Distance': 'mean'
}).round(2)

airline_summary.columns = ['Total_Flights', 'AvgArrDelay', 'MedianArrDelay', 'StdArrDelay', 
                           'AvgDepDelay', 'MedianDepDelay', 'CancellationRate_%', 
                           'Diversions', 'AvgDistance']
airline_summary = airline_summary.sort_values('Total_Flights', ascending=False)

print("=" * 80)
print("COMPANHIAS AÉREAS - SUMÁRIO")
print("=" * 80)
print(airline_summary.head(10))

# Insights a extrair:
# - Qual companhia tem maior atraso médio?
# - Qual tem maior taxa de cancelamento?
# - Há correlação entre volume de voos e qualidade de serviço?
# - Outliers (airlines muito boas ou muito ruins)?

print("\n🔍 INSIGHTS:")
worst_airline = airline_summary['AvgArrDelay'].idxmax()
best_airline = airline_summary['AvgArrDelay'].idxmin()
print(f"- Pior performance (atraso): {worst_airline} ({airline_summary.loc[worst_airline, 'AvgArrDelay']:.2f} min média)")
print(f"- Melhor performance (atraso): {best_airline} ({airline_summary.loc[best_airline, 'AvgArrDelay']:.2f} min média)")

most_cancelled = airline_summary['CancellationRate_%'].idxmax()
print(f"- Maior taxa de cancelamento: {most_cancelled} ({airline_summary.loc[most_cancelled, 'CancellationRate_%']:.2f}%)")
```

#### 2. Aeroportos - Análise Detalhada

```python
# Resumo por aeroporto origem
origin_summary = df_flights.groupby('Origin').agg({
    'FlightNum': 'count',
    'ArrDelay': ['mean', 'median'],
    'DepDelay': 'mean',
    'Cancelled': lambda x: (x.sum() / len(x) * 100)
}).round(2)

origin_summary.columns = ['Total_Departures', 'AvgArrDelay', 'MedianArrDelay', 'AvgDepDelay', 'CancellationRate_%']
origin_summary = origin_summary.sort_values('Total_Departures', ascending=False)

print("\n" + "=" * 80)
print("AEROPORTOS - SUMÁRIO (ORIGEM)")
print("=" * 80)
print(origin_summary.head(15))

# Resumo por aeroporto destino
dest_summary = df_flights.groupby('Dest').agg({
    'FlightNum': 'count',
    'ArrDelay': ['mean', 'median'],
    'DepDelay': 'mean'
}).round(2)

dest_summary.columns = ['Total_Arrivals', 'AvgArrDelay', 'MedianArrDelay', 'AvgDepDelay']
dest_summary = dest_summary.sort_values('Total_Arrivals', ascending=False)

print("\n" + "=" * 80)
print("AEROPORTOS - SUMÁRIO (DESTINO)")
print("=" * 80)
print(dest_summary.head(15))

# Insights a extrair:
print("\n🔍 INSIGHTS:")
worst_origin = origin_summary['AvgArrDelay'].idxmax()
most_congested = origin_summary['Total_Departures'].idxmax()
print(f"- Aeroporto com maior atraso médio (origem): {worst_origin} ({origin_summary.loc[worst_origin, 'AvgArrDelay']:.2f} min)")
print(f"- Aeroporto mais movimentado (origem): {most_congested} ({origin_summary.loc[most_congested, 'Total_Departures']:.0f} voos)")
```

#### 3. Padrões Temporais

```python
# Atrasos por hora do dia
hourly_pattern = df_flights.groupby('Hour').agg({
    'ArrDelay': ['mean', 'count'],
    'Cancelled': 'sum'
}).round(2)

hourly_pattern.columns = ['AvgArrDelay', 'FlightCount', 'Cancellations']

print("\n" + "=" * 80)
print("PADRÕES HORÁRIOS (INTRA-DAY)")
print("=" * 80)
print(hourly_pattern)

# Visualizar tendência
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(hourly_pattern.index, hourly_pattern['AvgArrDelay'], marker='o', linewidth=2, color='steelblue')
ax.set_xlabel('Hour of Day', fontsize=12)
ax.set_ylabel('Average Arrival Delay (minutes)', fontsize=12)
ax.set_title('Intra-day Pattern: Average Delay by Departure Hour', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xticks(range(0, 24, 2))
plt.tight_layout()
plt.savefig('docs/eda_plots/21_hourly_pattern.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n🔍 INSIGHTS:")
worst_hour = hourly_pattern['AvgArrDelay'].idxmax()
best_hour = hourly_pattern['AvgArrDelay'].idxmin()
print(f"- Hora com maior atraso: {worst_hour}:00 ({hourly_pattern.loc[worst_hour, 'AvgArrDelay']:.2f} min média)")
print(f"- Hora com menor atraso: {best_hour}:00 ({hourly_pattern.loc[best_hour, 'AvgArrDelay']:.2f} min média)")

# Sazonalidade
monthly_pattern = df_flights.groupby('Month').agg({
    'ArrDelay': ['mean', 'count'],
    'Cancelled': lambda x: (x.sum() / len(x) * 100)
}).round(2)

monthly_pattern.columns = ['AvgArrDelay', 'FlightCount', 'CancellationRate_%']

print("\n" + "=" * 80)
print("PADRÕES SAZONAIS (POR MÊS)")
print("=" * 80)
print(monthly_pattern)

season_map = {1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring',
              6: 'Summer', 7: 'Summer', 8: 'Summer', 9: 'Fall', 10: 'Fall', 11: 'Fall', 12: 'Winter'}

print("\n🔍 INSIGHTS SAZONAIS:")
# Agrupar por estação
df_flights['Season_temp'] = df_flights['Month'].map(season_map)
seasonal = df_flights.groupby('Season_temp')['ArrDelay'].mean().round(2)
print(f"Atraso médio por estação:\n{seasonal}")
```

#### 4. Distância vs Atrasos

```python
# Analisar efeito de distância
distance_bins = [0, 500, 1000, 1500, 2000, 2500, 5000]
df_flights['DistanceBin'] = pd.cut(df_flights['Distance'], bins=distance_bins)

distance_analysis = df_flights.groupby('DistanceBin', observed=True).agg({
    'FlightNum': 'count',
    'ArrDelay': ['mean', 'median'],
    'Distance': 'mean'
}).round(2)

distance_analysis.columns = ['FlightCount', 'AvgArrDelay', 'MedianArrDelay', 'AvgDistance']

print("\n" + "=" * 80)
print("ANÁLISE DE DISTÂNCIA vs ATRASOS")
print("=" * 80)
print(distance_analysis)

print("\n🔍 INSIGHTS:")
print("- Voos curtos têm menos atrasos do que voos longos?")
print("- Há ponto de inflexão na distância (ex: voos >2000 milhas)?")

# Correlação
corr_distance_delay = df_flights['Distance'].corr(df_flights['ArrDelay'])
print(f"- Correlação Distance ↔ ArrDelay: {corr_distance_delay:.3f}")
```

#### 5. Identificar Anomalias

```python
print("\n" + "=" * 80)
print("ANOMALIAS & COMPORTAMENTOS INESPERADOS")
print("=" * 80)

# Cancelamentos vs Atrasos
cancelled = df_flights[df_flights['Cancelled'] == 1]
not_cancelled = df_flights[df_flights['Cancelled'] == 0]
print(f"\nCancelamentos: {len(cancelled)} voos ({len(cancelled)/len(df_flights)*100:.2f}%)")

# Voos com atraso negativo (chegaram antes do previsto)
early_arrivals = df_flights[df_flights['ArrDelay'] < -30]
print(f"Voos com >30 min de antecedência: {len(early_arrivals)} ({len(early_arrivals)/len(df_flights)*100:.2f}%)")

# Voos diverted
diverted = df_flights[df_flights['Diverted'] == 1]
print(f"Voos desviados: {len(diverted)} ({len(diverted)/len(df_flights)*100:.2f}%)")

# Distribuição de motivos de cancelamento
print(f"\nMotivos de cancelamento:")
print(df_flights[df_flights['Cancelled'] == 1]['CancellationCode'].value_counts())
```

---

## 🔄 Changelog

| Data | Versão | Mudança | Autor |
|------|--------|---------|-------|
| 2026-03-23 | v1.0 | Criação inicial da subtask | Copilot |
| -- | -- | -- | -- |

---

## 💾 Outputs Esperados

1. Análise consolidada em Markdown
2. Tabelas de resumo (airlines, airports, temporal)
3. Mínimo 1-2 gráficos adicionais
4. JSON com insights estruturados

---

## 📋 Template de Insights

Documentar cada insight com:
1. **Descoberta**: O que foi encontrado?
2. **Evidência**: Qual métrica/visualização suporta?
3. **Impacto**: Por que é relevante?
4. **Ação**: Próximas etapas / implicação para modelagem

Exemplo:
```
## INSIGHT 1: Impacto Significativo da Companhia Aérea nos Atrasos
**Descoberta**: Diferentes companhias têm performance muito variada em atrasos
- Pior: Airline X (média 22.5 min)
- Melhor: Airline Y (média 4.2 min)
- Diferença: 18.3 minutos (437% maior)

**Evidência**: 
- Gráfico: 18_avg_delay_by_airline.png
- Dados: airline_summary.head(10)

**Impacto**: 
- Indica que processos operacionais diferem significativamente
- Airline pode ser feature forte para modelo preditivo

**Ação**:
- Incluir UniqueCarrier como variável categórica no modelo
- Investigar razões de performance diferente para modelagem de causas
```

---

## 🎯 Mínimo de Insights Esperados

- [ ] 1-2 sobre companhias aéreas
- [ ] 1-2 sobre aeroportos/rotas
- [ ] 1-2 sobre padrões temporais
- [ ] 1 sobre relações entre variáveis
- [ ] 1 sobre anomalias ou comportamentos inesperados
- [ ] **Total: 5-7 insights**

---

## ⚠️ Possíveis Bloqueadores

- [ ] Poucos padrões ou insights interessantes
- [ ] Correlações fracas
- [ ] Dados muito granulares (difícil achar padrões)
- [ ] Anomalias afetam análise (outliers extremos)

Quando encontrar bloqueadores, documentar abaixo:
```
[BLOQUEADOR] - Descrição do problema
Exploração alternativa: ...
```

