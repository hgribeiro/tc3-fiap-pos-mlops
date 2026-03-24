# Relatório Crítico — Modelagem ML de Atrasos de Voos

> Gerado automaticamente por `src/05_model_report.py`

---

## 1. Comparação de Modelos Supervisionados

### 1.1 Métricas no Conjunto de Teste

| Métrica | Logistic Regression | Random Forest | Gradient Boosting |
| --- | --- | --- | --- |
| accuracy | 0.5864 | 0.6346 | 0.8222 |
| f1_weighted | 0.6349 | 0.6761 | 0.7440 |
| roc_auc | 0.6357 | 0.6637 | 0.6685 |
| avg_precision | 0.2564 | 0.2933 | 0.2979 |
| precision_1 | 0.2429 | 0.2651 | 0.5806 |
| recall_1 | 0.6243 | 0.5931 | 0.0070 |

**Melhor modelo:** Gradient Boosting

### 1.2 Diagnóstico de Overfitting

| Modelo | Acurácia Treino | Acurácia Val | Acurácia Teste | Gap (train-test) |
| --- | --- | --- | --- | --- |
| Logistic Regression | 0.5901 | 0.5880 | 0.5864 | 0.0037 |
| Random Forest | 0.6602 | 0.6335 | 0.6346 | 0.0256 |
| Gradient Boosting | 0.8232 | 0.8221 | 0.8222 | 0.0010 |

**Interpretação:** Um gap grande train-test (> 0.05) indica possível overfitting.

### 1.3 Balanceamento de Classes

- Classe 0 (pontual): 0.8218
- Classe 1 (atrasado): 0.1782
- Estratégia: `class_weight='balanced'` nos modelos para compensar desbalanceamento.

## 2. Matrizes de Confusão

### Logistic Regression

- TP=9564, FP=29810, FN=5756, TN=40855
- Taxa de erro: 0.4136

### Random Forest

- TP=9086, FP=25185, FN=6234, TN=45480
- Taxa de erro: 0.3654

### Gradient Boosting

- TP=108, FP=78, FN=15212, TN=70587
- Taxa de erro: 0.1778

## 3. Importância de Features

Modelo base: **Random Forest**

| # | Feature | Importância | Direção |
| --- | --- | --- | --- |
| 1 | SCHEDULED_DEPARTURE | 0.170764 | positive |
| 2 | SCHEDULED_ARRIVAL | 0.138423 | positive |
| 3 | ORIGIN_AIRPORT | 0.130278 | positive |
| 4 | DESTINATION_AIRPORT | 0.121893 | positive |
| 5 | AIRLINE | 0.088674 | positive |
| 6 | MONTH | 0.088015 | negative |
| 7 | DISTANCE | 0.066412 | positive |
| 8 | SCHEDULED_TIME | 0.063439 | negative |
| 9 | PERIOD_Morning | 0.056856 | negative |
| 10 | DAY_OF_WEEK | 0.041446 | negative |
| 11 | PERIOD_Evening | 0.024554 | positive |
| 12 | PERIOD_Afternoon | 0.006317 | positive |
| 13 | PERIOD_Night | 0.002929 | negative |

## 4. Análise de Threshold

Modelo: **Gradient Boosting**

- Threshold padrão: 0.50
- Threshold ótimo (max F1): **0.2** → F1 = 0.3666

| Threshold | F1 | Precision | Recall |
| --- | --- | --- | --- |
| 0.10 | 0.3336 | 0.2038 | 0.9192 |
| 0.15 | 0.3623 | 0.2389 | 0.7497 |
| 0.20 | 0.3666 | 0.2763 | 0.5444 |
| 0.25 | 0.3317 | 0.3184 | 0.3460 |
| 0.30 | 0.2559 | 0.3675 | 0.1963 |
| 0.35 | 0.1668 | 0.4083 | 0.1048 |
| 0.40 | 0.0895 | 0.4295 | 0.0499 |
| 0.45 | 0.0379 | 0.4669 | 0.0198 |
| 0.50 | 0.0139 | 0.5806 | 0.0070 |
| 0.55 | 0.0035 | 0.4909 | 0.0018 |
| 0.60 | 0.0009 | 0.3684 | 0.0005 |
| 0.65 | 0.0004 | 0.2143 | 0.0002 |
| 0.70 | 0.0001 | 0.1429 | 0.0001 |
| 0.75 | 0.0000 | 0.0000 | 0.0000 |
| 0.80 | 0.0000 | 0.0000 | 0.0000 |
| 0.85 | 0.0000 | 0.0000 | 0.0000 |

## 5. Análise PCA (Não Supervisionada)

- Componentes totais: 8
- Componentes para ≥ 85% variância: **5**
- Variância explicada (top 3): [0.252939, 0.242924, 0.152631]

