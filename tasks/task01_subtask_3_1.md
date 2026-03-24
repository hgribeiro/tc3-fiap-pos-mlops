# Subtask 3.1 - Visualizações Univariadas

**Fase:** 3 - VISUALIZAÇÕES & INSIGHTS  
**Status:** ❌ Não Iniciada  
**Data de Início:** --  
**Data de Conclusão:** --  
**Tempo Estimado:** 1.5h  

---

## 📋 Objetivo
Criar visualizações de distribuições individuais de variáveis para entender como se distribuem os dados nas dimensões principais.

---

## ✅ Checklist de Tarefas

- [ ] Criar mínimo 3 histogramas (variáveis numéricas principais)
- [ ] Criar mínimo 3 gráficos de barras (categóricas relevantes)
- [ ] Criar mínimo 2 boxplots (para identificar outliers)
- [ ] Adicionar 1 distribuição por tipo de dados raro (se houver)
- [ ] Adicionar escalas e labels apropriados
- [ ] Usar cores e estilo consistentes (seaborn palette)
- [ ] Salvar todas as visualizações em `docs/eda_plots/`
- [ ] Documentar insights de cada visualização

---

## 🎯 Critérios de Aceitação

- ✅ Mínimo 8-10 visualizações univariadas criadas
- ✅ Todas as visualizações salvas em PNG/SVG
- ✅ Insights interpretados (qual é a distribuição?)
- ✅ Qualidade visual profissional
- ✅ Nomes de arquivo descritivos
- ✅ Legendas e títulos claros

---

## 📝 Notas de Implementação

