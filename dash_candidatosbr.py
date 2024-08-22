# Criando o dashboard com streamlit
# Autor: Christian Basilio

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd

# Carregando os dados brasil shape em base_dashboard (shapefile)
mapaGeneroUF = gpd.read_file('base_dashboard/brasil_genero.shp')

st.title('Dados sobre Candidaturas a Prefeituras nas Eleições de 2024')
st.subheader('Candidaturas a Prefeituras por Cor nas Eleições de 2024')
# Base de cor e prefeitura -----------------

# Criando subtitulo para o dashboard falando que os dados sao sobre cor
pref_cor = pd.read_csv('base_dashboard/bens_pref_agregado_cor.csv')
pref_cor.columns = ['Cor', 'Candidatos', 'Total', 'Media', 'Mediana']

# criando o perfencutal de candidatos
pref_cor['Percentual'] = ((pref_cor['Candidatos'] / pref_cor['Candidatos'].sum() * 100).round(2)).astype(str) + '%'



# Criando aba de apresentação de Dados sobre candidaturas a prefeito


# Criando grafico interativo com plotly de contagem de candidaturas por cor
fig_cor_pref = px.bar(pref_cor, x='Cor', y='Candidatos', labels={'Candidatos': 'Número de Candidatos', 'Cor': 'Cor'},
             color='Cor', color_discrete_sequence=px.colors.qualitative.Set3,
                 hover_data={'Percentual': True}  # Adicionando a coluna Percentual ao hover data
)

fig_cor_pref.update_layout(
    title={
        'text': 'Candidaturas a Prefeitura por Cor nas Cidades Brasileiras nas Eleições de 2024',
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

fig_cor_pref.update_geos(fitbounds="locations", visible=False)
fig_cor_pref.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_cor_pref)

# Segundo GRAFICO ----------------------------------------------
# Criando grafico interativo com plotly de total de bens por cor
# Função para formatar os valores com unidades
def format_value(value):
    if value >= 1e9:
        return f'{value / 1e9:.2f} Bilhão'
    elif value >= 1e6:
        return f'{value / 1e6:.2f} Milhão'
    else:
        return f'{value:.2f}'

# Aplicando a formatação aos dados
pref_cor['Media_format'] = pref_cor['Media'].apply(format_value)
pref_cor['Mediana_format'] = pref_cor['Mediana'].apply(format_value)

# Criando grafico interativo com plotly de total de bens por cor
fig_bens_cor = px.bar(
    pref_cor, 
    x='Cor', 
    y='Total', 
    labels={'Total': 'Total de Bens', 'Cor': 'Cor'},
    color='Cor', 
    color_discrete_sequence=px.colors.qualitative.Set3, 
    hover_data={'Media_format': True, 'Mediana_format': True},  # Usando os dados formatados
    title='Total de Bens Declarados por Cor dos Candidatos a Prefeito nas Eleições de 2024'
)

# Removendo o texto das barras
fig_bens_cor.update_traces(texttemplate='')

fig_bens_cor.update_layout()

st.plotly_chart(fig_bens_cor)

# Terceiro GRAFICO ----------------------------------------------
# Criando grafico interativo com plotly de contagem de candidaturas por genero
genero = pd.read_csv('base_dashboard/bens_pref_agregado_genero.csv')

genero.columns = ['Genero', 'Candidatos', 'Total', 'Media', 'Mediana']
# criando o percentual
genero['Percentual'] = ((genero['Candidatos'] / genero['Candidatos'].sum() * 100).round(2)).astype(str) + '%'

# criando o grafico interativo no plotly sobre genero e contagem
fig_genero_pref = px.bar(genero, x='Genero', y='Candidatos', labels={'Candidatos': 'Número de Candidatos', 'Genero': 'Genero'},
             color='Genero', color_discrete_sequence=px.colors.qualitative.Set3, hover_data=['Percentual'])
# colocando o titulo e ajustando o popup para ter o percentual
fig_genero_pref.update_layout(
    title={
        'text': 'Candidaturas a Prefeitura por Gênero nas Cidades Brasileiras nas Eleições de 2024',
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

fig_genero_pref.update_geos(fitbounds="locations", visible=False)
fig_genero_pref.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_genero_pref)



# criando o mapa no streamlit
st.title('Mapa % de candidaturas a Prefeitura Femininas por UF')

# criando o mapa interativo com plotly
fig = px.choropleth(mapaGeneroUF, geojson=mapaGeneroUF.geometry, locations=mapaGeneroUF.index, color='% FEMININO',
                    color_continuous_scale="Viridis",
                    range_color=(0, 0.3),
                    scope="south america",
                    labels={'% FEMININO': '% Feminino'}
                   )
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)