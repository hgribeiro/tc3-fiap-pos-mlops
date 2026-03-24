"""
Modelagem Supervisionada — Flight Delay Classification
Task 02, Script 2: Treino, avaliação e geração de JSONs para dashboard

Input : data/processed/{X,y}_{train,val,test}.parquet
        models/encoders.json
Output: models/{logistic_regression,random_forest,gradient_boosting}.pkl
        data/processed/dashboard/ml_*.json  (7 arquivos)
"""

# %% Imports
import json
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

warnings.filterwarnings("ignore")

# %% Paths
PROC = Path("./data/processed")
DASH = Path("./data/processed/dashboard")
MODEL_DIR = Path("./models")
DASH.mkdir(parents=True, exist_ok=True)

# %% ============================================================================
# 1. CARREGAMENTO DOS SPLITS
# =============================================================================

print("=" * 80)
print("1. CARREGAMENTO DOS SPLITS")
print("=" * 80)

X_train = pd.read_parquet(PROC / "X_train.parquet")
X_val = pd.read_parquet(PROC / "X_val.parquet")
X_test = pd.read_parquet(PROC / "X_test.parquet")
y_train = pd.read_parquet(PROC / "y_train.parquet").squeeze()
y_val = pd.read_parquet(PROC / "y_val.parquet").squeeze()
y_test = pd.read_parquet(PROC / "y_test.parquet").squeeze()

print(f"✓ Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
print(f"✓ Class balance (train): IS_DELAYED=1 → {y_train.mean()*100:.2f}%")

# Carregar encoders para decodificar previsões
with open(MODEL_DIR / "encoders.json") as f:
    encoders = json.load(f)

# %% ============================================================================
# 2. TREINAR MODELOS
# =============================================================================

print("\n" + "=" * 80)
print("2. TREINAMENTO DOS MODELOS")
print("=" * 80)

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000, class_weight="balanced", random_state=42, n_jobs=-1
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_leaf=50,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        random_state=42,
    ),
}

pkl_names = {
    "Logistic Regression": "logistic_regression.pkl",
    "Random Forest": "random_forest.pkl",
    "Gradient Boosting": "gradient_boosting.pkl",
}

trained = {}
for name, model in models.items():
    print(f"\n  ▸ Treinando {name}...")
    model.fit(X_train, y_train)
    trained[name] = model
    joblib.dump(model, MODEL_DIR / pkl_names[name])
    print(f"    ✓ Salvo: {MODEL_DIR / pkl_names[name]}")

# %% ============================================================================
# 3. AVALIAÇÃO
# =============================================================================

print("\n" + "=" * 80)
print("3. AVALIAÇÃO DOS MODELOS")
print("=" * 80)


def evaluate(model, X, y, label=""):
    y_pred = model.predict(X)
    y_prob = model.predict_proba(X)[:, 1]
    acc = accuracy_score(y, y_pred)
    f1w = f1_score(y, y_pred, average="weighted")
    prec = precision_score(y, y_pred, pos_label=1)
    rec = recall_score(y, y_pred, pos_label=1)
    auc = roc_auc_score(y, y_prob)
    ap = average_precision_score(y, y_prob)
    return {
        "accuracy": round(float(acc), 4),
        "f1_weighted": round(float(f1w), 4),
        "precision_1": round(float(prec), 4),
        "recall_1": round(float(rec), 4),
        "roc_auc": round(float(auc), 4),
        "avg_precision": round(float(ap), 4),
    }


# Métricas em train / val / test
results = {}
for name, model in trained.items():
    r_train = evaluate(model, X_train, y_train)
    r_val = evaluate(model, X_val, y_val)
    r_test = evaluate(model, X_test, y_test)
    results[name] = {"train": r_train, "val": r_val, "test": r_test}
    print(f"\n  {name}:")
    print(f"    Train  — acc={r_train['accuracy']:.4f}  f1={r_train['f1_weighted']:.4f}  auc={r_train['roc_auc']:.4f}")
    print(f"    Val    — acc={r_val['accuracy']:.4f}  f1={r_val['f1_weighted']:.4f}  auc={r_val['roc_auc']:.4f}")
    print(f"    Test   — acc={r_test['accuracy']:.4f}  f1={r_test['f1_weighted']:.4f}  auc={r_test['roc_auc']:.4f}")

# Determinar melhor modelo pelo AUC-ROC no teste
best_name = max(results, key=lambda n: results[n]["test"]["roc_auc"])
print(f"\n  ★ Melhor modelo: {best_name} (AUC-ROC teste = {results[best_name]['test']['roc_auc']:.4f})")

