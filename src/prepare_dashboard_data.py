"""
Prepara dados agregados em JSON para o dashboard frontend.
Lê o CSV processado e gera arquivos JSON compactos.
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA_PATH = Path('./data')
PROCESSED_PATH = DATA_PATH / 'processed'
DASHBOARD_PATH = PROCESSED_PATH / 'dashboard'
DASHBOARD_PATH.mkdir(parents=True, exist_ok=True)

print("Carregando flights_sample_processed.csv...")
df = pd.read_csv(PROCESSED_PATH / 'flights_sample_processed.csv')
print(f"✓ Carregado: {df.shape}")

# Carregar datasets auxiliares
df_airlines = pd.read_csv(DATA_PATH / 'airlines.csv')
df_airports = pd.read_csv(DATA_PATH / 'airports.csv')

# Mapas de nomes
airline_names = dict(zip(df_airlines['IATA_CODE'], df_airlines['AIRLINE']))
airport_names = dict(zip(df_airports['IATA_CODE'], df_airports['AIRPORT']))

# ============================================================================
# 1. KPIs
# ============================================================================
print("Gerando KPIs...")
kpis = {
    "total_flights": int(len(df)),
    "delay_rate": round(float((df['ARRIVAL_DELAY'] > 0).mean() * 100), 2),
    "avg_delay_minutes": round(float(df.loc[df['ARRIVAL_DELAY'] > 0, 'ARRIVAL_DELAY'].mean()), 1),
    "cancellation_rate": round(float(df['CANCELLED'].mean() * 100), 2),
    "diversion_rate": round(float(df['DIVERTED'].mean() * 100), 2),
    "total_airlines": int(df['AIRLINE'].nunique()),
    "total_airports": int(pd.concat([df['ORIGIN_AIRPORT'], df['DESTINATION_AIRPORT']]).nunique()),
    "avg_distance": round(float(df['DISTANCE'].mean()), 0),
    "median_delay": round(float(df.loc[df['ARRIVAL_DELAY'] > 0, 'ARRIVAL_DELAY'].median()), 1),
}

with open(DASHBOARD_PATH / 'dashboard_kpis.json', 'w') as f:
    json.dump(kpis, f, indent=2)
print("  ✓ dashboard_kpis.json")

# ============================================================================
# 2. Distribuição de Atrasos
# ============================================================================
print("Gerando distribuição de atrasos...")

# Histograma de arrival delay (bins de 10 min, de -60 a 200)
delays = df['ARRIVAL_DELAY'].dropna()
bins = list(range(-60, 210, 10))
hist_values, bin_edges = np.histogram(delays.clip(-60, 200), bins=bins)
delay_distribution = {
    "histogram": {
        "labels": [f"{int(bins[i])} to {int(bins[i+1])}" for i in range(len(bins)-1)],
        "values": [int(v) for v in hist_values],
        "bin_edges": [int(b) for b in bin_edges],
    },
    "categories": {},
    "stats": {
        "mean": round(float(delays.mean()), 2),
        "median": round(float(delays.median()), 2),
        "std": round(float(delays.std()), 2),
        "min": round(float(delays.min()), 2),
        "max": round(float(delays.max()), 2),
        "q25": round(float(delays.quantile(0.25)), 2),
        "q75": round(float(delays.quantile(0.75)), 2),
    }
}

# Categorias de atraso
if 'DELAY_CATEGORY' in df.columns:
    cat_counts = df['DELAY_CATEGORY'].value_counts()
    delay_distribution["categories"] = {
        "labels": cat_counts.index.tolist(),
        "values": [int(v) for v in cat_counts.values],
    }
else:
    def categorize_delay(delay):
        if pd.isna(delay): return 'Unknown'
        elif delay <= 0: return 'On Time'
        elif delay <= 15: return 'Minor Delay'
        elif delay <= 60: return 'Moderate Delay'
        else: return 'Major Delay'
    cats = df['ARRIVAL_DELAY'].apply(categorize_delay).value_counts()
    delay_distribution["categories"] = {
        "labels": cats.index.tolist(),
        "values": [int(v) for v in cats.values],
    }

with open(DASHBOARD_PATH / 'dashboard_delay_distribution.json', 'w') as f:
    json.dump(delay_distribution, f, indent=2)
print("  ✓ dashboard_delay_distribution.json")

# ============================================================================
# 3. Análise Temporal
# ============================================================================
print("Gerando análise temporal...")

month_names = {
    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
    7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
}
dow_names = {1: 'Seg', 2: 'Ter', 3: 'Qua', 4: 'Qui', 5: 'Sex', 6: 'Sáb', 7: 'Dom'}

monthly_delay = df.groupby('MONTH')['ARRIVAL_DELAY'].mean()
monthly_rate = (df.groupby('MONTH')['ARRIVAL_DELAY'].apply(lambda x: (x > 0).mean()) * 100)
monthly_count = df.groupby('MONTH').size()

dow_delay = df.groupby('DAY_OF_WEEK')['ARRIVAL_DELAY'].mean()
dow_rate = (df.groupby('DAY_OF_WEEK')['ARRIVAL_DELAY'].apply(lambda x: (x > 0).mean()) * 100)
dow_count = df.groupby('DAY_OF_WEEK').size()

# Período do dia
if 'DEPARTURE_PERIOD' in df.columns:
    period_col = 'DEPARTURE_PERIOD'
else:
    def get_time_period(hour):
        if pd.isna(hour): return 'Unknown'
        hour = int(hour / 100)
        if 5 <= hour < 12: return 'Morning'
        elif 12 <= hour < 17: return 'Afternoon'
        elif 17 <= hour < 21: return 'Evening'
        else: return 'Night'
    df['DEPARTURE_PERIOD'] = df['SCHEDULED_DEPARTURE'].apply(get_time_period)
    period_col = 'DEPARTURE_PERIOD'

period_delay = df.groupby(period_col)['ARRIVAL_DELAY'].mean()
period_rate = (df.groupby(period_col)['ARRIVAL_DELAY'].apply(lambda x: (x > 0).mean()) * 100)
period_count = df.groupby(period_col).size()

temporal = {
    "monthly": {
        "labels": [month_names.get(m, str(m)) for m in sorted(monthly_delay.index)],
        "avg_delay": [round(float(monthly_delay[m]), 2) for m in sorted(monthly_delay.index)],
        "delay_rate": [round(float(monthly_rate[m]), 2) for m in sorted(monthly_rate.index)],
        "flight_count": [int(monthly_count[m]) for m in sorted(monthly_count.index)],
    },
    "day_of_week": {
        "labels": [dow_names.get(d, str(d)) for d in sorted(dow_delay.index)],
        "avg_delay": [round(float(dow_delay[d]), 2) for d in sorted(dow_delay.index)],
        "delay_rate": [round(float(dow_rate[d]), 2) for d in sorted(dow_rate.index)],
        "flight_count": [int(dow_count[d]) for d in sorted(dow_count.index)],
    },
    "period": {
        "labels": period_delay.sort_values().index.tolist(),
        "avg_delay": [round(float(period_delay[p]), 2) for p in period_delay.sort_values().index],
        "delay_rate": [round(float(period_rate[p]), 2) for p in period_delay.sort_values().index],
        "flight_count": [int(period_count[p]) for p in period_delay.sort_values().index],
    },
}

with open(DASHBOARD_PATH / 'dashboard_temporal.json', 'w') as f:
    json.dump(temporal, f, indent=2)
print("  ✓ dashboard_temporal.json")

# ============================================================================
# 4. Companhias Aéreas
# ============================================================================
print("Gerando análise de companhias aéreas...")

airline_stats = df.groupby('AIRLINE').agg(
    avg_delay=('ARRIVAL_DELAY', 'mean'),
    delay_rate=('ARRIVAL_DELAY', lambda x: (x > 0).mean() * 100),
    flight_count=('AIRLINE', 'size'),
    avg_distance=('DISTANCE', 'mean'),
    cancel_rate=('CANCELLED', 'mean'),
).reset_index()

airline_stats['airline_name'] = airline_stats['AIRLINE'].map(airline_names).fillna(airline_stats['AIRLINE'])

# Top 14 por volume de voos
top_by_volume = airline_stats.nlargest(14, 'flight_count')
# Ordenar por atraso médio
top_by_delay = airline_stats.nlargest(14, 'avg_delay')

airlines_data = {
    "by_delay": {
        "labels": top_by_delay['AIRLINE'].tolist(),
        "names": top_by_delay['airline_name'].tolist(),
        "avg_delay": [round(float(v), 2) for v in top_by_delay['avg_delay']],
        "delay_rate": [round(float(v), 2) for v in top_by_delay['delay_rate']],
        "flight_count": [int(v) for v in top_by_delay['flight_count']],
    },
    "by_volume": {
        "labels": top_by_volume['AIRLINE'].tolist(),
        "names": top_by_volume['airline_name'].tolist(),
        "avg_delay": [round(float(v), 2) for v in top_by_volume['avg_delay']],
        "delay_rate": [round(float(v), 2) for v in top_by_volume['delay_rate']],
        "flight_count": [int(v) for v in top_by_volume['flight_count']],
    },
}

with open(DASHBOARD_PATH / 'dashboard_airlines.json', 'w') as f:
    json.dump(airlines_data, f, indent=2)
print("  ✓ dashboard_airlines.json")

# ============================================================================
# 5. Aeroportos
# ============================================================================
print("Gerando análise de aeroportos...")

# Filtrar aeroportos IATA (3 letras)
iata_mask_origin = df['ORIGIN_AIRPORT'].astype(str).str.match(r'^[A-Z]{3}$')
iata_mask_dest = df['DESTINATION_AIRPORT'].astype(str).str.match(r'^[A-Z]{3}$')

origin_stats = df[iata_mask_origin].groupby('ORIGIN_AIRPORT').agg(
    avg_departure_delay=('DEPARTURE_DELAY', 'mean'),
    flight_count=('ORIGIN_AIRPORT', 'size'),
).reset_index()
origin_stats['airport_name'] = origin_stats['ORIGIN_AIRPORT'].map(airport_names).fillna(origin_stats['ORIGIN_AIRPORT'])

dest_stats = df[iata_mask_dest].groupby('DESTINATION_AIRPORT').agg(
    avg_arrival_delay=('ARRIVAL_DELAY', 'mean'),
    flight_count=('DESTINATION_AIRPORT', 'size'),
).reset_index()
dest_stats['airport_name'] = dest_stats['DESTINATION_AIRPORT'].map(airport_names).fillna(dest_stats['DESTINATION_AIRPORT'])

top_origin = origin_stats.nlargest(10, 'avg_departure_delay')
top_dest = dest_stats.nlargest(10, 'avg_arrival_delay')

# Top por volume
top_origin_vol = origin_stats.nlargest(10, 'flight_count')
top_dest_vol = dest_stats.nlargest(10, 'flight_count')

airports_data = {
    "top_origin_delay": {
        "labels": top_origin['ORIGIN_AIRPORT'].tolist(),
        "names": top_origin['airport_name'].tolist(),
        "avg_delay": [round(float(v), 2) for v in top_origin['avg_departure_delay']],
        "flight_count": [int(v) for v in top_origin['flight_count']],
    },
    "top_dest_delay": {
        "labels": top_dest['DESTINATION_AIRPORT'].tolist(),
        "names": top_dest['airport_name'].tolist(),
        "avg_delay": [round(float(v), 2) for v in top_dest['avg_arrival_delay']],
        "flight_count": [int(v) for v in top_dest['flight_count']],
    },
    "top_origin_volume": {
        "labels": top_origin_vol['ORIGIN_AIRPORT'].tolist(),
        "names": top_origin_vol['airport_name'].tolist(),
        "avg_delay": [round(float(v), 2) for v in top_origin_vol['avg_departure_delay']],
        "flight_count": [int(v) for v in top_origin_vol['flight_count']],
    },
    "top_dest_volume": {
        "labels": top_dest_vol['DESTINATION_AIRPORT'].tolist(),
        "names": top_dest_vol['airport_name'].tolist(),
        "avg_delay": [round(float(v), 2) for v in top_dest_vol['avg_arrival_delay']],
        "flight_count": [int(v) for v in top_dest_vol['flight_count']],
    },
}

with open(DASHBOARD_PATH / 'dashboard_airports.json', 'w') as f:
    json.dump(airports_data, f, indent=2)
print("  ✓ dashboard_airports.json")

# ============================================================================
# 6. Correlação
# ============================================================================
print("Gerando matriz de correlação...")

numeric_cols = ['DEPARTURE_DELAY', 'ARRIVAL_DELAY', 'AIR_TIME', 'DISTANCE',
                'TAXI_OUT', 'TAXI_IN', 'ELAPSED_TIME']
corr = df[numeric_cols].corr()

correlation_data = {
    "labels": numeric_cols,
    "matrix": [[round(float(corr.iloc[i, j]), 3) for j in range(len(numeric_cols))] for i in range(len(numeric_cols))],
}

with open(DASHBOARD_PATH / 'dashboard_correlation.json', 'w') as f:
    json.dump(correlation_data, f, indent=2)
print("  ✓ dashboard_correlation.json")

# ============================================================================
# 7. Cancelamentos
# ============================================================================
print("Gerando análise de cancelamentos...")

cancel_rate = round(float(df['CANCELLED'].mean() * 100), 3)
divert_rate = round(float(df['DIVERTED'].mean() * 100), 3)

cancel_reasons_map = {'A': 'Airline/Carrier', 'B': 'Weather', 'C': 'NAS', 'D': 'Security'}
cancel_reasons = df['CANCELLATION_REASON'].dropna().map(cancel_reasons_map).value_counts()

# Cancelamentos por mês
monthly_cancel = (df.groupby('MONTH')['CANCELLED'].mean() * 100)

# Tipos de atraso (quando há atraso)
delay_type_cols = ['AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']
delay_types_sum = df[delay_type_cols].sum()

cancellations_data = {
    "cancel_rate": cancel_rate,
    "divert_rate": divert_rate,
    "reasons": {
        "labels": cancel_reasons.index.tolist() if len(cancel_reasons) > 0 else ["No data"],
        "values": [int(v) for v in cancel_reasons.values] if len(cancel_reasons) > 0 else [0],
    },
    "monthly_cancel_rate": {
        "labels": [month_names.get(m, str(m)) for m in sorted(monthly_cancel.index)],
        "values": [round(float(monthly_cancel[m]), 3) for m in sorted(monthly_cancel.index)],
    },
    "delay_types": {
        "labels": ['Air System', 'Security', 'Airline', 'Late Aircraft', 'Weather'],
        "values": [round(float(v), 0) for v in delay_types_sum],
    },
}

with open(DASHBOARD_PATH / 'dashboard_cancellations.json', 'w') as f:
    json.dump(cancellations_data, f, indent=2)
print("  ✓ dashboard_cancellations.json")

print("\n✓ Todos os dados do dashboard foram gerados em:", DASHBOARD_PATH)
