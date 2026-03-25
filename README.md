# Flight Delay Prediction - USA Flights Analysis

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Sobre o Projeto

Este projeto aplica técnicas de **Machine Learning supervisionado e não supervisionado** para analisar e prever atrasos em voos nos Estados Unidos, utilizando dados públicos de aviação. O objetivo é desenvolver um pipeline completo de ciência de dados, desde a exploração até a modelagem e interpretação dos resultados.

### 🎯 Objetivos

- **Análise Exploratória (EDA)**: Identificar padrões, tendências e insights nos dados de voos
- **Modelagem Supervisionada**: Prever se um voo atrasará (classificação) e/ou quanto tempo durará o atraso (regressão)
- **Modelagem Não Supervisionada**: Identificar agrupamentos e padrões ocultos em rotas, aeroportos e companhias aéreas
- **Insights Acionáveis**: Fornecer recomendações baseadas em dados para mitigação de atrasos

### ❓ Perguntas de Negócio

- Quais aeroportos são mais críticos em relação a atrasos?
- Que características aumentam a probabilidade de atraso?
- Atrasos são mais comuns em certos dias da semana ou horários?
- É possível agrupar aeroportos com perfis operacionais semelhantes?
- Qual a acurácia na previsão de atrasos com base em dados históricos?

---

## 📁 Estrutura do Projeto

```
.
├── data/
│   ├── airlines.csv          # Companhias aéreas (IATA_CODE, AIRLINE)
│   ├── airports.csv          # Aeroportos (IATA_CODE, CITY, STATE, etc)
│   ├── flights.csv           # Dados de voos (~592MB) ⚠️
│   └── processed/            # Dados processados pelo EDA
├── notebooks/
│   └── 01_eda.ipynb          # Análise exploratória (notebook)
├── src/
│   ├── 01_eda.py                        # Análise exploratória
│   ├── 02_feature_engineering.py        # Engenharia de features
│   ├── 03_supervised_classification.py  # Modelagem supervisionada
│   ├── 04_unsupervised.py               # Modelagem não supervisionada
│   ├── 05_model_report.py               # Relatório de avaliação
│   └── prepare_dashboard_data.py        # Consolidação de dados do dashboard
├── docs/
│   ├── eda_plots/            # Visualizações geradas pelo EDA
│   └── tc3.md                # Enunciado do Tech Challenge
├── tasks/
│   └── task01.md             # Especificação da Task 01
├── requirements.txt          # Dependências do projeto
└── README.md
```

---

## 🔧 Tecnologias e Ferramentas

- **Python 3.8+**: Linguagem principal
- **Pandas & NumPy**: Manipulação e análise de dados
- **Scikit-learn**: Modelagem de machine learning
- **XGBoost / LightGBM**: Modelos de gradient boosting
- **Matplotlib & Seaborn**: Visualização de dados
- **Plotly**: Visualizações interativas
- **Jupyter Notebook**: Ambiente de desenvolvimento

---

## 🚀 Como Executar

### 1. Clone o Repositório

```bash
git clone https://github.com/[seu-usuario]/tc3-fiap-pos-mlops.git
cd tc3-fiap-pos-mlops
```

### 2. Crie um Ambiente Virtual (Recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o Pipeline MLOps

Execute os scripts python na seguinte ordem:

```bash
python src/01_eda.py
python src/02_feature_engineering.py
python src/03_supervised_classification.py
python src/04_unsupervised.py
python src/05_model_report.py
python src/prepare_dashboard_data.py
```

*(Opcional)* Você também pode explorar a análise gravada usando `jupyter notebook` na pasta `notebooks/`.

### 5. Execute o Dashboard

Para visualizar o dashboard com os resultados das análises e dos modelos:

```bash
npx -y serve . -l 3847
```

Feito isso, abra o navegador e acesse: [http://localhost:3847/dashboard/](http://localhost:3847/dashboard/)

---

## 📊 Pipeline de Machine Learning

### 1. **Análise Exploratória de Dados (EDA)**
- Estatísticas descritivas e distribuições
- Análise de correlações
- Identificação de outliers e missing values
- Visualizações com insights de negócio

### 2. **Modelagem Supervisionada**

**Classificação**: Prever se um voo atrasará (binário)
- Algoritmos testados: Logistic Regression, Random Forest, Gradient Boosting
- Métricas: Accuracy, Precision, Recall, F1-Score, AUC-ROC

### 3. **Modelagem Não Supervisionada**

**Clusterização**:
- K-Means para agrupamento de aeroportos/rotas
- Análise de perfis de companhias aéreas

**Redução de Dimensionalidade**:
- PCA para visualização de alta dimensionalidade

### 4. **Interpretação e Conclusões**
- Feature importance
- SHAP values para explicabilidade
- Limitações dos modelos
- Recomendações de melhorias

---

## 📈 Resultados Esperados

- Identificação de fatores críticos para atrasos
- Modelo preditivo com performance acima do baseline
- Segmentação de aeroportos e rotas por perfil de risco
- Dashboard com insights visuais (opcional)
- Recomendações práticas para mitigação de atrasos

---

## 🔄 Melhorias Futuras

- [ ] Feature engineering avançado (feriados, condições climáticas, eventos)
- [ ] Análise temporal (séries temporais, sazonalidade)
- [ ] Mapas geográficos de rotas e atrasos
- [ ] Dashboard interativo (Streamlit/Dash)
- [ ] Detecção de anomalias em operações
- [ ] API para predição em tempo real
- [ ] MLOps pipeline (CI/CD, monitoramento)

---

## 👥 Equipe

Projeto desenvolvido para o **Tech Challenge 3** - FIAP Pós-Graduação em Machine Learning Engineering.

**Integrantes:**
- Carol Devens
- Matheus Silvestre
- Valterlan

---

## 📄 Licença

Este projeto é desenvolvido para fins educacionais como parte do curso de Pós-Graduação em MLOps da FIAP.

---

## 📚 Referências

- Dataset: [US Flight Delays and Cancellations](https://www.kaggle.com/datasets)
- FIAP - Machine Learning Engineering
- Documentação Scikit-learn
- Documentação XGBoost/LightGBM