# %% ============================================================================
# 4. JSON — ml_model_comparison.json
# =============================================================================

print("\n" + "=" * 80)
print("4. GERANDO JSONs PARA DASHBOARD")
print("=" * 80)

model_names = list(results.keys())
comparison = {
    "models": model_names,
    "metrics": {
        "accuracy": [results[n]["test"]["accuracy"] for n in model_names],
        "f1_weighted": [results[n]["test"]["f1_weighted"] for n in model_names],
        "roc_auc": [results[n]["test"]["roc_auc"] for n in model_names],
        "avg_precision": [results[n]["test"]["avg_precision"] for n in model_names],
        "precision_1": [results[n]["test"]["precision_1"] for n in model_names],
        "recall_1": [results[n]["test"]["recall_1"] for n in model_names],
        "train_accuracy": [results[n]["train"]["accuracy"] for n in model_names],
        "val_accuracy": [results[n]["val"]["accuracy"] for n in model_names],
    },
    "best_model": best_name,
    "class_balance": {
        "0": round(float((y_test == 0).mean()), 4),
        "1": round(float((y_test == 1).mean()), 4),
    },
}

with open(DASH / "ml_model_comparison.json", "w") as f:
    json.dump(comparison, f, indent=2)
print("  ✓ ml_model_comparison.json")

# %% ============================================================================
# 5. JSON — ml_roc_curves.json
# =============================================================================

