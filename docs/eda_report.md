# Análise Exploratória de Dados (EDA) - Relatório Final

## 📋 Resumo Executivo
Os datasets avaliados demonstram uma estrutura rica para a previsão de atraso de voos, consistindo de mais de 546934 amostragens após a limpeza. A nossa pipeline validou os foreign keys, extraiu anomalias do `ARRIVAL_DELAY` via IQR (preservando consistência estatística) e detectou colinearidades cruciais que devem guiar a modelagem a seguir (evitando vazamento de dados).

---

## 1️⃣ Introdução e Metodologia
Utilizando os datasets `airlines.csv`, `airports.csv` e `flights.csv`, implantou-se uma pipeline de carregamento com sampling de 10% do voos totais usando sementes fixas (`SEED=42`). 

**Tratamentos efetuados:**
* **Missing values:** Colunas estruturalmente imcompletas referentes a razões macro de cancelamento foram deletadas (>80% missing).
* **Outliers:** Filtrou-se os limites inferior e superior de `ARRIVAL_DELAY` usando a faixa de `Q1-3*IQR` a `Q3+3*IQR`.
* **Variáveis Independentes:** Criou-se a variável categórica do horário do dia, estação (`Season`) e datas completas (em tipo Date).

---

## 2️⃣ Análise Descritiva

* **Voos processados:** 546934 registros válidos.
* **Companhia Aérea Predominante:** WN.
* **Aeroporto de Origem Predominante:** ATL.

---

## 3️⃣ Principais Descobertas e Insights

**Insight 1: Efeitos Sazonais e Semanais**
Constatou-se uma variação do valor médio do atraso na chegada conforme o mês de voo (Sazonalidade), existindo um aumento expressivo no Verão (Junho/Julho) na amostra abordada. Semanas que começam as Segundas também sofrem com taxas de atraso um pouco mais elevadas.

**Insight 2: Cascatas Diárias**
Foi plotado (`19_delay_by_hour.png`) o tempo previsto associado ao atraso médio e verificou-se o acúmulo de atrasos - os últimos agendamentos do dia têm maior penalidade devido ao esgotamento sistêmico anterior.

**Insight 3: Ausência de Correlação com a Rota Longa**
Surpreendentemente, a distãncia da rota (`DISTANCE`) possui correlação quase nula (-0.0606) com a proporção do atraso na chegada, derrubando a idéia de que trajetos mais longos embutem mais atrasos em propulsão.

---

## 4️⃣ Recomendações para a Próxima Fase (Modelagem)
- A **Modelagem Supervisionada** para prever se a flag `IS_DELAYED` será 1 ou 0 DEVE EXCLUIR features contemporâneas de atraso imediato (ex: `DEPARTURE_DELAY`), já que elas possuem uma chance esmagadora de Data Leakage na prática real quando se tenta prever com horas de antecedência.
- O *Target Encoding* deve ser utilizado sobre as origin/destinations e as airlines a fim de preservar a significância categórica no classificador.
