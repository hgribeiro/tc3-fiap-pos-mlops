# Task 03: Feature Engineering

## Objetivo
Preparar os dados para modelagem de Machine Learning, aplicando encoding, escalonamento e split estratificado. O output são os datasets de treino/validação/teste em Parquet, prontos para consumo pelos scripts de modelagem.

## Contexto
- **Input:** `data/processed/flights_sample_processed.csv` (gerado pela Task 01)
- **Output:** splits Parquet + artefatos de encoding/escalonamento
- **Cenário preditivo:** prever atraso **antes do voo decolar** — **sem features de data leakage**
- **Arquivo:** `src/02_feature_engineering.py`

---

## Premissas de Ciência de Dados

### Definição do Problema
- **Classificação binária:** `IS_DELAYED` (1 = chegada > **15 min** de atraso)
- A aviação considera atrasos de até 15 minutos como toleráveis — somente acima de 15 min é classificado como atraso real.
- Foco no cenário **pré-decolagem**: só usar o que é conhecido antes do voo sair.

### Features Permitidas (sem data leakage)
| Feature | Tipo | Justificativa |
|---|---|---|
| `MONTH` | int | Sazonalidade |
| `DAY_OF_WEEK` | int | Padrão semanal |
| `SCHEDULED_DEPARTURE` | int | Horário planejado |
| `SCHEDULED_ARRIVAL` | int | Horário planejado |
| `DISTANCE` | float | Característica da rota |
| `AIRLINE` | category | Operadora |
| `ORIGIN_AIRPORT` | category | Aeroporto origem |
| `DESTINATION_AIRPORT` | category | Aeroporto destino |
| `DEPARTURE_PERIOD` | category | Período do dia (derivado) |
| `SCHEDULED_TIME` | float | Duração planejada |

> ⚠️ **Não usar:** `DEPARTURE_DELAY`, `ARRIVAL_DELAY`, `TAXI_OUT`, `TAXI_IN`, `AIR_TIME`, `ELAPSED_TIME`

---

## Etapas

### 1. Carregamento e seleção
- [x] Carregar `data/processed/flights_sample_processed.csv`
- [x] Selecionar apenas as features permitidas (sem leakage)
- [x] Remover linhas com `IS_DELAYED` nulo (target obrigatório)
- [x] Remover linhas com `CANCELLED == 1` (voo não decolou — diferente de atraso)

### 2. Tratamento de nulos
- [x] Numéricas: imputar com **mediana** do treino (nunca do dataset completo para evitar leakage)
- [x] Categóricas: imputar com `'UNKNOWN'` como nova categoria

### 3. Encoding
- [x] `AIRLINE` → **Target Encoding** (média de `IS_DELAYED` por companhia no treino)
- [x] `ORIGIN_AIRPORT`, `DESTINATION_AIRPORT` → **Target Encoding** (mesma lógica)
- [x] `DEPARTURE_PERIOD` → **One-Hot Encoding** (4 categorias: Morning, Afternoon, Evening, Night)
- [x] Salvar mapeamentos em `models/encoders.json` para uso em inferência no dashboard

### 4. Splitting estratificado
- [x] Split **estratificado** por `IS_DELAYED` para manter proporção de classes
- [x] Proporção: **70% treino / 15% validação / 15% teste** com `random_state=42`
- [x] Verificar e imprimir distribuição de classes em cada split

### 5. Escalonamento
- [x] `StandardScaler` ajustado **apenas** no treino
- [x] Transformar treino, validação e teste com o mesmo scaler
- [x] Salvar em `models/scaler.pkl`

---

## Outputs

```
data/processed/
├── X_train.parquet
├── X_val.parquet
├── X_test.parquet
├── y_train.parquet
├── y_val.parquet
└── y_test.parquet
models/
├── scaler.pkl
└── encoders.json
```

---

## Tratamento de Desbalanceamento
- Verificar razão de classes de `IS_DELAYED` (espera-se ~40-60% atrasados)
- Se desbalanceado (< 30% ou > 70% de uma classe): usar `class_weight='balanced'` nos modelos e reportar impacto

---

## Notas de DS
- **Leakage:** `DEPARTURE_DELAY` é o principal risco — **não usar** como feature.
- **Reprodutibilidade:** todo `random_state=42`.
- **Parquet:** usar `.parquet` para os splits (10x menor, 5x mais rápido que CSV).
- **Target Encoding:** calcular **somente no treino** e aplicar no val/teste — evita leakage de grupo.

---

## Critérios de Sucesso

| Requisito | Entregável | Status |
|---|---|---|
| Sem data leakage | Features pré-voo apenas | ✅ |
| Split estratificado 70/15/15 | Parquet files | ✅ |
| Encoding consistente treino→teste | `models/encoders.json` | ✅ |
| Scaler fit no treino apenas | `models/scaler.pkl` | ✅ |

---

## Dependências
```
scikit-learn>=1.3.0
joblib>=1.3.0
pyarrow>=14.0
```

## Ordem de Execução
```bash
python src/01_eda.py                     # Task 01 (pré-requisito)
python src/02_feature_engineering.py     # ← esta task
```
