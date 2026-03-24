# Subtask 3.2 - Visualizações Bivariadas & Correlações

**Fase:** 3 - VISUALIZAÇÕES & INSIGHTS  
**Status:** ❌ Não Iniciada  
**Data de Início:** --  
**Data de Conclusão:** --  
**Tempo Estimado:** 2.0h  

---

## 📋 Objetivo
Explorar relações entre pares de variáveis, correlações numéricas e padrões em agregações por grupos para entender dependências e relacionamentos.

---

## ✅ Checklist de Tarefas

- [ ] Criar matriz de correlação para variáveis numéricas
- [ ] Gerar heatmap de correlação
- [ ] Criar scatter plots para relações numéricas principais
- [ ] Criar gráficos categóricos × numéricos (boxplot, violinplot)
- [ ] Analisar padrões por grupo:
  - [ ] Atrasos por companhia aérea
  - [ ] Atrasos por aeroporto (origin/destination)
  - [ ] Padrões por dia da semana
  - [ ] Padrões sazonais (mês/trimestre)
- [ ] Criar análises de séries temporais (se data disponível)
- [ ] Documentar correlações significativas (>0.3)
- [ ] Salvar todas as visualizações

---

## 🎯 Critérios de Aceitação

- ✅ Mínimo 8-10 visualizações bivariadas criadas
- ✅ Heatmap de correlação clara e interpretável
- ✅ Correlações numéricas analisadas (>0.3 documentadas)
- ✅ Gráficos de agregação por grupo (mínimo 4)
- ✅ Descobertas não óbvias documentadas
- ✅ Qualidade visual profissional
- ✅ Todas em `docs/eda_plots/`

---

## 📝 Notas de Implementação

### 1. Matriz e Heatmap de Correlação

```python
# Calcular correlação
numeric_cols = ['ArrDelay', 'DepDelay', 'Distance', 'AirTime', 'TaxiIn', 'TaxiOut']
correlation_matrix = df_flights[numeric_cols].corr()

# Heatmap
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, ax=ax, cbar_kws={"shrink": 0.8})
ax.set_title('Correlation Matrix - Flight Numeric Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/eda_plots/11_correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.close()

# Documentar correlações >0.3
print("Correlações significativas (>0.3):")
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        corr_value = correlation_matrix.iloc[i, j]
        if abs(corr_value) > 0.3:
            print(f"{correlation_matrix.columns[i]} <-> {correlation_matrix.columns[j]}: {corr_value:.3f}")
```

### 2. Scatter Plots - Relações Numéricas

```python
# Distance vs ArrDelay
fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(df_flights['Distance'], df_flights['ArrDelay'], alpha=0.3, s=10, color='steelblue')
ax.set_xlabel('Distance (miles)', fontsize=12)
ax.set_ylabel('Arrival Delay (minutes)', fontsize=12)
ax.set_title('Distance vs Arrival Delay', fontsize=14, fontweight='bold')
# Adicionar linha de tendência
z = np.polyfit(df_flights['Distance'].dropna(), 
               df_flights.loc[df_flights['Distance'].notna(), 'ArrDelay'].dropna(), 1)
p = np.poly1d(z)
ax.plot(sorted(df_flights['Distance'].unique()), 
        p(sorted(df_flights['Distance'].unique())), 
        "r--", linewidth=2, label='Trend')
ax.legend()
plt.tight_layout()
plt.savefig('docs/eda_plots/12_distance_vs_arrdelay.png', dpi=300, bbox_inches='tight')
plt.close()

# AirTime vs ArrDelay
fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(df_flights['AirTime'], df_flights['ArrDelay'], alpha=0.3, s=10, color='coral')
ax.set_xlabel('Air Time (minutes)', fontsize=12)
ax.set_ylabel('Arrival Delay (minutes)', fontsize=12)
ax.set_title('Air Time vs Arrival Delay', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/eda_plots/13_airtime_vs_arrdelay.png', dpi=300, bbox_inches='tight')
plt.close()

# DepDelay vs ArrDelay
fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(df_flights['DepDelay'], df_flights['ArrDelay'], alpha=0.3, s=10, color='green')
ax.set_xlabel('Departure Delay (minutes)', fontsize=12)
ax.set_ylabel('Arrival Delay (minutes)', fontsize=12)
ax.set_title('Departure Delay vs Arrival Delay', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/eda_plots/14_depdelay_vs_arrdelay.png', dpi=300, bbox_inches='tight')
plt.close()
```

### 3. Boxplots - Categórica × Numérica

