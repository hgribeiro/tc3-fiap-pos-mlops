# %%
#Bibliotecas 

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

# %%


# %%
# Leitura do banco de dados - pesquisa de um shopping 

df = pd.read_csv("./data/airpots.csv")


# %%
df.head()

# %% [markdown]
# Primeiras análises do dataset 

# %%
df.shape

# %%
df.isna().sum()

# %%
df['UF']

# %%
contagem_distintos = df['UF'].value_counts()
contagem_distintos

# %%
import matplotlib.pyplot as plt

# Cria o gráfico de barras
plt.figure(figsize=(10, 6))
contagem_distintos.plot(kind='bar', color='blue')

# Adiciona título e rótulos aos eixos
plt.title('Contagem de Informações Distintas na Coluna DF', fontsize=16)
plt.xlabel('Informações Distintas', fontsize=14)
plt.ylabel('Contagem', fontsize=14)

# Exibe o gráfico
plt.tight_layout()
plt.show()


# %%
# Vamos limpar o banco de dados 

# Dicionário de renomeação
rename_dict = {
    'V0101': 'ano',
    'V0302': 'sexo',
    'V8005': 'idade',
    'V0404': 'cor',
    'V4803': 'faixa_etaria',
    'V4720': 'salario'
}

# Renomeando as colunas
df_renomeado = df.rename(columns=rename_dict)

# Exibir as novas colunas
df_renomeado.columns.tolist()


# %%
# Excluindo as colunas 'V4718' e 'V4729'
df_renomeado = df_renomeado.drop(columns=['V4718', 'V4729'])

# %%
df_renomeado.head(1)

# %%
df_renomeado.sexo

# %%
df_renomeado.sexo.value_counts()

# %%
df_renomeado.sexo.value_counts() / df_renomeado.shape[0]

# %%
# Cor da pele
df_renomeado.cor.value_counts() / df.shape[0]

# %%
# Idade 

df_renomeado.idade.head()

# %%
#pnad.idade.value_counts()
idade = df_renomeado['idade'].value_counts()
idade

# %%
# Cria o gráfico de barras
plt.figure(figsize=(10, 6))
idade.plot(kind='bar', color='blue')

# Adiciona título e rótulos aos eixos
plt.title('Contagem de Informações Distintas na Coluna DF', fontsize=16)
plt.xlabel('Informações Distintas', fontsize=14)
plt.ylabel('Contagem', fontsize=14)

# Exibe o gráfico
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt

# Cria o gráfico de barras apenas com os 30 primeiros valores
plt.figure(figsize=(10, 6))
idade.head(30).plot(kind='bar', color='blue')

# Adiciona título e rótulos aos eixos
plt.title('Contagem de Informações Distintas na Coluna IDADE (Top 30)', fontsize=16)
plt.xlabel('Informações Distintas', fontsize=14)
plt.ylabel('Contagem', fontsize=14)

# Exibe o gráfico
plt.tight_layout()
plt.show()


# %%
df_renomeado.idade.mean() # média

# %%
df_renomeado.idade.median() # mediana

# %%
df_renomeado.idade.var() # variância

# %%
df_renomeado.idade.std() # desvio padrão

# %%
# Tirando várias estatísticas descritivas de uma só vez
df_renomeado.idade.describe()

# %%
df_renomeado.describe()

# %%
df_renomeado.describe(include='all')

# %%
df_renomeado.dtypes

# %%
# Transformar salario em float
df_renomeado['salario'] = pd.to_numeric(df_renomeado['salario'], errors='coerce')

# %%
df_renomeado.describe()

# %%
import matplotlib.pyplot as plt
import seaborn as sns

# %%
sns.set(style='whitegrid')

# %%
plt.scatter(df_renomeado.idade, df_renomeado.salario)
plt.title("Interação entre idade e renda")
plt.show()

# %%
#SexoCorrigindo o código para contar os valores da coluna 'V0302'
sns.countplot(x='sexo', data=df_renomeado)
plt.title("Sexo")
plt.xlabel("")
plt.ylabel("Frequência")
plt.show()

# %%
# Cor da pele
sns.countplot(x='cor', data=df_renomeado)
plt.title("Cor da Pele")
plt.show()

# %%
sns.countplot(x='cor', hue='sexo', data=df_renomeado)
plt.title("Distribuição por cor e separado por Sexo")
plt.show()

# %%
sns.countplot(x='sexo', hue='cor', data=df_renomeado)
plt.title("Distribuição por sexo e Separado por cor")
plt.show()

# %% [markdown]
# Tratando a variável renda de todos os trabalhos

# %%
amostra = df_renomeado.loc[ (df_renomeado.idade >= 18) & (df_renomeado.idade <= 80) & (df_renomeado.salario > 0) ]

# %%
amostra.describe()

# %%
amostra.groupby('sexo').agg({'salario' : 'mean'})

# %%
amostra.groupby('cor').agg({'salario' : 'mean'})

# %%
amostra.groupby(['cor', 'sexo']).agg({'salario' : 'mean'})

# %%
plt.scatter(amostra.idade, amostra.salario)
plt.show()

# %%
dado = amostra.groupby('idade').agg({'salario' : 'mean'})
dado.reset_index(inplace=True)
dado

# %%
plt.figure(figsize=(10,5))
plt.scatter(x=dado.idade, y=dado.salario)
plt.xlabel('Idade')
plt.ylabel('Média da renda')
plt.show()


