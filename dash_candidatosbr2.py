import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configurando a página para usar a largura total
st.set_page_config(layout="wide")

# Sidebar para navegação
page = st.sidebar.selectbox("Selecione a página", ["Prefeitos", "Vereadores"])

if page == "Prefeitos":
    # Título da página
    st.title('Dados sobre Candidaturas a Prefeituras nas Eleições de 2024')
    
    st.markdown("""
    ### Análise dos Dados Eleitorais de 2024

    Esta análise foi realizada utilizando dados do TSE de 2024, coletados em 21 de agosto de 2024. 
    O tratamento e a disposição dos dados foram feitos utilizando Python, Streamlit e outras bibliotecas de visualização e tratamento de dados.

    #### Autor
    Christian Basilio, Gestor Público pela UFRJ e Pós-Graduando em Comunicação Política e Sociedade na ESPM.
    """)

    st.sidebar.markdown("""
    ### Contato
    - Email: [Christianbasilio97@gmail.com](mailto:Christianbasilio97@gmail.com)
    - LinkedIn: [linkedin.com/in/christianbasilio](https://www.linkedin.com/in/christianbasilioo/)
    """)
    # Subtítulo para a seção de candidaturas por cor
    st.subheader('Candidaturas a Prefeituras por Cor nas Eleições de 2024')
    
    # Carregando a base de dados de cor e prefeitura
    pref_cor = pd.read_csv('base_dashboard/bens_vereador_agregado_cor.csv')
    pref_cor.columns = ['Cor', 'Candidatos', 'Total', 'Media', 'Mediana']
    
    # Criando o percentual de candidatos
    pref_cor['Percentual'] = ((pref_cor['Candidatos'] / pref_cor['Candidatos'].sum() * 100).round(2)).astype(str) + '%'
    
     # Função para formatar os valores com unidades
    def format_value(value):
        return f'R${value:,.2f}'

    # Aplicando a formatação aos dados
    pref_cor['Media'] = pref_cor['Media'].apply(format_value)
    pref_cor['Mediana'] = pref_cor['Mediana'].apply(format_value)
    
    # Criando gráfico interativo com plotly de contagem de candidaturas por cor
    fig_cor_pref = px.bar(
        pref_cor, 
        x='Cor', 
        y='Candidatos', 
        labels={'Candidatos': 'Número de Candidatos', 'Cor': 'Cor'},
        color='Cor', 
        color_discrete_sequence=px.colors.qualitative.Set3,
        hover_data={'Percentual': True}  # Adicionando a coluna Percentual ao hover data
    )
    
    # Atualizando o layout do gráfico
    fig_cor_pref.update_layout(
        title={
            'text': 'Candidaturas a Prefeitura por Cor nas Cidades Brasileiras em 2024',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=12)
        },
        height=500,
        legend=dict(
            x=1,
            xanchor='center',
            y=0.5,
            yanchor='middle'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    # Criando gráfico interativo com plotly de total de bens por cor
    fig_bens_cor = px.bar(
        pref_cor, 
        x='Cor', 
        y='Total', 
        labels={'Total': 'Total de Bens', 'Cor': 'Cor'},
        color='Cor', 
        color_discrete_sequence=px.colors.qualitative.Set3, 
        hover_data={'Media': True, 'Mediana': True}
    )
    
    # Removendo o texto das barras
    fig_bens_cor.update_traces(texttemplate='')
    
    # Atualizando o layout do gráfico
    fig_bens_cor.update_layout(
        title={
            'text': 'Bens declarados em (R$) de candidatos a Prefeitura por Cor nas Cidades Brasileiras em 2024',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=12)
        },
        height=500,
        legend=dict(
            x=1,
            xanchor='center',
            y=0.5,
            yanchor='middle'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    # Colocando os gráficos lado a lado
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_cor_pref, use_container_width=True)
    with col2:
        st.plotly_chart(fig_bens_cor, use_container_width=True)

    # Carregando a base de dados de gênero e cor
    genero_cor = pd.read_csv('base_dashboard/bens_vereador_agregado_cor_genero.csv')
    genero_cor.columns = ['Cor', 'Genero', 'Candidatos', 'Total', 'Media', 'Mediana']
    
    # Formatando os valores de média e mediana para exibição
    genero_cor['Media_format'] = genero_cor['Media'].apply(format_value)
    genero_cor['Mediana_format'] = genero_cor['Mediana'].apply(format_value)
    
    # Criando gráfico interativo com plotly de mediana dos bens por cor e gênero
    fig_bens_cor_genero = px.bar(
        genero_cor, 
        x='Cor', 
        y='Mediana', 
        labels={'Total': 'Total de Bens', 'Cor': 'Cor'},
        color='Genero', 
        color_discrete_sequence=px.colors.qualitative.Set3, 
        hover_data={'Media_format': True, 'Mediana_format': True},
        barmode='group' 
    )
    
    # Removendo o texto das barras
    fig_bens_cor_genero.update_traces(texttemplate='')
    
    # Atualizando o layout do gráfico
    fig_bens_cor_genero.update_layout(
        title={
            'text': 'Mediana dos Bens Declarados por Cor e Gênero dos Candidatos a Prefeito nas Eleições de 2024',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=15)
        },
        legend=dict(
            x=1,
            xanchor='center',
            y=0.5,
            yanchor='middle'
        ),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin={"r":10,"t":10,"l":10,"b":10}
    )
    
    # Atualizando os dados exibidos no hover
    fig_bens_cor_genero.update_traces(
        hovertemplate='Total de Bens: %{y:.2f}<br>Média: %{customdata[0]}<br>Mediana: %{customdata[1]}'
    )
    
    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig_bens_cor_genero, use_container_width=True)
    
    # Subtítulo para a seção de lista de candidatos
    st.subheader('Lista de Candidatos a Prefeito em 2024')
    
    # Carregando a base de dados de candidatos a prefeito
    df_cand_itens = pd.read_csv('consulta_cand_2024_BRASIL.csv', sep=';', encoding='latin1')

    # Filtrar apenas os cargos de prefeito e selecionar as colunas desejadas
    df_cand_itens = df_cand_itens[df_cand_itens['DS_CARGO'] == 'PREFEITO'][['NM_URNA_CANDIDATO', 'DS_COR_RACA', 'DS_OCUPACAO', 'DS_GRAU_INSTRUCAO', 'DS_GENERO', 'SG_PARTIDO', 'NM_UE', 'SG_UF', 'DS_CARGO']]

    # Melhorar o nome das colunas
    df_cand_itens.columns = ['Nome', 'Cor', 'Profissão', 'Grau de Instrução', 'Gênero', 'Partido', 'Cidade', 'UF', 'Cargo']

    # Opções de filtro por estado, cidade, partido e gênero
    estado_options = sorted(df_cand_itens['UF'].unique())
    partido_options = sorted(df_cand_itens['Partido'].unique())
    genero_options = sorted(df_cand_itens['Gênero'].unique())
    
    # Criando colunas para os filtros
    col1, col2 = st.columns(2)
    
    with col1:
        estado_filter = st.multiselect('Estado', options=estado_options)
    
    # Filtrando as cidades com base no estado selecionado
    if estado_filter:
        cidade_options = sorted(df_cand_itens[df_cand_itens['UF'].isin(estado_filter)]['Cidade'].unique())
    else:
        cidade_options = sorted(df_cand_itens['Cidade'].unique())
    
    with col2:
        cidade_filter = st.multiselect('Cidade', options=cidade_options)
    
    col3, col4 = st.columns(2)
    
    with col3:
        partido_filter = st.multiselect('Partido', options=partido_options)
    
    with col4:
        genero_filter = st.multiselect('Gênero', options=genero_options)
    
    # Filtrando os dados com base nos filtros selecionados
    filtered_data = df_cand_itens
    if estado_filter:
        filtered_data = filtered_data[filtered_data['UF'].isin(estado_filter)]
    if cidade_filter:
        filtered_data = filtered_data[filtered_data['Cidade'].isin(cidade_filter)]
    if partido_filter:
        filtered_data = filtered_data[filtered_data['Partido'].isin(partido_filter)]
    if genero_filter:
        filtered_data = filtered_data[filtered_data['Gênero'].isin(genero_filter)]

    # Contagem total de candidaturas
    total_candidaturas = len(filtered_data)

    # Contagem de candidaturas por cor
    candidaturas_por_cor = filtered_data['Cor'].value_counts()

    # Contagem de candidaturas por partido
    candidaturas_por_partido = filtered_data['Partido'].value_counts()

    # Contagem de candidaturas por gênero
    candidaturas_por_genero = filtered_data['Gênero'].value_counts()

    # Exibindo as contagens no Streamlit organizadamente
    st.markdown(f"### Total de Candidaturas: {total_candidaturas}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### Candidaturas por Cor:")
        fig_cor = px.pie(candidaturas_por_cor, names=candidaturas_por_cor.index, values=candidaturas_por_cor.values, labels={'names': 'Cor', 'values': 'Contagem'})
        st.plotly_chart(fig_cor)

    with col2:
        st.markdown("##### Candidaturas por Partido:")
        fig_partido_prefeitos = px.bar(
            candidaturas_por_partido, 
            x=candidaturas_por_partido.values, 
            y=candidaturas_por_partido.index, 
            orientation='h', 
            labels={'x': 'Contagem', 'y': 'Partido'},
            color=candidaturas_por_partido.index,  # Adiciona cores diferentes para cada partido
            color_discrete_sequence=px.colors.qualitative.Set3  # Escolhe uma paleta de cores
        )
        fig_partido_prefeitos.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=800,  # Ajuste a altura conforme necessário
            bargap=0.1,  # Ajuste o espaçamento entre as barras (0 a 1)
            title="Candidaturas por Partido",
            xaxis_title="Contagem",
            yaxis_title="Partido"
        )
        fig_partido_prefeitos.update_traces(texttemplate='%{x}', textposition='outside')
        st.plotly_chart(fig_partido_prefeitos)

    with col3:
        st.markdown("##### Candidaturas por Gênero:")
        fig_genero = px.pie(candidaturas_por_genero, names=candidaturas_por_genero.index, values=candidaturas_por_genero.values, labels={'names': 'Gênero', 'values': 'Contagem'})
        st.plotly_chart(fig_genero)

    # Exibindo os dados filtrados em uma tabela
    if not filtered_data.empty:
        st.dataframe(filtered_data.style.format({'Total de Bens': 'R$ {:,.2f}'}), height=300)
    else:
        st.write("Nenhum dado encontrado para os filtros selecionados.")