```python
# ArrDelay por Airline (top 10)
fig, ax = plt.subplots(figsize=(14, 6))
top_airlines = df_flights['UniqueCarrier'].value_counts().head(10).index
df_top = df_flights[df_flights['UniqueCarrier'].isin(top_airlines)]
sns.boxplot(x='UniqueCarrier', y='ArrDelay', data=df_top, ax=ax, palette='Set2')
ax.set_xlabel('Airline', fontsize=12)
ax.set_ylabel('Arrival Delay (minutes)', fontsize=12)
ax.set_title('Arrival Delay Distribution by Airline (Top 10)', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('docs/eda_plots/15_arrdelay_by_airline.png', dpi=300, bbox_inches='tight')
plt.close()

# ArrDelay por Day of Week
fig, ax = plt.subplots(figsize=(12, 6))
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sns.boxplot(x='DayOfWeek', y='ArrDelay', data=df_flights, ax=ax, palette='husl')
ax.set_xticklabels(day_names, rotation=45)
ax.set_xlabel('Day of Week', fontsize=12)
ax.set_ylabel('Arrival Delay (minutes)', fontsize=12)
ax.set_title('Arrival Delay Distribution by Day of Week', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/eda_plots/16_arrdelay_by_dayofweek_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()

# ArrDelay por Month (sazonalidade)
fig, ax = plt.subplots(figsize=(12, 6))
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sns.boxplot(x='Month', y='ArrDelay', data=df_flights, ax=ax, palette='coolwarm')
ax.set_xticklabels(month_names, rotation=45)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Arrival Delay (minutes)', fontsize=12)
ax.set_title('Seasonal Pattern: Arrival Delay by Month', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/eda_plots/17_arrdelay_by_month.png', dpi=300, bbox_inches='tight')
plt.close()
```

### 4. Análises por Grupo - Agregações

```python
# Average delay por airline
fig, ax = plt.subplots(figsize=(14, 6))
airline_delay = df_flights.groupby('UniqueCarrier')['ArrDelay'].agg(['mean', 'count']).sort_values('mean', ascending=False)
airline_delay = airline_delay[airline_delay['count'] > 1000]  # Filtrar airlines com <1000 voos
sns.barplot(x=airline_delay.index, y=airline_delay['mean'], ax=ax, palette='rocket')
ax.set_xlabel('Airline', fontsize=12)
ax.set_ylabel('Average Arrival Delay (minutes)', fontsize=12)
ax.set_title('Average Arrival Delay by Airline (min 1000 flights)', fontsize=14, fontweight='bold')
ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('docs/eda_plots/18_avg_delay_by_airline.png', dpi=300, bbox_inches='tight')
plt.close()

# Cancellation rate por airline
fig, ax = plt.subplots(figsize=(14, 6))
cancel_rate = df_flights.groupby('UniqueCarrier')['Cancelled'].agg(['sum', 'count'])
cancel_rate['rate'] = (cancel_rate['sum'] / cancel_rate['count'] * 100).sort_values(ascending=False)
cancel_rate = cancel_rate[cancel_rate['count'] > 1000]
sns.barplot(x=cancel_rate.index, y=cancel_rate['rate'], ax=ax, palette='viridis')
ax.set_xlabel('Airline', fontsize=12)
ax.set_ylabel('Cancellation Rate (%)', fontsize=12)
ax.set_title('Flight Cancellation Rate by Airline', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('docs/eda_plots/19_cancellation_rate_by_airline.png', dpi=300, bbox_inches='tight')
plt.close()

# Temporal trend (flights per month)
fig, ax = plt.subplots(figsize=(12, 6))
monthly_flights = df_flights.groupby('Month').size()
ax.plot(monthly_flights.index, monthly_flights.values, marker='o', linewidth=2, markersize=8, color='steelblue')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Number of Flights', fontsize=12)
ax.set_title('Seasonal Trend: Number of Flights by Month', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('docs/eda_plots/20_temporal_trend.png', dpi=300, bbox_inches='tight')
plt.close()
```

---

## 🔄 Changelog

| Data | Versão | Mudança | Autor |
|------|--------|---------|-------|
| 2026-03-23 | v1.0 | Criação inicial da subtask | Copilot |
| -- | -- | -- | -- |

---

## 💾 Outputs Esperados

1. Mínimo 8-10 arquivos PNG/SVG em `docs/eda_plots/`
2. Matriz de correlação JSON
3. Summary de correlações significativas

---

## 📋 Checklist de Arquivos

- [ ] 11_correlation_matrix.png
- [ ] 12_distance_vs_arrdelay.png
- [ ] 13_airtime_vs_arrdelay.png
- [ ] 14_depdelay_vs_arrdelay.png
- [ ] 15_arrdelay_by_airline.png
- [ ] 16_arrdelay_by_dayofweek_boxplot.png
- [ ] 17_arrdelay_by_month.png
- [ ] 18_avg_delay_by_airline.png
- [ ] 19_cancellation_rate_by_airline.png
- [ ] 20_temporal_trend.png
- [ ] (se houver: mais 0-5 visualizações adicionais)

---

## 💡 Correlações a Documentar

Para cada correlação >0.3, anotar:
- Pair de variáveis
- Valor de correlação
- Tipo (positivo/negativo)
- Interpretação no contexto de negócio

Exemplo:
```
DepDelay <-> ArrDelay: 0.856 (forte positivo)
- Explicação: Atrasos na partida frequentemente resultam em atrasos na chegada
- Implicação: Uma variável pode ser redundante para modelagem

Distance <-> AirTime: 0.923 (muito forte positivo)
- Explicação: Distâncias maiores levam a tempos de voo maiores
- Implicação: Variáveis altamente colineares (usar só uma ou aplicar PCA)
```

---

## ⚠️ Possíveis Bloqueadores

- [ ] Muita colinearidade entre variáveis numéricas
- [ ] Scatter plots com muitos pontos são ilegíveis
- [ ] Correlações fracas (não há padrões interessantes)
- [ ] Valores missing afetam correlações

Quando encontrar bloqueadores, documentar abaixo:
```
[BLOQUEADOR] - Descrição do problema
Solução: ...
```