roc_data = {}
for name, model in trained.items():
    y_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc_val = roc_auc_score(y_test, y_prob)
    # Down-sample points for JSON (max 200 points)
    step = max(1, len(fpr) // 200)
    roc_data[name] = {
        "fpr": [round(float(v), 6) for v in fpr[::step]],
        "tpr": [round(float(v), 6) for v in tpr[::step]],
        "auc": round(float(auc_val), 4),
    }

with open(DASH / "ml_roc_curves.json", "w") as f:
    json.dump(roc_data, f, indent=2)
print("  ✓ ml_roc_curves.json")

# %% ============================================================================
# 6. JSON — ml_pr_curves.json
# =============================================================================

pr_data = {}
for name, model in trained.items():
    y_prob = model.predict_proba(X_test)[:, 1]
    prec_arr, rec_arr, _ = precision_recall_curve(y_test, y_prob)
    ap_val = average_precision_score(y_test, y_prob)
    step = max(1, len(prec_arr) // 200)
    pr_data[name] = {
        "precision": [round(float(v), 6) for v in prec_arr[::step]],
        "recall": [round(float(v), 6) for v in rec_arr[::step]],
        "avg_precision": round(float(ap_val), 4),
    }

with open(DASH / "ml_pr_curves.json", "w") as f:
    json.dump(pr_data, f, indent=2)
print("  ✓ ml_pr_curves.json")

# %% ============================================================================
# 7. JSON — ml_confusion_matrices.json
# =============================================================================

cm_data = {}
for name, model in trained.items():
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    cm_data[name] = {
        "matrix": cm.tolist(),
        "labels": ["On Time", "Delayed"],
        "TN": int(cm[0, 0]),
        "FP": int(cm[0, 1]),
        "FN": int(cm[1, 0]),
        "TP": int(cm[1, 1]),
    }

with open(DASH / "ml_confusion_matrices.json", "w") as f:
    json.dump(cm_data, f, indent=2)
print("  ✓ ml_confusion_matrices.json")

# %% ============================================================================
# 8. JSON — ml_feature_importance.json
# =============================================================================

feature_names = X_train.columns.tolist()

# Random Forest — Gini importance
rf_model = trained["Random Forest"]
rf_imp = rf_model.feature_importances_

# Logistic Regression — absolute coefficients
lr_model = trained["Logistic Regression"]
lr_coefs = np.abs(lr_model.coef_[0])

# Normalizar LR coefs para comparabilidade
lr_imp = lr_coefs / lr_coefs.max()

# Usar RF como principal (mais confiável)
sorted_idx = np.argsort(rf_imp)[::-1][:20]

fi_list = []
for i in sorted_idx:
    direction = "positive"
    if "Logistic Regression" in trained:
        # Usar sinal do coeficiente LR para direção
        coef_val = lr_model.coef_[0][i]
        direction = "positive" if coef_val >= 0 else "negative"
    fi_list.append({
        "name": feature_names[i],
        "importance": round(float(rf_imp[i]), 6),
        "direction": direction,
    })

fi_json = {"model": "Random Forest", "features": fi_list}

with open(DASH / "ml_feature_importance.json", "w") as f:
    json.dump(fi_json, f, indent=2)
print("  ✓ ml_feature_importance.json")

# %% ============================================================================
# 9. JSON — ml_threshold_analysis.json
# =============================================================================

best_model = trained[best_name]
y_prob_best = best_model.predict_proba(X_test)[:, 1]

thresholds = np.arange(0.1, 0.95, 0.05)
th_analysis = {"model": best_name, "thresholds": [], "f1": [], "precision": [], "recall": []}

for th in thresholds:
    y_pred_th = (y_prob_best >= th).astype(int)
    if y_pred_th.sum() == 0 or (1 - y_pred_th).sum() == 0:
        continue
    th_analysis["thresholds"].append(round(float(th), 2))
    th_analysis["f1"].append(round(float(f1_score(y_test, y_pred_th)), 4))
    th_analysis["precision"].append(round(float(precision_score(y_test, y_pred_th)), 4))
    th_analysis["recall"].append(round(float(recall_score(y_test, y_pred_th)), 4))

# Threshold ótimo (max F1)
opt_idx = int(np.argmax(th_analysis["f1"]))
th_analysis["optimal_threshold"] = th_analysis["thresholds"][opt_idx]
th_analysis["optimal_f1"] = th_analysis["f1"][opt_idx]

with open(DASH / "ml_threshold_analysis.json", "w") as f:
    json.dump(th_analysis, f, indent=2)
print("  ✓ ml_threshold_analysis.json")
print(f"    Threshold ótimo: {th_analysis['optimal_threshold']} → F1 = {th_analysis['optimal_f1']:.4f}")

# %% ============================================================================
# 10. JSON — ml_test_predictions.json
# =============================================================================

# Carregar dados originais para decodificar features
df_orig = pd.read_csv("data/processed/flights_sample_processed.csv")
# Remover cancelados e sem IS_DELAYED como fizemos no feature engineering
df_orig = df_orig[df_orig["CANCELLED"] != 1].dropna(subset=["IS_DELAYED"]).reset_index(drop=True)

# Recuperar os índices do split de teste
# Replay do split com mesmo random_state para obter os índices corretos
n_total = len(df_orig)
n_train_val = int(n_total * 0.70)
_, temp_idx = train_test_split(range(n_total), test_size=0.30, 
                                stratify=df_orig["IS_DELAYED"].astype(int), 
                                random_state=42)
_, test_idx = train_test_split(temp_idx, test_size=0.50,
                                stratify=df_orig.iloc[temp_idx]["IS_DELAYED"].astype(int),
                                random_state=42)

df_test_orig = df_orig.iloc[test_idx].reset_index(drop=True)

# Previsões do melhor modelo
y_prob_all = best_model.predict_proba(X_test)[:, 1]
y_pred_all = best_model.predict(X_test)

# Montar sample (até 5000)
sample_size = min(5000, len(df_test_orig))
sample_idx = np.random.RandomState(42).choice(len(df_test_orig), sample_size, replace=False)

columns = ["AIRLINE", "ORIGIN_AIRPORT", "DESTINATION_AIRPORT", "MONTH",
           "DAY_OF_WEEK", "SCHEDULED_DEPARTURE", "DISTANCE",
           "y_true", "y_pred", "y_prob"]

data_rows = []
for i in sample_idx:
    row = [
        str(df_test_orig.iloc[i].get("AIRLINE_NAME", df_test_orig.iloc[i].get("AIRLINE", ""))),
        str(df_test_orig.iloc[i].get("ORIGIN_AIRPORT_NAME", df_test_orig.iloc[i].get("ORIGIN_AIRPORT", ""))),
        str(df_test_orig.iloc[i].get("DESTINATION_AIRPORT_NAME", df_test_orig.iloc[i].get("DESTINATION_AIRPORT", ""))),
        int(df_test_orig.iloc[i].get("MONTH", 0)),
        int(df_test_orig.iloc[i].get("DAY_OF_WEEK", 0)),
        int(df_test_orig.iloc[i].get("SCHEDULED_DEPARTURE", 0)),
        float(df_test_orig.iloc[i].get("DISTANCE", 0)),
        int(y_test.iloc[i]),
        int(y_pred_all[i]),
        round(float(y_prob_all[i]), 4),
    ]
    data_rows.append(row)

pred_json = {
    "sample_size": sample_size,
    "model": best_name,
    "columns": columns,
    "data": data_rows,
}

with open(DASH / "ml_test_predictions.json", "w") as f:
    json.dump(pred_json, f, indent=2)
print(f"  ✓ ml_test_predictions.json ({sample_size} amostras)")

print("\n" + "=" * 80)
print("MODELAGEM SUPERVISIONADA CONCLUÍDA!")
print("=" * 80)
