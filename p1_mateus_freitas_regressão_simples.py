# -*- coding: utf-8 -*-
"""P1 - Mateus Freitas - Regressão Simples

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15F4Dw7q1iB3uV1jp-lCWuB149oeNex3N

## Importando Bibliotecas
"""

!pip install scrapy

import numpy as np
from sklearn import datasets
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
import matplotlib.pyplot as plt
import scrapy
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
import csv
from datetime import datetime 
import pandas as pd 
import requests 
from bs4 import BeautifulSoup
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
import pydot
import graphviz

"""## Carregando a Base de dados web"""

url = 'https://www.worldometers.info/world-population/world-population-by-year/'

agent = {"User-Agent":"Mozilla/5.0"}
response = requests.get(url, headers = agent)

soup = BeautifulSoup(response.text, 'lxml')
table = soup.find_all('table')[0]
population_dataf = pd.read_html(str(table), decimal=',', thousands='.')[0]
print(population_dataf)

"""##Análise exploratória"""

plt.figure(figsize=(10, 10))
sns.heatmap(population_dataf.isnull(),yticklabels=False,cbar=False,cmap='viridis')

population_dataf[population_dataf["YearlyChange"].isnull()][["World Population","YearlyChange"]].head(30)

population_dataf[population_dataf["UrbanPop %"].isnull()][["World Population","UrbanPop %"]].head(30)

"""##Preparação dos Dados"""

population_dataf = population_dataf.drop('UrbanPop %', axis = 1)
population_dataf = population_dataf.drop('YearlyChange', axis = 1)

population_dataf = population_dataf.drop(population_dataf[population_dataf['Year'] <= 1927].index)
population_dataf

population_dataf['World Population'] = population_dataf['World Population'].astype(str)
population_dataf['World Population'] = population_dataf['World Population'].str.replace(',', '.')

population_dataf['NetChange'] = population_dataf['NetChange'].astype(str)
population_dataf['NetChange'] = population_dataf['NetChange'].str.replace(',', '.')

population_dataf['UrbanPop'] = population_dataf['UrbanPop'].astype(str)
population_dataf['UrbanPop'] = population_dataf['UrbanPop'].str.replace(',', '.')

population_dataf

"""##Aplicação do modelo Regressão Simples"""

population_dataf.info()

X_pop_world = population_dataf.iloc[:, 0].values
X_pop_world

y_pop_world = population_dataf.iloc[:, 3].values
y_pop_world

X_pop_world.shape

X_pop_world = X_pop_world.reshape(-1,1)
X_pop_world.shape

regressor_pop_world = LinearRegression()
regressor_pop_world.fit(X_pop_world, y_pop_world)

regressor_pop_world.intercept_

regressor_pop_world.coef_

previsoes = regressor_pop_world.predict(X_pop_world)
previsoes

X_pop_world.ravel()



"""##Apresentação dos resultados"""

grafico = px.scatter(x = X_pop_world.ravel(), y = y_pop_world)
grafico.add_scatter(x = X_pop_world.ravel(), y = previsoes, name = 'Regressão')
grafico.show()

