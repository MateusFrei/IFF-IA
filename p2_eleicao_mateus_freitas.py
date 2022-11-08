# -*- coding: utf-8 -*-
"""P2_Eleicao_Mateus_Freitas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qsPb0f31io9eX8VvZKVLNDhOEJekRnSM

P2 - Mateus Freitas

##Importando Bibliotecas
"""

import pandas as pd
import numpy 
#graticos
import seaborn as sns
import plotly.express as px

#treinamento RNR
import sys
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.layers import Embedding, SpatialDropout1D
import math
import pandas_datareader as web
import matplotlib.pyplot as plt
from keras.utils import np_utils

"""##Lendo a base de dados"""

from google.colab import drive
drive.mount('/content/drive')

candidatos = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/P2/Mateus da Silva Freitas - consulta_cand_2020_RJ.csv',sep=';' ,encoding='ISO-8859-1')
receitas = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/P2/Mateus da Silva Freitas - receitas_candidatos_2020_RJ.csv',sep=';' ,encoding='ISO-8859-1')
despesas = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/P2/Mateus da Silva Freitas - despesas_contratadas_candidatos_2020_RJ.csv',sep=';' ,encoding='ISO-8859-1')

candidatos.info()

receitas.info()

despesas.info()



"""##Analise exploratória dos dados"""

candidatos = candidatos.drop(['HH_GERACAO', 'ANO_ELEICAO', 'CD_TIPO_ELEICAO', 'CD_GENERO', 'CD_OCUPACAO',
       'NM_TIPO_ELEICAO', 'CD_ELEICAO', 'DS_ELEICAO', 'DT_ELEICAO', 'TP_ABRANGENCIA', 'ST_DECLARAR_BENS', 'SG_UF',
       'SQ_CANDIDATO', 'NM_URNA_CANDIDATO', 'NM_SOCIAL_CANDIDATO', 'CD_SITUACAO_CANDIDATURA', 'DS_SITUACAO_CANDIDATURA',
       'CD_DETALHE_SITUACAO_CAND', 'DS_DETALHE_SITUACAO_CAND', 'SG_PARTIDO', 'SQ_COLIGACAO', 'NM_COLIGACAO',
       'DS_NACIONALIDADE', 'SG_UF_NASCIMENTO', 'CD_MUNICIPIO_NASCIMENTO', 'NM_MUNICIPIO_NASCIMENTO', 'DT_GERACAO', 'DT_NASCIMENTO',
       'NR_TITULO_ELEITORAL_CANDIDATO', 'CD_GRAU_INSTRUCAO',  'CD_ESTADO_CIVIL', 'CD_COR_RACA', 'NR_TURNO',
       'VR_DESPESA_MAX_CAMPANHA', 'CD_SIT_TOT_TURNO', 'ST_REELEICAO', 'NR_PROTOCOLO_CANDIDATURA', 'NR_PROCESSO',
       'CD_SITUACAO_CANDIDATO_PLEITO', 'DS_SITUACAO_CANDIDATO_PLEITO', 'CD_SITUACAO_CANDIDATO_URNA', 'DS_SITUACAO_CANDIDATO_URNA',
       'ST_CANDIDATO_INSERIDO_URNA'], axis=1)

candidatos.columns



"""##Carregando dados do Municipio e cargo

dataframe contento somente candisatos a vereadores de campos dos goytacazes
"""

df_candidato_mun = candidatos

df_candidato_mun = candidatos.loc[candidatos['NM_UE'] == 'CAMPOS DOS GOYTACAZES']

df_candidato_mun = df_candidato_mun.loc[df_candidato_mun['DS_CARGO'] == 'VEREADOR']



df_receita_mun = receitas

df_receita_mun = receitas.loc[receitas['NM_UE'] == 'CAMPOS DOS GOYTACAZES']

df_receita_mun = df_receita_mun.loc[df_receita_mun['DS_CARGO'] == 'Vereador']



df_despesa_mun = despesas

df_despesa_mun = despesas.loc[despesas['NM_UE'] == 'CAMPOS DOS GOYTACAZES']

df_despesa_mun = df_despesa_mun.loc[df_despesa_mun['DS_CARGO'] == 'Vereador']



"""##Realizando o somatorio das receitas e despesas

Somatorio das Receitas
"""

df_receita_mun['VR_RECEITA'] = df_receita_mun['VR_RECEITA'].apply(lambda x: float(x.split()[0].replace(',', '.')))
df_despesa_mun['VR_DESPESA_CONTRATADA'] = df_despesa_mun['VR_DESPESA_CONTRATADA'].apply(lambda x: float(x.split()[0].replace(',', '.')))

cpf_candidatos = df_candidato_mun['NR_CPF_CANDIDATO']


somatorio_receitas = pd.DataFrame([], columns = ['NR_CPF_CANDIDATO', 'VR_RECEITA'])
cpf_receitas = df_receita_mun.loc[:, df_receita_mun.columns.intersection(['NR_CPF_CANDIDATO','VR_RECEITA'])]

for cpf in cpf_candidatos:
  receitas_por_cpf = cpf_receitas[cpf_receitas['NR_CPF_CANDIDATO'] == cpf]
  somatorio = receitas_por_cpf['VR_RECEITA'].sum()
  new_value = pd.Series(data=[cpf, somatorio], index=['NR_CPF_CANDIDATO', 'VR_RECEITA'])
  somatorio_receitas = somatorio_receitas.append(new_value, ignore_index=True)

somatorio_receitas

"""Somatorio das despesas"""

cpf_candidatos = df_candidato_mun['NR_CPF_CANDIDATO']