### Setup de Visualização

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar estilo
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Criar diretório se não existir
import os
os.makedirs('docs/eda_plots', exist_ok=True)
```

### Visualizações Recomendadas por Tipo

#### 1. Histogramas - Variáveis Numéricas

```python
# ArrDelay distribution
fig, ax = plt.subplots(figsize=(12, 6))
df_flights['ArrDelay'].hist(bins=100, ax=ax, color='steelblue', edgecolor='black')
ax.set_xlabel('Arrival Delay (minutes)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Distribution of Arrival Delays', fontsize=14, fontweight='bold')
ax.axvline(df_flights['ArrDelay'].mean(), color='red', linestyle='--', label=f'Mean: {df_flights["ArrDelay"].mean():.2f}')
ax.axvline(df_flights['ArrDelay'].median(), color='orange', linestyle='--', label=f'Median: {df_flights["ArrDelay"].median():.2f}')
ax.legend()
plt.tight_layout()
plt.savefig('docs/eda_plots/01_arr_delay_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# DepDelay distribution
fig, ax = plt.subplots(figsize=(12, 6))
df_flights['DepDelay'].hist(bins=100, ax=ax, color='coral', edgecolor='black')
ax.set_xlabel('Departure Delay (minutes)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Distribution of Departure Delays', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/eda_plots/02_dep_delay_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Distance distribution
fig, ax = plt.subplots(figsize=(12, 6))
df_flights['Distance'].hist(bins=100, ax=ax, color='green', edgecolor='black')
ax.set_xlabel('Distance (miles)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Distribution of Flight Distances', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/eda_plots/03_distance_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# AirTime distribution
fig, ax = plt.subplots(figsize=(12, 6))
df_flights['AirTime'].hist(bins=100, ax=ax, color='purple', edgecolor='black')
ax.set_xlabel('Air Time (minutes)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Distribution of Air Time', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/eda_plots/04_airtime_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
```

#### 2. Gráficos de Barras - Variáveis Categóricas

```python
# Top 10 Airlines
fig, ax = plt.subplots(figsize=(12, 6))
top_airlines = df_flights['UniqueCarrier'].value_counts().head(10)
sns.barplot(x=top_airlines.values, y=top_airlines.index, ax=ax, palette='Set2')
ax.set_xlabel('Number of Flights', fontsize=12)
ax.set_ylabel('Airline', fontsize=12)
ax.set_title('Top 10 Airlines by Number of Flights', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/eda_plots/05_top_airlines.png', dpi=300, bbox_inches='tight')
plt.close()

# Top 10 Origin Airports
fig, ax = plt.subplots(figsize=(12, 6))
top_origins = df_flights['Origin'].value_counts().head(10)
sns.barplot(x=top_origins.values, y=top_origins.index, ax=ax, palette='husl')
ax.set_xlabel('Number of Departures', fontsize=12)
ax.set_ylabel('Airport', fontsize=12)
ax.set_title('Top 10 Origin Airports', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/eda_plots/06_top_origins.png', dpi=300, bbox_inches='tight')
plt.close()

# Delays by Day of Week
fig, ax = plt.subplots(figsize=(12, 6))
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
delays_by_day = df_flights.groupby('DayOfWeek')['ArrDelay'].mean()
sns.barplot(x=range(7), y=delays_by_day.values, ax=ax, palette='coolwarm')
ax.set_xticklabels(day_names, rotation=45)
ax.set_xlabel('Day of Week', fontsize=12)
ax.set_ylabel('Average Arrival Delay (minutes)', fontsize=12)
ax.set_title('Average Arrival Delay by Day of Week', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/eda_plots/07_delays_by_dayofweek.png', dpi=300, bbox_inches='tight')
plt.close()

# Cancelled flights by airline (top 10)
fig, ax = plt.subplots(figsize=(12, 6))
cancelled_by_airline = df_flights[df_flights['Cancelled'] == 1]['UniqueCarrier'].value_counts().head(10)
sns.barplot(x=cancelled_by_airline.values, y=cancelled_by_airline.index, ax=ax, palette='rocket')
ax.set_xlabel('Number of Cancelled Flights', fontsize=12)
ax.set_ylabel('Airline', fontsize=12)
ax.set_title('Top 10 Airlines by Cancelled Flights', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/eda_plots/08_cancelled_by_airline.png', dpi=300, bbox_inches='tight')
plt.close()
```

#### 3. Boxplots - Identificar Outliers

```python
# ArrDelay boxplot
fig, ax = plt.subplots(figsize=(12, 6))
bp = ax.boxplot(df_flights['ArrDelay'].dropna(), vert=True, patch_artist=True)
bp['boxes'][0].set_facecolor('lightblue')
ax.set_ylabel('Arrival Delay (minutes)', fontsize=12)
ax.set_title('Boxplot of Arrival Delays (Outlier Detection)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('docs/eda_plots/09_arrdelay_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()

# DepDelay boxplot
fig, ax = plt.subplots(figsize=(12, 6))
bp = ax.boxplot(df_flights['DepDelay'].dropna(), vert=True, patch_artist=True)
bp['boxes'][0].set_facecolor('lightcoral')
ax.set_ylabel('Departure Delay (minutes)', fontsize=12)
ax.set_title('Boxplot of Departure Delays (Outlier Detection)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('docs/eda_plots/10_depdelay_boxplot.png', dpi=300, bbox_inches='tight')
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
2. Nomes descritivos: `01_arr_delay_distribution.png`, etc.
3. Resolução alta (300 DPI)

---

## 📋 Checklist de Arquivos

- [ ] 01_arr_delay_distribution.png
- [ ] 02_dep_delay_distribution.png
- [ ] 03_distance_distribution.png
- [ ] 04_airtime_distribution.png
- [ ] 05_top_airlines.png
- [ ] 06_top_origins.png
- [ ] 07_delays_by_dayofweek.png
- [ ] 08_cancelled_by_airline.png
- [ ] 09_arrdelay_boxplot.png
- [ ] 10_depdelay_boxplot.png
- [ ] (se houver: mais 0-5 visualizações adicionais)

---

## 💡 Insights a Documentar

Para cada visualização, anotar:
- Qual é a distribuição? (normal, skewed, bimodal, etc.)
- Valores extremos presentes? (outliers)
- Padrão inesperado? (anomalias)
- Implicação para modelagem futura?

Exemplo:
```
01_arr_delay_distribution.png
- Distribuição: Right-skewed (cauda longa positiva)
- Mean: X min, Median: Y min (mean > median confirma skew)
- Outliers: Atrasos >500 min (raros mas presentes)
- Insight: Maioria voos on-time, minoria com atrasos extremos
- Implicação: Considerar transformação log ou categorização para modelagem
```

---

## ⚠️ Possíveis Bloqueadores

- [ ] Matplotlib/Seaborn problemas de rendering
- [ ] Dataset muito grande para ser visualizado
- [ ] Memória insuficiente para criar múltiplos plots
- [ ] Valores extremos distorcem escala dos gráficos

Quando encontrar bloqueadores, documentar abaixo:
```
[BLOQUEADOR] - Descrição do problema
Solução: ...
```

