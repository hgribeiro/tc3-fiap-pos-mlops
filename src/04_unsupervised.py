"""
Modelagem Não Supervisionada — Clustering de Rotas Aéreas
Task 02, Script 3: PCA + K-Means por rota

Input : data/processed/flights_sample_processed.csv
Output: data/processed/dashboard/ml_pca_*.json, ml_kmeans_*.json, ml_cluster_*.json
"""

# %% Imports
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
np.random.seed(42)

# %% Paths
DATA_RAW = Path("./data/processed/flights_sample_processed.csv")
DASH = Path("./data/processed/dashboard")
DASH.mkdir(parents=True, exist_ok=True)

# %% ============================================================================
# 1. CARREGAMENTO E PREPARAÇÃO DE FEATURES POR ROTA
# =============================================================================

print("=" * 80)
print("1. CARREGAMENTO E AGREGAÇÃO POR ROTA")
print("=" * 80)

df = pd.read_csv(DATA_RAW)

# Remover cancelados
df = df[df["CANCELLED"] != 1].copy()
df = df.dropna(subset=["IS_DELAYED"])
print(f"✓ Dataset: {df.shape}")

# Agregar por rota (ORIGIN_AIRPORT, DESTINATION_AIRPORT)
route_agg = df.groupby(["ORIGIN_AIRPORT", "DESTINATION_AIRPORT"]).agg(
    avg_distance=("DISTANCE", "mean"),
    avg_scheduled_time=("SCHEDULED_TIME", "mean"),
    avg_month=("MONTH", "mean"),
    avg_day_of_week=("DAY_OF_WEEK", "mean"),
    avg_scheduled_departure=("SCHEDULED_DEPARTURE", "mean"),
    avg_arrival_delay=("ARRIVAL_DELAY", "mean"),
    delay_rate=("IS_DELAYED", "mean"),
    flight_count=("IS_DELAYED", "count"),
).reset_index()

# Remover rotas com poucos voos (ruído)
min_flights = 5
route_agg = route_agg[route_agg["flight_count"] >= min_flights].reset_index(drop=True)
print(f"✓ Rotas com ≥ {min_flights} voos: {len(route_agg)}")

# Features para clustering (sem target direto — delay_rate é uma descrição da rota, não leakage)
cluster_features = [
    "avg_distance",
    "avg_scheduled_time",
    "avg_month",
    "avg_day_of_week",
    "avg_scheduled_departure",
    "avg_arrival_delay",
    "delay_rate",
    "flight_count",
]

X_routes = route_agg[cluster_features].copy()

# Tratar nulos restantes
X_routes = X_routes.fillna(X_routes.median())

# Escalonar
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_routes)

print(f"✓ Features de clustering: {cluster_features}")
print(f"✓ Shape: {X_scaled.shape}")

# %% ============================================================================
# 2. PCA — REDUÇÃO DE DIMENSIONALIDADE
# =============================================================================

print("\n" + "=" * 80)
print("2. PCA")
print("=" * 80)

pca_full = PCA(random_state=42)
pca_full.fit(X_scaled)

explained = pca_full.explained_variance_ratio_
cumulative = np.cumsum(explained)

# Componentes para ≥ 85% da variância
n_comp_85 = int(np.argmax(cumulative >= 0.85)) + 1
print(f"✓ Componentes para ≥ 85% variância: {n_comp_85}")
print(f"✓ Variância explicada (primeiras 3): {explained[:3].round(4)}")
print(f"✓ Variância acumulada (primeiras 3): {cumulative[:3].round(4)}")

# Loadings (contribuição de cada feature por componente)
loadings = {}
for i in range(min(len(cluster_features), len(pca_full.components_))):
    pc_name = f"PC{i+1}"
    loadings[pc_name] = {
        feat: round(float(pca_full.components_[i][j]), 4)
        for j, feat in enumerate(cluster_features)
    }

# Projetar em 2D para visualização
pca_2d = PCA(n_components=2, random_state=42)
coords_2d = pca_2d.fit_transform(X_scaled)
route_agg["PC1"] = coords_2d[:, 0]
route_agg["PC2"] = coords_2d[:, 1]

# JSON: ml_pca_variance.json
pca_json = {
    "n_components": int(len(explained)),
    "explained_variance_ratio": [round(float(v), 6) for v in explained],
    "cumulative_variance": [round(float(v), 6) for v in cumulative],
    "components_for_85pct": n_comp_85,
    "loadings": loadings,
}

