"""
Feature Engineering — Flight Delay Prediction
Task 03: Encoding, splitting e escalonamento sem data leakage

Input : data/processed/flights_sample_processed.csv
Output: data/processed/{X,y}_{train,val,test}.parquet
        models/scaler.pkl
        models/encoders.json

Critérios de Sucesso (task03.md):
  ✓ Sem data leakage (features pré-voo apenas)
  ✓ IS_DELAYED = ARRIVAL_DELAY > 15 min
  ✓ Split estratificado 70/15/15
  ✓ Target Encoding calculado apenas no treino
  ✓ StandardScaler fit apenas no treino
  ✓ encoders.json com mapeamentos completos para inferência
"""

# ── Imports ────────────────────────────────────────────────────────────────────
import json
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
np.random.seed(42)

SCRIPT_START = time.time()

# ── Paths ──────────────────────────────────────────────────────────────────────
DATA_RAW  = Path("./data/processed/flights_sample_processed.csv")
OUT_DIR   = Path("./data/processed")
MODEL_DIR = Path("./models")
OUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# ── Feature lists ──────────────────────────────────────────────────────────────
FEATURES_NUM = [
    "MONTH",
    "DAY_OF_WEEK",
    "SCHEDULED_DEPARTURE",
    "SCHEDULED_ARRIVAL",
    "DISTANCE",
    "SCHEDULED_TIME",
]

FEATURES_CAT_TARGET_ENC = ["AIRLINE", "ORIGIN_AIRPORT", "DESTINATION_AIRPORT"]
FEATURES_CAT_OHE        = ["DEPARTURE_PERIOD"]
TARGET                  = "IS_DELAYED"

# Colunas com risco de data leakage — jamais devem aparecer nas features
LEAKAGE_COLS = [
    "DEPARTURE_DELAY", "ARRIVAL_DELAY", "TAXI_OUT", "TAXI_IN",
    "AIR_TIME", "ELAPSED_TIME", "WHEELS_OFF", "WHEELS_ON",
    "DEPARTURE_TIME", "ARRIVAL_TIME",
]


def _elapsed(start: float) -> str:
    return f"{time.time() - start:.1f}s"


# ==============================================================================
# 1. CARREGAMENTO E SELEÇÃO
# ==============================================================================
_t = time.time()
print("=" * 80)
print("1. CARREGAMENTO E SELEÇÃO DE FEATURES")
print("=" * 80)

df = pd.read_csv(DATA_RAW)
print(f"✓ Dataset carregado: {df.shape}  [{_elapsed(_t)}]")

# Remover voos cancelados (não decolaram — não é atraso)
n_before = len(df)
df = df[df["CANCELLED"] != 1].copy()
print(f"✓ Removidos {n_before - len(df):,} voos cancelados → {len(df):,} restantes")

# Recalcular IS_DELAYED com threshold correto: > 15 min  (task03.md §1)
# (01_eda.py usa > 0 — corrigimos aqui para seguir a definição de negócio)
if "ARRIVAL_DELAY" in df.columns:
    df[TARGET] = (df["ARRIVAL_DELAY"] > 15).astype("Int8")
    print("✓ IS_DELAYED recalculado: ARRIVAL_DELAY > 15 min  (threshold correto)")

# Remover linhas sem target
n_before = len(df)
df = df.dropna(subset=[TARGET])
print(f"✓ Removidos {n_before - len(df):,} sem IS_DELAYED → {len(df):,} restantes")

# ── Guarda anti-leakage ────────────────────────────────────────────────────────
leakage_present = [c for c in LEAKAGE_COLS if c in df.columns]
all_feats = FEATURES_NUM + FEATURES_CAT_TARGET_ENC + FEATURES_CAT_OHE
forbidden_in_feats = [c for c in leakage_present if c in all_feats]
if forbidden_in_feats:
    raise ValueError(
        f"⛔ DATA LEAKAGE DETECTADO! Colunas proibidas na lista de features: "
        f"{forbidden_in_feats}"
    )
print(f"✓ Leakage guard OK — colunas proibidas ({len(leakage_present)}) não estão nas features")

# Garantir que DEPARTURE_PERIOD exista (derivado de SCHEDULED_DEPARTURE)
if "DEPARTURE_PERIOD" not in df.columns:
    def _period(h):
        if pd.isna(h):
            return "Unknown"
        h = int(h) // 100
        if   5 <= h < 12: return "Morning"
        elif 12 <= h < 17: return "Afternoon"
        elif 17 <= h < 21: return "Evening"
        return "Night"
    df["DEPARTURE_PERIOD"] = df["SCHEDULED_DEPARTURE"].apply(_period)
    print("✓ DEPARTURE_PERIOD derivado de SCHEDULED_DEPARTURE")

X = df[all_feats].copy()
y = df[TARGET].astype(int).copy()

print(f"\n✓ Features selecionadas ({len(all_feats)}): {all_feats}")
print(f"✓ Target: {TARGET}  — distribuição global:\n"
      f"     0 (pontual): {(y == 0).sum():>8,}  ({(y == 0).mean()*100:.1f}%)\n"
      f"     1 (atrasado): {(y == 1).sum():>7,}  ({(y == 1).mean()*100:.1f}%)")

