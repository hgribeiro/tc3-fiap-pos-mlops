"""
Relatório Crítico — Geração automática de docs/model_report.md
Task 02, Script 4: Consolida todos os JSONs em um relatório markdown

Input : data/processed/dashboard/ml_*.json
Output: docs/model_report.md
"""

# %% Imports
import json
from pathlib import Path

DASH = Path("./data/processed/dashboard")
DOCS = Path("./docs")
DOCS.mkdir(parents=True, exist_ok=True)

# %% Carregar todos os JSONs
print("=" * 80)
print("GERANDO RELATÓRIO CRÍTICO")
print("=" * 80)


def load(name):
    p = DASH / name
    if not p.exists():
        print(f"  ⚠ {name} não encontrado — seção será omitida")
        return None
    with open(p) as f:
        return json.load(f)


comp = load("ml_model_comparison.json")
roc = load("ml_roc_curves.json")
pr = load("ml_pr_curves.json")
cm = load("ml_confusion_matrices.json")
fi = load("ml_feature_importance.json")
th = load("ml_threshold_analysis.json")
pred = load("ml_test_predictions.json")
pca = load("ml_pca_variance.json")
elbow = load("ml_kmeans_elbow.json")
profiles = load("ml_cluster_profiles.json")

# %% Gerar relatório
lines = []
L = lines.append  # shorthand

L("# Relatório Crítico — Modelagem ML de Atrasos de Voos\n")
L("> Gerado automaticamente por `src/05_model_report.py`\n")
L("---\n")

# ---------- Seção 1: Comparação de Modelos ----------
L("## 1. Comparação de Modelos Supervisionados\n")

if comp:
    L("### 1.1 Métricas no Conjunto de Teste\n")
    L("| Métrica | " + " | ".join(comp["models"]) + " |")
    L("| --- | " + " | ".join(["---"] * len(comp["models"])) + " |")
    for metric in ["accuracy", "f1_weighted", "roc_auc", "avg_precision", "precision_1", "recall_1"]:
        vals = comp["metrics"].get(metric, [])
        L(f"| {metric} | " + " | ".join(f"{v:.4f}" for v in vals) + " |")
    L("")
    L(f"**Melhor modelo:** {comp['best_model']}\n")

    # Overfitting check
    L("### 1.2 Diagnóstico de Overfitting\n")
    L("| Modelo | Acurácia Treino | Acurácia Val | Acurácia Teste | Gap (train-test) |")
    L("| --- | --- | --- | --- | --- |")
    for i, name in enumerate(comp["models"]):
        tr = comp["metrics"]["train_accuracy"][i]
        va = comp["metrics"]["val_accuracy"][i]
        te = comp["metrics"]["accuracy"][i]
        gap = tr - te
        L(f"| {name} | {tr:.4f} | {va:.4f} | {te:.4f} | {gap:.4f} |")
    L("")
    L("**Interpretação:** Um gap grande train-test (> 0.05) indica possível overfitting.\n")

    L("### 1.3 Balanceamento de Classes\n")
    cb = comp.get("class_balance", {})
    L(f"- Classe 0 (pontual): {cb.get('0', 'N/A')}")
    L(f"- Classe 1 (atrasado): {cb.get('1', 'N/A')}")
    L(f"- Estratégia: `class_weight='balanced'` nos modelos para compensar desbalanceamento.\n")

# ---------- Seção 2: Matrizes de Confusão ----------
L("## 2. Matrizes de Confusão\n")
if cm:
    for name, data in cm.items():
        L(f"### {name}\n")
        L(f"- TP={data['TP']}, FP={data['FP']}, FN={data['FN']}, TN={data['TN']}")
        total = data['TP'] + data['FP'] + data['FN'] + data['TN']
        if total > 0:
            L(f"- Taxa de erro: {(data['FP'] + data['FN']) / total:.4f}\n")

# ---------- Seção 3: Feature Importance ----------
L("## 3. Importância de Features\n")
if fi:
    L(f"Modelo base: **{fi['model']}**\n")
    L("| # | Feature | Importância | Direção |")
    L("| --- | --- | --- | --- |")
    for i, feat in enumerate(fi["features"][:20], 1):
        L(f"| {i} | {feat['name']} | {feat['importance']:.6f} | {feat['direction']} |")
    L("")

# ---------- Seção 4: Threshold Ótimo ----------
L("## 4. Análise de Threshold\n")
if th:
    L(f"Modelo: **{th['model']}**\n")
    L(f"- Threshold padrão: 0.50")
    L(f"- Threshold ótimo (max F1): **{th['optimal_threshold']}** → F1 = {th['optimal_f1']:.4f}\n")
    L("| Threshold | F1 | Precision | Recall |")
    L("| --- | --- | --- | --- |")
    for i in range(len(th["thresholds"])):
        L(f"| {th['thresholds'][i]:.2f} | {th['f1'][i]:.4f} | {th['precision'][i]:.4f} | {th['recall'][i]:.4f} |")
    L("")

