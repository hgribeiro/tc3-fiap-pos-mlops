"""
Análise Exploratória de Dados (EDA) - Flight Delay Prediction
Task 01: Exploração completa dos datasets de voos

Datasets:
- airlines.csv: Informações das companhias aéreas
- airports.csv: Informações dos aeroportos
- flights.csv: Dados de voos (~592MB)
"""

# %% Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

# %% Configurações
DATA_PATH = Path('./data')
PLOTS_PATH = Path('./docs/eda_plots')
PROCESSED_PATH = Path('./data/processed')

# Criar diretórios se não existirem
PLOTS_PATH.mkdir(parents=True, exist_ok=True)
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

# %% ============================================================================
# 1. CARREGAMENTO DOS DATASETS
# ============================================================================

print("=" * 80)
print("1. CARREGAMENTO E EXPLORAÇÃO INICIAL DOS DATASETS")
print("=" * 80)

# 1.1 Airlines
print("\n[1/3] Carregando airlines.csv...")
df_airlines = pd.read_csv(DATA_PATH / 'airlines.csv')
print(f"✓ Airlines carregado: {df_airlines.shape}")

# 1.2 Airports
print("\n[2/3] Carregando airports.csv...")
df_airports = pd.read_csv(DATA_PATH / 'airports.csv')
print(f"✓ Airports carregado: {df_airports.shape}")

# 1.3 Flights (com otimização de memória)
print("\n[3/3] Carregando flights.csv (arquivo grande - usando amostragem)...")

# Definir dtypes otimizados para reduzir uso de memória
dtypes_flights = {
    'YEAR': 'int16',
    'MONTH': 'int8',
    'DAY': 'int8',
    'DAY_OF_WEEK': 'int8',
    'AIRLINE': 'category',
    'FLIGHT_NUMBER': 'int16',
    'TAIL_NUMBER': 'category',
    'ORIGIN_AIRPORT': 'category',
    'DESTINATION_AIRPORT': 'category',
    'SCHEDULED_DEPARTURE': 'int16',
    'DEPARTURE_TIME': 'float32',
    'DEPARTURE_DELAY': 'float32',
    'TAXI_OUT': 'float32',
    'WHEELS_OFF': 'float32',
    'SCHEDULED_TIME': 'float32',
    'ELAPSED_TIME': 'float32',
    'AIR_TIME': 'float32',
    'DISTANCE': 'int16',
    'WHEELS_ON': 'float32',
    'TAXI_IN': 'float32',
    'SCHEDULED_ARRIVAL': 'int16',
    'ARRIVAL_TIME': 'float32',
    'ARRIVAL_DELAY': 'float32',
    'DIVERTED': 'int8',
    'CANCELLED': 'int8',
    'CANCELLATION_REASON': 'category',
    'AIR_SYSTEM_DELAY': 'float32',
    'SECURITY_DELAY': 'float32',
    'AIRLINE_DELAY': 'float32',
    'LATE_AIRCRAFT_DELAY': 'float32',
    'WEATHER_DELAY': 'float32'
}

# Carregar amostra de 10% para análise inicial
df_flights = pd.read_csv(
    DATA_PATH / 'flights.csv',
    dtype=dtypes_flights,
    skiprows=lambda i: i > 0 and np.random.random() > 0.1
)

