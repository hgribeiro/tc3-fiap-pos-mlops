# Copilot Instructions - Flight Delay Prediction Project

## Project Overview

This is a **Tech Challenge 3** project for FIAP MLOps post-graduate course. The goal is to analyze and predict flight delays in the USA using supervised and unsupervised machine learning techniques.

**Important**: This project represents 90% of the final grade and must be developed as a team.

## Setup & Dependencies

### Installation
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Running Jupyter Notebooks
```bash
jupyter notebook
```
Execute notebooks in numerical order from the `notebooks/` directory.

## Data Architecture

### Datasets Location
- `data/airlines.csv` - Airline information (~359 bytes)
- `data/airports.csv` - Airport details (~24KB)
- `data/flights.csv` - **Main dataset** (~592MB) ⚠️

### Performance Considerations for Large Files

When working with `flights.csv`:

```python
# Optimize dtypes to reduce memory
dtypes = {
    'col1': 'int32',      # instead of int64
    'col2': 'category',   # for categorical columns
}
df = pd.read_csv('data/flights.csv', dtype=dtypes)

# Read in chunks for processing
chunk_size = 100000
for chunk in pd.read_csv('data/flights.csv', chunksize=chunk_size):
    # Process each chunk
    pass

# Or use sampling for initial exploration
df_sample = pd.read_csv('data/flights.csv', 
                        skiprows=lambda i: i>0 and np.random.random() > 0.1)
```

### Directory Structure
```
data/
├── raw/           # Original datasets
├── processed/     # Cleaned/transformed datasets
└── external/      # External data (holidays, weather, etc.)
```

## Development Workflow

### Phase Sequence
1. **EDA** (Exploratory Data Analysis) - `01_eda.ipynb`
2. **Preprocessing** - `02_preprocessing.ipynb`
3. **Supervised Models** - `03_supervised_models.ipynb`
4. **Unsupervised Models** - `04_unsupervised_models.ipynb`

### Code Organization
- `src/data/` - Data ingestion and transformation scripts
- `src/features/` - Feature engineering code
- `src/models/` - Model training and evaluation code
- `src/visualization/` - Visualization functions
- `models/` - Saved trained models
- `docs/` - Additional documentation

## Machine Learning Pipeline

### Required Components

**Supervised Learning** (minimum 1):
- Classification: Predict if flight will be delayed (binary)
  - Algorithms: Logistic Regression, Random Forest, XGBoost, LightGBM
  - Metrics: Accuracy, Precision, Recall, F1-Score, AUC-ROC
- Regression: Predict delay duration in minutes
  - Algorithms: Linear Regression, Ridge, Random Forest, XGBoost
  - Metrics: MAE, RMSE, R²

**Unsupervised Learning** (minimum 1):
- Clustering: K-Means, DBSCAN for airports/routes/airlines
- Dimensionality Reduction: PCA, t-SNE for visualization

**Model Interpretation**:
- Feature importance analysis
- SHAP values for explainability

## Key Business Questions

- Which airports are most critical for delays?
- What features increase delay probability?
- Are delays more common on certain days/times?
- Can airports be grouped by similar operational profiles?
- How accurately can we predict delays from historical data?

## Best Practices

### Data Handling
- Always document data transformations and cleaning decisions
- Use appropriate dtypes to optimize memory with large datasets
- Consider chunking or sampling for initial exploration of `flights.csv`
- Validate foreign key relationships between datasets

### Feature Engineering
Consider creating:
- Time-based features (time of day, day of week, month, season)
- Holiday indicators
- Route-based features (distance, frequency)
- Weather-related features (from external data)
- Airport/airline aggregated statistics

### Documentation
- Save visualizations to `docs/eda_plots/`
- Document insights in `docs/eda_report.md`
- Save cleaned datasets to `data/processed/`
- Document all assumptions and decisions
- Include limitations and improvement suggestions

## Tech Stack

- **Python 3.8+**
- **Data**: pandas, numpy
- **ML**: scikit-learn, XGBoost, LightGBM
- **Viz**: matplotlib, seaborn, plotly
- **Notebooks**: Jupyter

## Deliverables

1. GitHub repository with complete code
2. Video presentation (5-10 minutes) explaining work, results, and conclusions
3. Critical analysis of results, limitations, and next steps