with open(DASH / "ml_pca_variance.json", "w") as f:
    json.dump(pca_json, f, indent=2)
print("  ✓ ml_pca_variance.json")

# %% ============================================================================
# 3. K-MEANS — SELEÇÃO DE K
# =============================================================================

print("\n" + "=" * 80)
print("3. K-MEANS — SELEÇÃO DE K")
print("=" * 80)

# Usar PCA com n_comp_85 componentes para clustering
pca_cluster = PCA(n_components=n_comp_85, random_state=42)
X_pca = pca_cluster.fit_transform(X_scaled)

k_range = range(2, 11)
inertias = []
silhouettes = []

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
    labels = km.fit_predict(X_pca)
    inertias.append(float(km.inertia_))
    sil = silhouette_score(X_pca, labels)
    silhouettes.append(round(float(sil), 4))
    print(f"  K={k:>2}: inertia={km.inertia_:>12,.1f}  silhouette={sil:.4f}")

# Escolher K ótimo — max silhouette
best_k_idx = int(np.argmax(silhouettes))
chosen_k = list(k_range)[best_k_idx]
print(f"\n  ★ K ótimo selecionado: {chosen_k} (silhouette = {silhouettes[best_k_idx]:.4f})")

# JSON: ml_kmeans_elbow.json
elbow_json = {
    "k_values": list(k_range),
    "inertia": [round(v, 2) for v in inertias],
    "silhouette": silhouettes,
    "chosen_k": chosen_k,
    "choice_reason": f"Silhouette máximo em K={chosen_k} ({silhouettes[best_k_idx]:.4f})",
}

with open(DASH / "ml_kmeans_elbow.json", "w") as f:
    json.dump(elbow_json, f, indent=2)
print("  ✓ ml_kmeans_elbow.json")

# %% ============================================================================
# 4. K-MEANS FINAL + ATRIBUIÇÃO DE CLUSTERS
# =============================================================================

print("\n" + "=" * 80)
print("4. K-MEANS FINAL")
print("=" * 80)

km_final = KMeans(n_clusters=chosen_k, random_state=42, n_init=10, max_iter=300)
route_agg["cluster_id"] = km_final.fit_predict(X_pca)

print(f"✓ Clusters atribuídos: {route_agg['cluster_id'].value_counts().to_dict()}")

# %% ============================================================================
# 5. PERFIL DOS CLUSTERS
# =============================================================================

print("\n" + "=" * 80)
print("5. PERFIL DOS CLUSTERS")
print("=" * 80)

# Para obter top airlines por cluster, precisamos do df original com cluster labels
# Mapear cluster_id de volta para as rotas no df original
route_cluster_map = route_agg.set_index(["ORIGIN_AIRPORT", "DESTINATION_AIRPORT"])["cluster_id"].to_dict()
df["cluster_id"] = df.apply(
    lambda r: route_cluster_map.get((r["ORIGIN_AIRPORT"], r["DESTINATION_AIRPORT"]), -1),
    axis=1,
)