somatorio_despesas = pd.DataFrame([], columns = ['NR_CPF_CANDIDATO', 'VR_DESPESA_CONTRATADA'])
cpf_despesas = df_despesa_mun.loc[:, df_despesa_mun.columns.intersection(['NR_CPF_CANDIDATO','VR_DESPESA_CONTRATADA'])]

for cpf in cpf_candidatos:
  despesas_por_cpf = cpf_despesas[cpf_despesas['NR_CPF_CANDIDATO'] == cpf]
  somatorio = despesas_por_cpf['VR_DESPESA_CONTRATADA'].sum()
  new_value = pd.Series(data=[cpf, somatorio], index=['NR_CPF_CANDIDATO', 'VR_DESPESA_CONTRATADA'])
  somatorio_despesas = somatorio_despesas.append(new_value, ignore_index=True)

somatorio_despesas

vereadores_receita_despesa = pd.merge(df_candidato_mun, somatorio_receitas, on='NR_CPF_CANDIDATO', how='left')
vereadores_receita_despesa = pd.merge(vereadores_receita_despesa, somatorio_despesas, on='NR_CPF_CANDIDATO', how='left')
vereadores_receita_despesa

vereadores_receita_despesa.columns

"""##Graficos da base



"""

#idades 
sns.set(rc={'figure.figsize':(25,10)})
sns.set_style('whitegrid')
sns.countplot(x='NR_IDADE_DATA_POSSE',hue='CD_CARGO',data=vereadores_receita_despesa,palette='Greys_r')

#Escolaridade por cargo
sns.set(rc={'figure.figsize':(25,10)})
sns.set_style('whitegrid')
sns.countplot(x='DS_GRAU_INSTRUCAO',hue='CD_CARGO',data=vereadores_receita_despesa,palette='Greys_r')

#Etnis por cargo
sns.set(rc={'figure.figsize':(10,10)})
sns.set_style('whitegrid')
sns.countplot(x='DS_COR_RACA',hue='CD_CARGO',data=vereadores_receita_despesa,palette='Greys_r')

#Escolaridade por etinia
sns.set(rc={'figure.figsize':(25,10)})
sns.set_style('whitegrid')
sns.countplot(x='DS_GRAU_INSTRUCAO',hue='DS_COR_RACA',data=vereadores_receita_despesa,palette='Greys_r')

#Genero por cargo
sns.set(rc={'figure.figsize':(10,10)})
sns.set_style('whitegrid')
sns.countplot(x='DS_GENERO',hue='CD_CARGO',data=vereadores_receita_despesa,palette='Greys_r')

#distribuição de Despesas
fig=px.histogram(vereadores_receita_despesa, x='VR_DESPESA_CONTRATADA',hover_data=vereadores_receita_despesa.columns,)
fig.show()

#Valor da Receita
fig=px.histogram(vereadores_receita_despesa, x='VR_RECEITA',hover_data=vereadores_receita_despesa.columns,)
fig.show()

#Quantidade de candidatos nos partidos
fig=px.histogram(vereadores_receita_despesa, x='NM_PARTIDO',hover_data=vereadores_receita_despesa.columns,)
fig.show()

#Quantidade de mulheres e homens nos partidos
sns.set(rc={'figure.figsize':(50,13)})
sns.set_style('whitegrid')
sns.countplot(x='NM_PARTIDO',hue='DS_GENERO',data=vereadores_receita_despesa,palette='Greys_r')

"""#Preparação dos Dados"""

# Função para transformar os dados em números
def transform(feature):
    le=LabelEncoder()
    vereadores_receita_despesa[feature]=le.fit_transform(vereadores_receita_despesa[feature])
    print(le.classes_)

cat_df=vereadores_receita_despesa.select_dtypes(include='object')
cat_df.columns

#Transformando os dados em números
for col in cat_df.columns:
    transform(col)

vereadores_receita_despesa.columns

# Coluna chave para definir quem foi e não foi eleito
Y = vereadores_receita_despesa['DS_SIT_TOT_TURNO']
Y

vereadores_receita_despesa.drop(['DS_SIT_TOT_TURNO'],axis=1,inplace=True)

# Normaliza os dados com o MinMaxScaler
scaler = MinMaxScaler(feature_range = (0, 1))
df = scaler.fit_transform(vereadores_receita_despesa)

# X normalizado
X = df
X

# Treina a base de dados
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3,random_state=10)

print(X_train.shape,Y_train.shape)
print(X_test.shape,Y_test.shape)



"""#Arquitetura da Rede Neural (RNR ou RNN)"""

# Rede neural LSTM, a camadas densa tem 10 neurônios e softmax como função de ativação
embed_dim = 128
max_fatures = 2000
lstm_out = 196

model = Sequential()
model.add(Embedding(max_fatures, embed_dim,input_length = X.shape[1]))
model.add(SpatialDropout1D(0.4))
model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(10,activation='softmax'))
model.compile(loss = 'sparse_categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
print(model.summary())

# Define o checkpoint
filepath = "weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor = 'loss', verbose = 1, save_best_only = True, mode = 'min')
callbacks_list = [checkpoint]

# Commented out IPython magic to ensure Python compatibility.
# # Mostra o tempo restante
# %%time
# # Treino da rede neural 
# model.fit(X_train, Y_train, epochs = 100, batch_size = 64, callbacks = callbacks_list)



"""#Acurácia do modelo"""

# Resultados da rede neural LTSM
score,acc = model.evaluate(X_test, Y_test, verbose = 2, batch_size = 64)
print("score: %.2f" % (score))
print("acc: %.2f" % (acc))



# determining the name of the file
file_name = 'eleicoes.csv'
  
# saving the excel
vereadores_receita_despesa.to_csv(file_name)