# ==============================================================================
# 2. TRATAMENTO DE NULOS CATEGÓRICOS  (antes do split — valor fixo 'UNKNOWN')
# ==============================================================================
print("\n" + "=" * 80)
print("2. TRATAMENTO DE NULOS CATEGÓRICOS")
print("=" * 80)

for col in FEATURES_CAT_TARGET_ENC + FEATURES_CAT_OHE:
    n_miss = X[col].isna().sum()
    if n_miss > 0:
        X[col] = X[col].fillna("UNKNOWN")
        print(f"  {col}: {n_miss:,} nulos → 'UNKNOWN'")

print("✓ Nulos categóricos tratados")

# ==============================================================================
# 3. SPLIT ESTRATIFICADO  (70 / 15 / 15)
# ==============================================================================
print("\n" + "=" * 80)
print("3. SPLIT ESTRATIFICADO  70% / 15% / 15%")
print("=" * 80)

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=42
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42
)

# Reset de índices para evitar problemas de alinhamento nas etapas seguintes
X_train = X_train.reset_index(drop=True)
X_val   = X_val.reset_index(drop=True)
X_test  = X_test.reset_index(drop=True)
y_train = y_train.reset_index(drop=True)
y_val   = y_val.reset_index(drop=True)
y_test  = y_test.reset_index(drop=True)

print(f"  {'Split':<12} {'Amostras':>10}  {'IS_DELAYED=1':>14}")
print(f"  {'-'*40}")
for name, ys in [("Treino", y_train), ("Validação", y_val), ("Teste", y_test)]:
    pct = ys.mean() * 100
    print(f"  {name:<12} {len(ys):>10,}  {pct:>13.2f}%")

# ── Verificar desbalanceamento ─────────────────────────────────────────────────
delay_rate = y_train.mean()
if delay_rate < 0.30 or delay_rate > 0.70:
    print(
        f"\n  ⚠️  DESBALANCEAMENTO DETECTADO (IS_DELAYED=1: {delay_rate*100:.1f}%)\n"
        f"     → Recomendado: usar class_weight='balanced' nos modelos."
    )
else:
    print(f"\n  ✓ Classes balanceadas no treino (IS_DELAYED=1: {delay_rate*100:.1f}%)")

# ==============================================================================
# 4. IMPUTAÇÃO DE NULOS NUMÉRICOS  (mediana do TREINO apenas)
# ==============================================================================
print("\n" + "=" * 80)
print("4. IMPUTAÇÃO DE NULOS NUMÉRICOS  (mediana do treino)")
print("=" * 80)

medians: dict = {}
for col in FEATURES_NUM:
    n_miss_train = X_train[col].isna().sum()
    if n_miss_train > 0 or X_val[col].isna().sum() > 0 or X_test[col].isna().sum() > 0:
        med = float(X_train[col].median())
        medians[col] = med
        X_train[col] = X_train[col].fillna(med)
        X_val[col]   = X_val[col].fillna(med)
        X_test[col]  = X_test[col].fillna(med)
        print(f"  {col}: mediana = {med:.4f}  (nulos no treino: {n_miss_train:,})")

if not medians:
    print("  ✓ Sem nulos numéricos — imputação não necessária")
print("✓ Imputação de nulos numéricos concluída")

# ==============================================================================
# 5. ENCODING  (usando somente dados de TREINO)
# ==============================================================================
print("\n" + "=" * 80)
print("5. ENCODING")
print("=" * 80)

encoders: dict = {
    "__version__": "1.0",
    "__created_at__": datetime.now(timezone.utc).isoformat(),
    "target_encoding": {},
    "ohe_columns": [],
    "medians": medians,
    "feature_columns": [],    # preenchido após OHE
    "leakage_guard": LEAKAGE_COLS,
}

# 5.1 Target Encoding — AIRLINE, ORIGIN_AIRPORT, DESTINATION_AIRPORT
for col in FEATURES_CAT_TARGET_ENC:
    # Calcular mapeamento somente no treino
    train_tmp = pd.concat([X_train[[col]], y_train.rename(TARGET)], axis=1)
    mapping = train_tmp.groupby(col)[TARGET].mean().to_dict()
    global_mean = float(y_train.mean())

    # Aplicar via map (unseen → global_mean via fillna)
    X_train[col] = X_train[col].map(mapping).fillna(global_mean)
    X_val[col]   = X_val[col].map(mapping).fillna(global_mean)
    X_test[col]  = X_test[col].map(mapping).fillna(global_mean)

    encoders["target_encoding"][col] = {
        str(k): float(v) for k, v in mapping.items()
    }
    encoders["target_encoding"][col]["__global_mean__"] = global_mean

    print(f"  ✓ Target Encoding: {col} → {len(mapping):,} categorias  "
          f"(global_mean = {global_mean:.4f})")