cluster_profiles = []
for cid in sorted(route_agg["cluster_id"].unique()):
    mask = route_agg["cluster_id"] == cid
    cluster_routes = route_agg[mask]
    cluster_flights = df[df["cluster_id"] == cid]

    n_routes = int(mask.sum())
    n_flights = int(cluster_routes["flight_count"].sum())

    avg_dist = round(float(cluster_routes["avg_distance"].mean()), 1)
    std_dist = round(float(cluster_routes["avg_distance"].std()), 1) if n_routes > 1 else 0.0
    avg_delay_rate = round(float(cluster_routes["delay_rate"].mean()), 3)
    std_delay_rate = round(float(cluster_routes["delay_rate"].std()), 3) if n_routes > 1 else 0.0
    avg_arr_delay = round(float(cluster_routes["avg_arrival_delay"].mean()), 1)
    std_arr_delay = round(float(cluster_routes["avg_arrival_delay"].std()), 1) if n_routes > 1 else 0.0
    avg_fc = round(float(cluster_routes["flight_count"].mean()), 1)
    std_fc = round(float(cluster_routes["flight_count"].std()), 1) if n_routes > 1 else 0.0

    top_airlines = (
        cluster_flights["AIRLINE"]
        .value_counts()
        .head(3)
        .index.tolist()
    )
    top_origins = (
        cluster_flights["ORIGIN_AIRPORT"]
        .value_counts()
        .head(3)
        .index.tolist()
    )

    # Gerar label interpretativo em português
    if avg_dist < 600 and avg_delay_rate < 0.40:
        label = "Rotas Curtas Pontuais"
    elif avg_dist < 600 and avg_delay_rate >= 0.40:
        label = "Rotas Curtas com Atrasos"
    elif avg_dist >= 600 and avg_dist < 1500 and avg_delay_rate < 0.40:
        label = "Rotas Médias Pontuais"
    elif avg_dist >= 600 and avg_dist < 1500 and avg_delay_rate >= 0.40:
        label = "Rotas Médias com Atrasos"
    elif avg_dist >= 1500 and avg_delay_rate < 0.40:
        label = "Rotas Longas Pontuais"
    elif avg_dist >= 1500 and avg_delay_rate >= 0.40:
        label = "Rotas Longas com Atrasos"
    elif avg_fc > 200:
        label = "Hubs Congestionados"
    else:
        label = f"Cluster {cid}"

    profile = {
        "id": int(cid),
        "label": label,
        "n_routes": n_routes,
        "n_flights": n_flights,
        "avg_distance": avg_dist,
        "std_distance": std_dist,
        "avg_delay_rate": avg_delay_rate,
        "std_delay_rate": std_delay_rate,
        "avg_arrival_delay": avg_arr_delay,
        "std_arrival_delay": std_arr_delay,
        "avg_flight_count": avg_fc,
        "std_flight_count": std_fc,
        "top_airlines": [str(a) for a in top_airlines],
        "top_origins": [str(o) for o in top_origins],
    }
    cluster_profiles.append(profile)
    print(f"\n  Cluster {cid} — \"{label}\":")
    print(f"    Rotas: {n_routes}, Voos: {n_flights:,}")
    print(f"    Distância média: {avg_dist:.0f}, Delay rate: {avg_delay_rate:.3f}")
    print(f"    Top airlines: {top_airlines}")

# JSON: ml_cluster_profiles.json
profiles_json = {
    "n_clusters": chosen_k,
    "clusters": cluster_profiles,
}

with open(DASH / "ml_cluster_profiles.json", "w") as f:
    json.dump(profiles_json, f, indent=2)
print("\n  ✓ ml_cluster_profiles.json")

# %% ============================================================================
# 6. JSONs — SCATTER E ROTAS
# =============================================================================

print("\n" + "=" * 80)
print("6. JSONs FINAIS")
print("=" * 80)

# ml_pca_scatter.json — coordenadas PC1/PC2 com cluster label
# Limitar a 2000 pontos para o dashboard
scatter_sample = route_agg.sample(n=min(2000, len(route_agg)), random_state=42)

scatter_json = {
    "n_points": len(scatter_sample),
    "PC1": [round(float(v), 4) for v in scatter_sample["PC1"]],
    "PC2": [round(float(v), 4) for v in scatter_sample["PC2"]],
    "cluster_id": scatter_sample["cluster_id"].tolist(),
    "labels": {p["id"]: p["label"] for p in cluster_profiles},
}

with open(DASH / "ml_pca_scatter.json", "w") as f:
    json.dump(scatter_json, f, indent=2)
print("  ✓ ml_pca_scatter.json")

# ml_cluster_routes.json — rotas com cluster_id, PC1, PC2, delay_rate
routes_sample = route_agg.sample(n=min(3000, len(route_agg)), random_state=42)
routes_json = {
    "columns": ["ORIGIN_AIRPORT", "DESTINATION_AIRPORT", "cluster_id",
                 "PC1", "PC2", "delay_rate", "avg_distance", "flight_count"],
    "data": [],
}

for _, row in routes_sample.iterrows():
    routes_json["data"].append([
        str(row["ORIGIN_AIRPORT"]),
        str(row["DESTINATION_AIRPORT"]),
        int(row["cluster_id"]),
        round(float(row["PC1"]), 4),
        round(float(row["PC2"]), 4),
        round(float(row["delay_rate"]), 4),
        round(float(row["avg_distance"]), 1),
        int(row["flight_count"]),
    ])

with open(DASH / "ml_cluster_routes.json", "w") as f:
    json.dump(routes_json, f, indent=2)
print("  ✓ ml_cluster_routes.json")

print("\n" + "=" * 80)
print("MODELAGEM NÃO SUPERVISIONADA CONCLUÍDA!")
print("=" * 80)