elif page == "Vereadores":
    # Título da página para vereadores
    st.title('Dados sobre Candidaturas a Vereadores nas Eleições de 2024')

    st.markdown("""
    ### Análise dos Dados Eleitorais de 2024

    Esta análise foi realizada utilizando dados do TSE de 2024, coletados em 21 de agosto de 2024. 
    O tratamento e a disposição dos dados foram feitos utilizando Python, Streamlit e outras bibliotecas de visualização e tratamento de dados.

    #### Autor
    Christian Basilio, Gestor Público pela UFRJ e Pós-Graduando em Comunicação Política e Sociedade na ESPM.
    """)

    # Subtítulo para a seção de candidaturas por cor
    st.subheader('Candidaturas a Vereadores por Cor nas Eleições de 2024')
    
    # Carregando a base de dados de cor e vereador
    ver_cor = pd.read_csv('base_dashboard/bens_vereador_agregado_cor.csv')
    ver_cor.columns = ['Cor', 'Candidatos', 'Total', 'Media', 'Mediana']
    
    # Criando o percentual de candidatos
    ver_cor['Percentual'] = ((ver_cor['Candidatos'] / ver_cor['Candidatos'].sum() * 100).round(2)).astype(str) + '%'
    
    # Criando gráfico interativo com plotly de contagem de candidaturas por cor
    fig_cor_ver = px.bar(
        ver_cor, 
        x='Cor', 
        y='Candidatos', 
        labels={'Candidatos': 'Número de Candidatos', 'Cor': 'Cor'},
        color='Cor', 
        color_discrete_sequence=px.colors.qualitative.Set3,
        hover_data={'Percentual': True}  # Adicionando a coluna Percentual ao hover data
    )
    
    # Atualizando o layout do gráfico
    fig_cor_ver.update_layout(
        title={
            'text': 'Candidaturas a Vereador por Cor nas Cidades Brasileiras em 2024',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=15)
        },
        height=500,
        legend=dict(
            x=1,
            xanchor='center',
            y=0.5,
            yanchor='middle'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    # Função para formatar os valores com unidades
    def format_value(value):
        if value >= 1e9:
            return f'{value / 1e9:.2f} Bilhão'
        elif value >= 1e6:
            return f'{value / 1e6:.2f} Milhão'
        elif value >= 1e3:
            return f'{value / 1e3:.2f} Mil'
        else:
            return f'{value:.2f}'
    
    # Aplicando a formatação aos dados
    ver_cor['Media'] = ver_cor['Media'].apply(format_value)
    
    # Criando gráfico interativo com plotly de total de bens por cor
    fig_bens_cor = px.bar(
        ver_cor, 
        x='Cor', 
        y='Total', 
        labels={'Total': 'Total de Bens', 'Cor': 'Cor'},
        color='Cor', 
        color_discrete_sequence=px.colors.qualitative.Set3, 
        hover_data={'Media': True},  # Usando os dados formatados
    )
    
    # Removendo o texto das barras
    fig_bens_cor.update_traces(texttemplate='')
    
    # Atualizando o layout do gráfico
    fig_bens_cor.update_layout(
        title={
            'text': 'Bens declarados em (R$) de candidatos a Vereador por Cor nas Cidades Brasileiras em 2024',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=12)
        },
        height=500,
        legend=dict(
            x=1,
            xanchor='center',
            y=0.5,
            yanchor='middle'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    # Colocando os gráficos lado a lado
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_cor_ver, use_container_width=True)
    with col2:
        st.plotly_chart(fig_bens_cor, use_container_width=True)
    
    # Carregando a base de dados de gênero e cor
    genero_cor = pd.read_csv('base_dashboard/bens_vereador_agregado_cor_genero.csv')
    genero_cor.columns = ['Cor', 'Genero', 'Candidatos', 'Total', 'Media', 'Mediana']
    
    # Criando gráfico interativo com plotly de total de candidaturas por raça e gênero
    fig_genero_cor_ver = px.bar(
        genero_cor, 
        x='Cor', 
        y='Candidatos', 
        labels={'Candidatos': 'Número de Candidatos', 'Cor': 'Cor'},
        color='Genero', 
        color_discrete_sequence=px.colors.qualitative.Set3,
        barmode='group'  # Configurando para barras agrupadas
    )
    
    # Atualizando o layout do gráfico
    fig_genero_cor_ver.update_layout(
        title={
            'text': 'Total de Candidaturas por Raça e Gênero nas Eleições de 2024',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=15)
        },
        legend=dict(
            x=1,
            xanchor='center',
            y=0.5,
            yanchor='middle'
        ),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig_genero_cor_ver, use_container_width=True)
    
    # Formatando os valores de média e mediana para exibição
    genero_cor['Media_format'] = genero_cor['Media'].apply(format_value)
    genero_cor['Mediana_format'] = genero_cor['Mediana'].apply(format_value)
    
    # Criando gráfico interativo com plotly de mediana dos bens por cor e gênero
    fig_bens_cor_genero = px.bar(
        genero_cor, 
        x='Cor', 
        y='Mediana', 
        labels={'Total': 'Total de Bens', 'Cor': 'Cor'},
        color='Genero', 
        color_discrete_sequence=px.colors.qualitative.Set3, 
        hover_data={'Media_format': True, 'Mediana_format': True},
        barmode='group' 
    )
    
    # Removendo o texto das barras
    fig_bens_cor_genero.update_traces(texttemplate='')
    
    # Atualizando o layout do gráfico
    fig_bens_cor_genero.update_layout(
        title={
            'text': 'Mediana dos Bens Declarados por Cor e Gênero dos Candidatos a Vereador nas Eleições de 2024',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=15)
        },
        legend=dict(
            x=1,
            xanchor='center',
            y=0.5,
            yanchor='middle'
        ),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin={"r":10,"t":10,"l":10,"b":10}
    )
    
    # Atualizando os dados exibidos no hover
    fig_bens_cor_genero.update_traces(
        hovertemplate='Total de Bens: %{y:.2f}<br>Média: %{customdata[0]}<br>Mediana: %{customdata[1]}'
    )
    
    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig_bens_cor_genero, use_container_width=True)
    
    # Subtítulo para a seção de lista de candidatos
    st.subheader('Lista de Candidatos a Vereador em 2024')
    
    # Carregando a base de dados de candidatos a vereador
    df_cand_itens = pd.read_csv('consulta_cand_2024_BRASIL.csv', sep=';', encoding='latin1')

    # Filtrar apenas os cargos de vereador e selecionar as colunas desejadas
    df_cand_itens = df_cand_itens[df_cand_itens['DS_CARGO'] == 'VEREADOR'][['NM_URNA_CANDIDATO', 'DS_COR_RACA', 'DS_OCUPACAO', 'DS_GRAU_INSTRUCAO', 'DS_GENERO', 'SG_PARTIDO', 'NM_UE', 'SG_UF', 'DS_CARGO']]

    # Melhorar o nome das colunas
    df_cand_itens.columns = ['Nome', 'Cor', 'Profissão', 'Grau de Instrução', 'Gênero', 'Partido', 'Cidade', 'UF', 'Cargo']

    estado_options = sorted(df_cand_itens['UF'].unique())
    partido_options = sorted(df_cand_itens['Partido'].unique())
    genero_options = sorted(df_cand_itens['Gênero'].unique())
    
    # Criando colunas para os filtros
    col1, col2 = st.columns(2)
    
    with col1:
        estado_filter = st.multiselect('Estado', options=estado_options)
    
    # Filtrando as cidades com base no estado selecionado
    if estado_filter:
        cidade_options = sorted(df_cand_itens[df_cand_itens['UF'].isin(estado_filter)]['Cidade'].unique())
    else:
        cidade_options = sorted(df_cand_itens['Cidade'].unique())
    
    with col2:
        cidade_filter = st.multiselect('Cidade', options=cidade_options)
    
    col3, col4 = st.columns(2)
    
    with col3:
        partido_filter = st.multiselect('Partido', options=partido_options)
    
    with col4:
        genero_filter = st.multiselect('Gênero', options=genero_options)
    
    # Filtrando os dados com base nos filtros selecionados
    filtered_data = df_cand_itens
    if estado_filter:
        filtered_data = filtered_data[filtered_data['UF'].isin(estado_filter)]
    if cidade_filter:
        filtered_data = filtered_data[filtered_data['Cidade'].isin(cidade_filter)]
    if partido_filter:
        filtered_data = filtered_data[filtered_data['Partido'].isin(partido_filter)]
    if genero_filter:
        filtered_data = filtered_data[filtered_data['Gênero'].isin(genero_filter)]

    # Contagem total de candidaturas
    total_candidaturas = len(filtered_data)

    # Contagem de candidaturas por cor
    candidaturas_por_cor = filtered_data['Cor'].value_counts()

    # Contagem de candidaturas por partido
    candidaturas_por_partido = filtered_data['Partido'].value_counts()

    # Contagem de candidaturas por gênero
    candidaturas_por_genero = filtered_data['Gênero'].value_counts()

    # Exibindo as contagens no Streamlit organizadamente
    st.markdown(f"### Total de Candidaturas: {total_candidaturas}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### Candidaturas por Cor:")
        fig_cor = px.pie(candidaturas_por_cor, names=candidaturas_por_cor.index, values=candidaturas_por_cor.values, labels={'names': 'Cor', 'values': 'Contagem'})
        st.plotly_chart(fig_cor)

    with col2:
        st.markdown("##### Candidaturas por Partido:")
        fig_partido = px.bar(
            candidaturas_por_partido, 
            x=candidaturas_por_partido.values, 
            y=candidaturas_por_partido.index, 
            orientation='h', 
            labels={'x': 'Contagem', 'y': 'Partido'},
            color=candidaturas_por_partido.index,  # Adiciona cores diferentes para cada partido
            color_discrete_sequence=px.colors.qualitative.Set3  # Escolhe uma paleta de cores
        )
        fig_partido.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=800,  # Ajuste a altura conforme necessário
            bargap=0.1,  # Ajuste o espaçamento entre as barras (0 a 1)
            title="Candidaturas por Partido",
            xaxis_title="Contagem",
            yaxis_title="Partido"
        )
        fig_partido.update_traces(texttemplate='%{x}', textposition='outside')  # Adiciona rótulos nas barras
        st.plotly_chart(fig_partido)

    with col3:
        st.markdown("##### Candidaturas por Gênero:")
        fig_genero = px.pie(candidaturas_por_genero, names=candidaturas_por_genero.index, values=candidaturas_por_genero.values, labels={'names': 'Gênero', 'values': 'Contagem'})
        st.plotly_chart(fig_genero)

    # Exibindo os dados filtrados em uma tabela
    if not filtered_data.empty:
        # Limitar a visualização inicial para 100 registros
        st.dataframe(filtered_data.head(15000).style.format({'Total de Bens': 'R$ {:,.2f}'}), height=600)
    else:
        st.write("Nenhum dado encontrado para os filtros selecionados.")