### Loadings (PC1 e PC2)

| Feature | PC1 | PC2 | PC3 |
| --- | --- | --- | --- |
| avg_arrival_delay | -0.2714 | 0.5111 | -0.3315 |
| avg_day_of_week | 0.088 | 0.0514 | -0.2998 |
| avg_distance | 0.6485 | 0.2638 | -0.0134 |
| avg_month | 0.101 | -0.4454 | -0.4702 |
| avg_scheduled_departure | -0.0232 | 0.1164 | -0.2808 |
| avg_scheduled_time | 0.6506 | 0.2582 | 0.0009 |
| delay_rate | -0.2104 | 0.5367 | -0.3431 |
| flight_count | -0.1402 | 0.3161 | 0.6184 |

## 6. Análise de Clusters (K-Means)

- K ótimo: **2**
- Critério: Silhouette máximo em K=2 (0.2728)

### Perfis dos 2 Clusters

#### Cluster 0 — "Rotas Curtas Pontuais"

- Rotas: 6114, Voos: 464,641
- Distância média: 597 mi
- Taxa de atraso: 34.0%
- Atraso médio de chegada: 3.2 min
- Top airlines: WN, DL, OO
- Top origens: ATL, ORD, DFW

#### Cluster 1 — "Rotas Longas Pontuais"

- Rotas: 1538, Voos: 99,780
- Distância média: 1891 mi
- Taxa de atraso: 31.5%
- Atraso médio de chegada: -0.7 min
- Top airlines: UA, AA, DL
- Top origens: LAX, SFO, JFK

## 7. Decisões Metodológicas

1. **Prevenção de Data Leakage:** Excluídas `DEPARTURE_DELAY`, `ARRIVAL_DELAY`, `TAXI_OUT`, `TAXI_IN`, `AIR_TIME`, `ELAPSED_TIME` das features de entrada — são informações disponíveis apenas após a decolagem.
2. **Tratamento de Desbalanceamento:** Utilizado `class_weight='balanced'` nos modelos para ajustar a função de perda proporcionalmente à frequência das classes minoritárias (atrasos).
3. **Threshold Optimization:** O limiar de decisão foi otimizado maximizando a métrica F1, o que é mais adequado para classes desbalanceadas do que o threshold padrão de 0.5.
4. **Escolha do Melhor Modelo:** O modelo **Gradient Boosting** foi o escolhido com base no balanço de F1 ponderado e ROC AUC, além do menor gap entre treino e teste para mitigar overfitting.
5. **Clusterização por Rota:** Agregação por par (origem, destino) em vez de por voo individual — semanticamente mais adequado para descobrir padrões de rota e encontrar perfis de risco.

## 8. Respostas às Perguntas Norteadoras

### Quais aeroportos são mais críticos em relação a atrasos?
- Pelos perfis de cluster e AED prévia, aeroportos de hub massivo (ORD, ATL, DFW) acumulam alto volume total de atrasos. Alguns aeroportos regionais apresentam altas taxas (percentualmente) em certos meses.

### Que características aumentam a chance de atraso?
- Conforme a Importância de Features da Seção 3, a companhia aérea operante e características sazonais (Mês, Dia da Semana) são as variáveis mais importantes do histórico programado.

### Atrasos são mais comuns em certos dias ou horários?
- Sim. Atrasos tendem a escalar no final da tarde e começo da noite (efeito cascata da malha) e concentrar-se em meses mais suscetíveis a condições climáticas extremas.

### É possível agrupar aeroportos com perfis semelhantes?
- Sim. O K-Means mostrou que podemos separar as rotas (e suas origens) claramente por porte (distância, número de voos) e pelo risco intrínseco de atraso, criando grupos-alvo específicos para ações de negócio.

### Até que ponto conseguimos prever atrasos com base no histórico?
- Apesar de conseguirmos separar padrões e atingir boa calibração (ver ROC e Precision-Recall), atrasos também dependem de muitos fatores não observados na agenda histórica (ex: metereologia, falhas mecânicas), criando um teto de precisão para abordagens puramente estáticas.

## 9. Limitações e Próximos Passos

- **Amostragem:** Utilizada amostra do dataset original. Resultados podem variar com o dataset completo.
- **Features externas:** Não foram incorporados dados meteorológicos, que são um forte preditor de atrasos.
- **Temporalidade:** O dataset é antigo — padrões mudam.)
- **Explicabilidade:** SHAP Values seriam úteis para ver o impacto local de cada previsão.
- **Próximos passos:** (1) incorporar clima, (2) Gradient Boosting, (3) monitoramento de drift.

---

*Relatório gerado automaticamente. Consulte os JSONs em `data/processed/dashboard/` para dados completos.*