print(f"✓ Flights carregado (amostra 10%): {df_flights.shape}")
print(f"  Memória utilizada: {df_flights.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# %% ============================================================================
# 2. EXPLORAÇÃO INICIAL
# ============================================================================

print("\n" + "=" * 80)
print("2. VISÃO GERAL DOS DATASETS")
print("=" * 80)

# 2.1 Airlines
print("\n--- AIRLINES ---")
print(f"Dimensões: {df_airlines.shape[0]} linhas x {df_airlines.shape[1]} colunas")
print("\nPrimeiras linhas:")
print(df_airlines.head())
print("\nTipos de dados:")
print(df_airlines.dtypes)
print(f"\nTotal de companhias: {df_airlines.shape[0]}")

# 2.2 Airports
print("\n--- AIRPORTS ---")
print(f"Dimensões: {df_airports.shape[0]} linhas x {df_airports.shape[1]} colunas")
print("\nPrimeiras linhas:")
print(df_airports.head())
print("\nTipos de dados:")
print(df_airports.dtypes)
print(f"\nTotal de aeroportos: {df_airports.shape[0]}")

# 2.3 Flights
print("\n--- FLIGHTS (AMOSTRA) ---")
print(f"Dimensões: {df_flights.shape[0]} linhas x {df_flights.shape[1]} colunas")
print("\nPrimeiras linhas:")
print(df_flights.head())
print("\nTipos de dados:")
print(df_flights.dtypes)
print("\nColunas disponíveis:")
print(df_flights.columns.tolist())

# %% ============================================================================
# 3. ANÁLISE DE QUALIDADE DOS DADOS
# ============================================================================

print("\n" + "=" * 80)
print("3. QUALIDADE DOS DADOS")
print("=" * 80)

# 3.1 Valores Nulos
print("\n--- VALORES NULOS ---")
print("\nAirlines:")
print(df_airlines.isna().sum())

print("\nAirports:")
missing_airports = df_airports.isna().sum()
print(missing_airports[missing_airports > 0] if missing_airports.sum() > 0 else "Sem valores nulos")

print("\nFlights (Top 15 colunas com missing):")
missing_flights = df_flights.isna().sum().sort_values(ascending=False)
print(missing_flights.head(15))
print(f"\nPercentual de missing por coluna:")
missing_pct = (df_flights.isna().sum() / len(df_flights) * 100).sort_values(ascending=False)
print(missing_pct.head(15))

# 3.2 Valores Duplicados
print("\n--- VALORES DUPLICADOS ---")
print(f"Airlines duplicadas: {df_airlines.duplicated().sum()}")
print(f"Airports duplicados: {df_airports.duplicated().sum()}")
print(f"Flights duplicados: {df_flights.duplicated().sum()}")

# 3.3 Validação de Relacionamentos
print("\n--- VALIDAÇÃO DE RELACIONAMENTOS ---")
airlines_in_flights = df_flights['AIRLINE'].unique()
airlines_in_master = df_airlines['IATA_CODE'].unique()
print(f"Airlines em flights: {len(airlines_in_flights)}")
print(f"Airlines em master: {len(airlines_in_master)}")
print(f"Airlines sem cadastro: {set(airlines_in_flights) - set(airlines_in_master)}")

airports_origin = df_flights['ORIGIN_AIRPORT'].unique()
airports_dest = df_flights['DESTINATION_AIRPORT'].unique()
airports_all = set(airports_origin) | set(airports_dest)
airports_master = set(df_airports['IATA_CODE'].unique())
print(f"\nAeroportos em flights (origem + destino): {len(airports_all)}")
print(f"Aeroportos em master: {len(airports_master)}")
print(f"Aeroportos sem cadastro: {len(airports_all - airports_master)}")

# %% ============================================================================
# 4. ESTATÍSTICAS DESCRITIVAS
# ============================================================================

print("\n" + "=" * 80)
print("4. ESTATÍSTICAS DESCRITIVAS")
print("=" * 80)

# 4.1 Variáveis Numéricas
print("\n--- VARIÁVEIS NUMÉRICAS ---")
print(df_flights.describe())

# 4.2 Variáveis Categóricas
print("\n--- VARIÁVEIS CATEGÓRICAS ---")
print("\nTop 10 Companhias Aéreas:")
print(df_flights['AIRLINE'].value_counts().head(10))

print("\nTop 10 Aeroportos de Origem:")
print(df_flights['ORIGIN_AIRPORT'].value_counts().head(10))

print("\nTop 10 Aeroportos de Destino:")
print(df_flights['DESTINATION_AIRPORT'].value_counts().head(10))

print("\nDistribuição por Mês:")
print(df_flights['MONTH'].value_counts().sort_index())

print("\nDistribuição por Dia da Semana:")
print(df_flights['DAY_OF_WEEK'].value_counts().sort_index())

# %% ============================================================================
# 5. CRIAÇÃO DE FEATURES DERIVADAS
# ============================================================================

print("\n" + "=" * 80)
print("5. CRIAÇÃO DE FEATURES DERIVADAS")
print("=" * 80)

# Criar feature: voo atrasado (classificação binária)
df_flights['IS_DELAYED'] = (df_flights['ARRIVAL_DELAY'] > 0).astype(int)

# Criar feature: categoria de atraso
def categorize_delay(delay):
    if pd.isna(delay):
        return 'Unknown'
    elif delay <= 0:
        return 'On Time'
    elif delay <= 15:
        return 'Minor Delay'
    elif delay <= 60:
        return 'Moderate Delay'
    else:
        return 'Major Delay'

df_flights['DELAY_CATEGORY'] = df_flights['ARRIVAL_DELAY'].apply(categorize_delay)

# Período do dia
def get_time_period(hour):
    if pd.isna(hour):
        return 'Unknown'
    hour = int(hour / 100)  # Converter de HHMM para HH
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'

df_flights['DEPARTURE_PERIOD'] = df_flights['SCHEDULED_DEPARTURE'].apply(get_time_period)

print("✓ Features criadas:")
print("  - IS_DELAYED: Voo atrasado (0/1)")
print("  - DELAY_CATEGORY: Categoria de atraso")
print("  - DEPARTURE_PERIOD: Período do dia")

print("\nDistribuição de voos atrasados:")
print(df_flights['IS_DELAYED'].value_counts())
print(f"\nTaxa de atrasos: {df_flights['IS_DELAYED'].mean()*100:.2f}%")

# %% ============================================================================
# 6. VISUALIZAÇÕES EXPLORATÓRIAS
# ============================================================================

print("\n" + "=" * 80)
print("6. GERANDO VISUALIZAÇÕES")
print("=" * 80)

# 6.1 Distribuição de Atrasos
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Histograma de atrasos de chegada
axes[0, 0].hist(df_flights['ARRIVAL_DELAY'].dropna(), bins=100, edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Atraso de Chegada (minutos)')
axes[0, 0].set_ylabel('Frequência')
axes[0, 0].set_title('Distribuição de Atrasos de Chegada')
axes[0, 0].set_xlim(-50, 200)

# Boxplot de atrasos
axes[0, 1].boxplot(df_flights['ARRIVAL_DELAY'].dropna(), vert=True)
axes[0, 1].set_ylabel('Atraso (minutos)')
axes[0, 1].set_title('Boxplot de Atrasos de Chegada')

# Pizza de categorias de atraso
delay_counts = df_flights['DELAY_CATEGORY'].value_counts()
axes[1, 0].pie(delay_counts, labels=delay_counts.index, autopct='%1.1f%%', startangle=90)
axes[1, 0].set_title('Distribuição por Categoria de Atraso')

# Voos atrasados vs pontuais
delay_binary = df_flights['IS_DELAYED'].value_counts()
axes[1, 1].bar(['Pontual', 'Atrasado'], delay_binary.values, color=['green', 'red'], alpha=0.7)
axes[1, 1].set_ylabel('Quantidade de Voos')
axes[1, 1].set_title('Voos Pontuais vs Atrasados')

plt.tight_layout()
plt.savefig(PLOTS_PATH / '01_distribuicao_atrasos.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 01_distribuicao_atrasos.png")

# 6.2 Análise Temporal
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Atrasos por mês
monthly_delays = df_flights.groupby('MONTH')['ARRIVAL_DELAY'].mean()
axes[0, 0].plot(monthly_delays.index, monthly_delays.values, marker='o', linewidth=2)
axes[0, 0].set_xlabel('Mês')
axes[0, 0].set_ylabel('Atraso Médio (minutos)')
axes[0, 0].set_title('Atraso Médio por Mês')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_xticks(range(1, 13))

# Atrasos por dia da semana
dow_delays = df_flights.groupby('DAY_OF_WEEK')['ARRIVAL_DELAY'].mean()
axes[0, 1].bar(dow_delays.index, dow_delays.values, color='skyblue', edgecolor='black')
axes[0, 1].set_xlabel('Dia da Semana (1=Segunda)')
axes[0, 1].set_ylabel('Atraso Médio (minutos)')
axes[0, 1].set_title('Atraso Médio por Dia da Semana')
axes[0, 1].set_xticks(range(1, 8))

# Atrasos por período do dia
period_delays = df_flights.groupby('DEPARTURE_PERIOD')['ARRIVAL_DELAY'].mean().sort_values()
axes[1, 0].barh(period_delays.index, period_delays.values, color='coral', edgecolor='black')
axes[1, 0].set_xlabel('Atraso Médio (minutos)')
axes[1, 0].set_title('Atraso Médio por Período do Dia')

# Taxa de atraso por mês
monthly_delay_rate = df_flights.groupby('MONTH')['IS_DELAYED'].mean() * 100
axes[1, 1].plot(monthly_delay_rate.index, monthly_delay_rate.values, marker='s', 
                linewidth=2, color='red')
axes[1, 1].set_xlabel('Mês')
axes[1, 1].set_ylabel('Taxa de Atraso (%)')
axes[1, 1].set_title('Taxa de Atraso por Mês')
axes[1, 1].grid(True, alpha=0.3)
axes[1, 1].set_xticks(range(1, 13))

plt.tight_layout()
plt.savefig(PLOTS_PATH / '02_analise_temporal.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 02_analise_temporal.png")

# 6.3 Análise por Companhia Aérea
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Top 10 companhias com mais atrasos
top_airlines_delay = df_flights.groupby('AIRLINE')['ARRIVAL_DELAY'].mean().sort_values(ascending=False).head(10)
axes[0].barh(range(len(top_airlines_delay)), top_airlines_delay.values, color='tomato', edgecolor='black')
axes[0].set_yticks(range(len(top_airlines_delay)))
axes[0].set_yticklabels(top_airlines_delay.index)
axes[0].set_xlabel('Atraso Médio (minutos)')
axes[0].set_title('Top 10 Companhias com Maior Atraso Médio')
axes[0].invert_yaxis()

# Top 10 companhias com mais voos
top_airlines_flights = df_flights['AIRLINE'].value_counts().head(10)
axes[1].bar(range(len(top_airlines_flights)), top_airlines_flights.values, 
            color='steelblue', edgecolor='black')
axes[1].set_xticks(range(len(top_airlines_flights)))
axes[1].set_xticklabels(top_airlines_flights.index, rotation=45)
axes[1].set_ylabel('Número de Voos')
axes[1].set_title('Top 10 Companhias com Mais Voos')

plt.tight_layout()
plt.savefig(PLOTS_PATH / '03_analise_companhias.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 03_analise_companhias.png")

# 6.4 Análise por Aeroporto
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Top 10 aeroportos de origem com mais atrasos
top_origin_delay = df_flights.groupby('ORIGIN_AIRPORT')['DEPARTURE_DELAY'].mean().sort_values(ascending=False).head(10)
axes[0].barh(range(len(top_origin_delay)), top_origin_delay.values, color='orange', edgecolor='black')
axes[0].set_yticks(range(len(top_origin_delay)))
axes[0].set_yticklabels(top_origin_delay.index)
axes[0].set_xlabel('Atraso Médio na Partida (minutos)')
axes[0].set_title('Top 10 Aeroportos com Maior Atraso na Partida')
axes[0].invert_yaxis()

# Top 10 aeroportos de destino com mais atrasos
top_dest_delay = df_flights.groupby('DESTINATION_AIRPORT')['ARRIVAL_DELAY'].mean().sort_values(ascending=False).head(10)
axes[1].barh(range(len(top_dest_delay)), top_dest_delay.values, color='purple', edgecolor='black')
axes[1].set_yticks(range(len(top_dest_delay)))
axes[1].set_yticklabels(top_dest_delay.index)
axes[1].set_xlabel('Atraso Médio na Chegada (minutos)')
axes[1].set_title('Top 10 Aeroportos com Maior Atraso na Chegada')
axes[1].invert_yaxis()

plt.tight_layout()
plt.savefig(PLOTS_PATH / '04_analise_aeroportos.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 04_analise_aeroportos.png")

# 6.5 Correlação entre variáveis numéricas
numeric_cols = ['DEPARTURE_DELAY', 'ARRIVAL_DELAY', 'AIR_TIME', 'DISTANCE', 
                'TAXI_OUT', 'TAXI_IN', 'ELAPSED_TIME']
correlation_matrix = df_flights[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=1)
plt.title('Matriz de Correlação - Variáveis Numéricas')
plt.tight_layout()
plt.savefig(PLOTS_PATH / '05_correlacao.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 05_correlacao.png")

# 6.6 Análise de Distância vs Atraso
plt.figure(figsize=(12, 6))
plt.scatter(df_flights['DISTANCE'], df_flights['ARRIVAL_DELAY'], 
            alpha=0.1, s=1)
plt.xlabel('Distância (milhas)')
plt.ylabel('Atraso na Chegada (minutos)')
plt.title('Relação entre Distância e Atraso')
plt.ylim(-50, 200)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(PLOTS_PATH / '06_distancia_vs_atraso.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 06_distancia_vs_atraso.png")

# 6.7 Análise de Cancelamentos e Desvios
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Taxa de cancelamento
cancel_rate = df_flights['CANCELLED'].mean() * 100
divert_rate = df_flights['DIVERTED'].mean() * 100
axes[0].bar(['Cancelados', 'Desviados'], [cancel_rate, divert_rate], 
            color=['red', 'orange'], edgecolor='black')
axes[0].set_ylabel('Taxa (%)')
axes[0].set_title('Taxa de Cancelamento e Desvio de Voos')

# Motivos de cancelamento
if df_flights['CANCELLATION_REASON'].notna().sum() > 0:
    cancel_reasons = df_flights['CANCELLATION_REASON'].value_counts()
    axes[1].pie(cancel_reasons, labels=cancel_reasons.index, autopct='%1.1f%%', startangle=90)
    axes[1].set_title('Motivos de Cancelamento')
else:
    axes[1].text(0.5, 0.5, 'Sem dados de cancelamento\nna amostra', 
                ha='center', va='center', fontsize=14)
    axes[1].set_title('Motivos de Cancelamento')

plt.tight_layout()
plt.savefig(PLOTS_PATH / '07_cancelamentos.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 07_cancelamentos.png")

# %% ============================================================================
# 7. INSIGHTS E PADRÕES
# ============================================================================

print("\n" + "=" * 80)
print("7. PRINCIPAIS INSIGHTS")
print("=" * 80)

print("\n--- INSIGHTS GERAIS ---")
print(f"✓ Total de voos na amostra: {len(df_flights):,}")
print(f"✓ Taxa de atraso: {df_flights['IS_DELAYED'].mean()*100:.2f}%")
print(f"✓ Atraso médio (quando há atraso): {df_flights[df_flights['IS_DELAYED']==1]['ARRIVAL_DELAY'].mean():.2f} min")
print(f"✓ Taxa de cancelamento: {df_flights['CANCELLED'].mean()*100:.2f}%")
print(f"✓ Taxa de desvio: {df_flights['DIVERTED'].mean()*100:.2f}%")

print("\n--- PADRÕES TEMPORAIS ---")
print(f"✓ Mês com mais atrasos: {monthly_delays.idxmax()} (média de {monthly_delays.max():.2f} min)")
print(f"✓ Dia da semana com mais atrasos: {dow_delays.idxmax()} (média de {dow_delays.max():.2f} min)")
print(f"✓ Período com mais atrasos: {period_delays.idxmax()} (média de {period_delays.max():.2f} min)")

print("\n--- COMPANHIAS AÉREAS ---")
print(f"✓ Companhia com mais atrasos: {top_airlines_delay.idxmax()} ({top_airlines_delay.max():.2f} min)")
print(f"✓ Companhia com mais voos: {top_airlines_flights.idxmax()} ({top_airlines_flights.max():,} voos)")

print("\n--- AEROPORTOS ---")
print(f"✓ Aeroporto origem com mais atrasos: {top_origin_delay.idxmax()} ({top_origin_delay.max():.2f} min)")
print(f"✓ Aeroporto destino com mais atrasos: {top_dest_delay.idxmax()} ({top_dest_delay.max():.2f} min)")

print("\n--- CORRELAÇÕES ---")
print(f"✓ Correlação DEPARTURE_DELAY x ARRIVAL_DELAY: {correlation_matrix.loc['DEPARTURE_DELAY', 'ARRIVAL_DELAY']:.3f}")
print(f"✓ Correlação DISTANCE x ARRIVAL_DELAY: {correlation_matrix.loc['DISTANCE', 'ARRIVAL_DELAY']:.3f}")

# %% ============================================================================
# 8. SALVAR DADOS PROCESSADOS
# ============================================================================

print("\n" + "=" * 80)
print("8. SALVANDO DADOS PROCESSADOS")
print("=" * 80)

# Salvar amostra processada
df_flights.to_csv(PROCESSED_PATH / 'flights_sample_processed.csv', index=False)
print(f"✓ Salvo: flights_sample_processed.csv ({len(df_flights):,} registros)")

# Salvar estatísticas resumidas
summary_stats = {
    'total_flights': len(df_flights),
    'delay_rate': df_flights['IS_DELAYED'].mean(),
    'avg_delay_when_delayed': df_flights[df_flights['IS_DELAYED']==1]['ARRIVAL_DELAY'].mean(),
    'cancellation_rate': df_flights['CANCELLED'].mean(),
    'diversion_rate': df_flights['DIVERTED'].mean(),
    'worst_month': monthly_delays.idxmax(),
    'worst_day_of_week': dow_delays.idxmax(),
    'worst_airline': top_airlines_delay.idxmax(),
}

import json
with open(PROCESSED_PATH / 'eda_summary.json', 'w') as f:
    json.dump(summary_stats, f, indent=2)
print("✓ Salvo: eda_summary.json")

print("\n" + "=" * 80)
print("ANÁLISE EXPLORATÓRIA CONCLUÍDA!")
print("=" * 80)
print(f"\nVisualizações salvas em: {PLOTS_PATH}")
print(f"Dados processados em: {PROCESSED_PATH}")
print("\n✓ Próximos passos:")
print("  1. Revisar visualizações e insights")
print("  2. Feature engineering avançado")
print("  3. Modelagem supervisionada (classificação/regressão)")
print("  4. Modelagem não supervisionada (clustering)")