# 5.2 One-Hot Encoding para DEPARTURE_PERIOD
ohe_train = pd.get_dummies(X_train["DEPARTURE_PERIOD"], prefix="PERIOD")
ohe_val   = pd.get_dummies(X_val["DEPARTURE_PERIOD"],   prefix="PERIOD")
ohe_test  = pd.get_dummies(X_test["DEPARTURE_PERIOD"],  prefix="PERIOD")

# Garantir colunas consistentes em todos os splits  &  cast para int
ohe_cols = sorted(ohe_train.columns.tolist())
for split_ohe in [ohe_train, ohe_val, ohe_test]:
    for c in ohe_cols:
        if c not in split_ohe.columns:
            split_ohe[c] = 0
ohe_train = ohe_train[ohe_cols].astype(int)
ohe_val   = ohe_val[ohe_cols].astype(int)
ohe_test  = ohe_test[ohe_cols].astype(int)

encoders["ohe_columns"] = ohe_cols

# Substituir coluna original pelas dummies
X_train = pd.concat([X_train.drop(columns=["DEPARTURE_PERIOD"]), ohe_train], axis=1)
X_val   = pd.concat([X_val.drop(columns=["DEPARTURE_PERIOD"]),   ohe_val],   axis=1)
X_test  = pd.concat([X_test.drop(columns=["DEPARTURE_PERIOD"]),  ohe_test],  axis=1)

print(f"  ✓ OHE: DEPARTURE_PERIOD → {ohe_cols}")
print(f"\n✓ Shapes após encoding:")
print(f"    X_train: {X_train.shape}  |  X_val: {X_val.shape}  |  X_test: {X_test.shape}")

# ==============================================================================
# 6. ESCALONAMENTO  (StandardScaler — fit apenas no treino)
# ==============================================================================
print("\n" + "=" * 80)
print("6. ESCALONAMENTO  (StandardScaler)")
print("=" * 80)

scaler = StandardScaler()
X_train_scaled = pd.DataFrame(
    scaler.fit_transform(X_train), columns=X_train.columns
)
X_val_scaled = pd.DataFrame(
    scaler.transform(X_val), columns=X_val.columns
)
X_test_scaled = pd.DataFrame(
    scaler.transform(X_test), columns=X_test.columns
)

joblib.dump(scaler, MODEL_DIR / "scaler.pkl")
print(f"✓ StandardScaler salvo: {MODEL_DIR / 'scaler.pkl'}")
print(f"  Média (primeiras 4 features): {scaler.mean_[:4].round(4).tolist()}")

# ==============================================================================
# 7. SALVANDO OUTPUTS  (parquets + artefatos)
# ==============================================================================
print("\n" + "=" * 80)
print("7. SALVANDO OUTPUTS")
print("=" * 80)

# Parquets de features
splits = {
    "X_train": X_train_scaled,
    "X_val":   X_val_scaled,
    "X_test":  X_test_scaled,
}
for name, df_out in splits.items():
    path = OUT_DIR / f"{name}.parquet"
    df_out.to_parquet(path, index=False)

# Parquets de target
targets = {
    "y_train": y_train,
    "y_val":   y_val,
    "y_test":  y_test,
}
for name, s_out in targets.items():
    path = OUT_DIR / f"{name}.parquet"
    s_out.to_frame().to_parquet(path, index=False)

# encoders.json — salvo UMA única vez com todos os campos
encoders["feature_columns"] = X_train_scaled.columns.tolist()
with open(MODEL_DIR / "encoders.json", "w") as f:
    json.dump(encoders, f, indent=2, ensure_ascii=False)

print("✓ Arquivos gerados:")
all_outputs = (
    [OUT_DIR / f"{n}.parquet" for n in list(splits) + list(targets)]
    + [MODEL_DIR / "scaler.pkl", MODEL_DIR / "encoders.json"]
)
for p in all_outputs:
    size_kb = p.stat().st_size / 1024
    unit = "KB" if size_kb < 1024 else "MB"
    size_disp = size_kb if size_kb < 1024 else size_kb / 1024
    print(f"    {str(p):<50}  {size_disp:>7.1f} {unit}")

# ==============================================================================
# SUMÁRIO FINAL
# ==============================================================================
print("\n" + "=" * 80)
total = time.time() - SCRIPT_START
print(f"FEATURE ENGINEERING CONCLUÍDO!  ({total:.1f}s total)")
print("=" * 80)

print("\n📋 Critérios de Sucesso (task03.md):")
print(f"  ✅ Sem data leakage     — {len(all_feats)} features pré-voo apenas")
print(f"  ✅ IS_DELAYED correto   — threshold > 15 min")
print(f"  ✅ Split estratificado  — 70% / 15% / 15%  (random_state=42)")
print(f"  ✅ Target Encoding      — calculado no treino, aplicado a val/teste")
print(f"  ✅ OHE consistente      — {len(ohe_cols)} colunas inteiras em todos splits")
print(f"  ✅ Scaler               — fit no treino, transform em val/teste")
print(f"  ✅ encoders.json        — {len(encoders['feature_columns'])} feature_columns + mapeamentos")
print(f"  ✅ scaler.pkl           — salvo em {MODEL_DIR / 'scaler.pkl'}")
print(f"\n▶  Próximo passo: python src/03_supervised_classification.py")