# ---------- Seção 5: PCA ----------
L("## 5. Análise PCA (Não Supervisionada)\n")
if pca:
    L(f"- Componentes totais: {pca['n_components']}")
    L(f"- Componentes para ≥ 85% variância: **{pca['components_for_85pct']}**")
    L(f"- Variância explicada (top 3): {pca['explained_variance_ratio'][:3]}\n")

    if "loadings" in pca:
        L("### Loadings (PC1 e PC2)\n")
        # Coletar todas as features dos loadings
        all_feats = set()
        for pc_data in pca["loadings"].values():
            all_feats.update(pc_data.keys())
        all_feats = sorted(all_feats)

        pcs = sorted(pca["loadings"].keys())[:3]
        L("| Feature | " + " | ".join(pcs) + " |")
        L("| --- | " + " | ".join(["---"] * len(pcs)) + " |")
        for feat in all_feats:
            vals = [str(pca["loadings"].get(pc, {}).get(feat, "—")) for pc in pcs]
            L(f"| {feat} | " + " | ".join(vals) + " |")
        L("")

# ---------- Seção 6: Clusters ----------
L("## 6. Análise de Clusters (K-Means)\n")
if elbow:
    L(f"- K ótimo: **{elbow['chosen_k']}**")
    L(f"- Critério: {elbow['choice_reason']}\n")

if profiles:
    L(f"### Perfis dos {profiles['n_clusters']} Clusters\n")
    for c in profiles["clusters"]:
        L(f"#### Cluster {c['id']} — \"{c['label']}\"\n")
        L(f"- Rotas: {c['n_routes']}, Voos: {c['n_flights']:,}")
        L(f"- Distância média: {c['avg_distance']:.0f} mi")
        L(f"- Taxa de atraso: {c['avg_delay_rate']:.1%}")
        L(f"- Atraso médio de chegada: {c['avg_arrival_delay']:.1f} min")
        L(f"- Top airlines: {', '.join(c['top_airlines'])}")
        L(f"- Top origens: {', '.join(c['top_origins'])}\n")

# ---------- Seção 7: Decisões Metodológicas ----------
L("## 7. Decisões Metodológicas\n")
L("1. **Prevenção de Data Leakage:** Excluídas `DEPARTURE_DELAY`, `ARRIVAL_DELAY`, `TAXI_OUT`, `TAXI_IN`, `AIR_TIME`, `ELAPSED_TIME` das features de entrada — são informações disponíveis apenas após a decolagem.")
L("2. **Tratamento de Desbalanceamento:** Utilizado `class_weight='balanced'` nos modelos para ajustar a função de perda proporcionalmente à frequência das classes minoritárias (atrasos).")
L("3. **Threshold Optimization:** O limiar de decisão foi otimizado maximizando a métrica F1, o que é mais adequado para classes desbalanceadas do que o threshold padrão de 0.5.")
if comp:
    L(f"4. **Escolha do Melhor Modelo:** O modelo **{comp['best_model']}** foi o escolhido com base no balanço de F1 ponderado e ROC AUC, além do menor gap entre treino e teste para mitigar overfitting.")
L("5. **Clusterização por Rota:** Agregação por par (origem, destino) em vez de por voo individual — semanticamente mais adequado para descobrir padrões de rota e encontrar perfis de risco.\n")

# ---------- Seção 8: Respostas às Perguntas Norteadoras ----------
L("## 8. Respostas às Perguntas Norteadoras\n")
L("### Quais aeroportos são mais críticos em relação a atrasos?")
L("- Pelos perfis de cluster e AED prévia, aeroportos de hub massivo (ORD, ATL, DFW) acumulam alto volume total de atrasos. Alguns aeroportos regionais apresentam altas taxas (percentualmente) em certos meses.\n")
L("### Que características aumentam a chance de atraso?")
L("- Conforme a Importância de Features da Seção 3, a companhia aérea operante e características sazonais (Mês, Dia da Semana) são as variáveis mais importantes do histórico programado.\n")
L("### Atrasos são mais comuns em certos dias ou horários?")
L("- Sim. Atrasos tendem a escalar no final da tarde e começo da noite (efeito cascata da malha) e concentrar-se em meses mais suscetíveis a condições climáticas extremas.\n")
L("### É possível agrupar aeroportos com perfis semelhantes?")
L("- Sim. O K-Means mostrou que podemos separar as rotas (e suas origens) claramente por porte (distância, número de voos) e pelo risco intrínseco de atraso, criando grupos-alvo específicos para ações de negócio.\n")
L("### Até que ponto conseguimos prever atrasos com base no histórico?")
L("- Apesar de conseguirmos separar padrões e atingir boa calibração (ver ROC e Precision-Recall), atrasos também dependem de muitos fatores não observados na agenda histórica (ex: metereologia, falhas mecânicas), criando um teto de precisão para abordagens puramente estáticas.\n")

# ---------- Seção 9: Limitações e Próximos Passos ----------
L("## 9. Limitações e Próximos Passos\n")
L("- **Amostragem:** Utilizada amostra do dataset original. Resultados podem variar com o dataset completo.")
L("- **Features externas:** Não foram incorporados dados meteorológicos, que são um forte preditor de atrasos.")
L("- **Temporalidade:** O dataset é antigo — padrões mudam.)")
L("- **Explicabilidade:** SHAP Values seriam úteis para ver o impacto local de cada previsão.")
L("- **Próximos passos:** (1) incorporar clima, (2) Gradient Boosting, (3) monitoramento de drift.\n")

L("---\n")
L("*Relatório gerado automaticamente. Consulte os JSONs em `data/processed/dashboard/` para dados completos.*\n")

# %% Salvar
report_path = DOCS / "model_report.md"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\n✓ Relatório salvo em: {report_path}")
print(f"  ({len(lines)} linhas)")
print("\n" + "=" * 80)
print("RELATÓRIO CONCLUÍDO!")
print("=" * 80)
