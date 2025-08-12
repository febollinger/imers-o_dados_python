import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Salários na área de dados',
    page_icon='📊',
    layout='centered'
)

#carregar arq. CSV
df = pd.read_csv('https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv')
#exibir 10 primeiros indices
#print(df.head(10))

#Sidebar para filtros
st.sidebar.header('Filtros')

#Todos os anos cadastrados uma vez
todos_os_anos = sorted(df['ano'].unique())
#crio um filtro com os anos disponiveis listados
anos_encontrados = st.sidebar.multiselect('Ano', todos_os_anos, default= todos_os_anos)

# Seleciono todas as senioridades e depois exibo em um sidebar de filtro

senioridades = sorted(df['senioridade'].unique())
senioridades_filtro = st.sidebar.multiselect('Senioridade', senioridades ,default=senioridades)

#Seleciono todos os tipos de contratos e exibo em um sidebar

tipos_de_contratos = sorted(df['contrato'].unique())
filtro_contratos = st.sidebar.multiselect('Tipos de contratos', tipos_de_contratos, default=tipos_de_contratos)

#Seleciono todos os tamanhos de empresas e crio um sidebar 

tamanhos_das_empresas = sorted(df['tamanho_empresa'].unique())
filtro_tamanho_empresas = st.sidebar.multiselect('Tamanhos das empresas', tamanhos_das_empresas, default=tamanhos_das_empresas)

#O dataframe é filtrado de acordo com as seleções feitas (O & só é usado caso possua mais opções)

df_filtrado = df[
    (df['ano'].isin (anos_encontrados) &
     df['contrato'].isin(filtro_contratos) &
     df['senioridade'].isin(senioridades_filtro) &
     df['tamanho_empresa'].isin(filtro_tamanho_empresas)
    )
]

st.title('🎲 Dashboard de Análise de Salários na Área de Dados')
st.markdown('Explore os dados saláriais. Utilize os filtros à esquerda.')

print(df.columns)

#verifico se meu dataframe não esta vazio e faço calculo de métricas se não exibe zerado
if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, ""

#crio colunas lado a lado
col1, col2, col3, col4 = st.columns(4)

#exibe uma métrica visual
col1.metric('Salário médio', f"${salario_medio:,.0f}")
col2.metric('Salário máximo', f"${salario_maximo:,.0f}")
col3.metric('Total de registros', f"{total_registros:,}")
col4.metric('Cargo mais frequente', cargo_mais_frequente)

st.markdown('---')
st.subheader('Gráficos')

col_graph1, col_graph2 = st.columns(2)

#verificação se o dataframe esta vazio, caso não esteja agrupar o cargo com a média salarial dos 10 maiores
with col_graph1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title='Top 10 cargos por salário médio',
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico de cargos.')

with col_graph2:
    if not df_filtrado.empty:
        graph_histogram = px.histogram(
            df_filtrado,
            x='usd',
            nbins=20,
            title='Distribuição de salários anuais',
            labels={'usd': 'Faixa salaral - USD', 'count': ''}
        )
        graph_histogram.update_layout(title_x = 0.2)
        st.plotly_chart(graph_histogram, use_container_width= True)
    else:
        st.warning('Nenhum dado no gráfico de distribuição')

col_graph3, col_graph4 = st.columns(2)

with col_graph3:
    if not df_filtrado.empty:
        tipos_trabalho_contagem = df_filtrado['remoto'].value_counts().reset_index()
        tipos_trabalho_contagem.columns = ['tipo_trabalho', 'quantidade']
        graph_remoto = px.pie(
            tipos_trabalho_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5
        )

        graph_remoto.update_traces(textinfo = 'percent+label')
        graph_remoto.update_layout(title = 'Proporção dos tipos de trabalho')
        st.plotly_chart(graph_remoto, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir nos tipos de trabalhos')

with col_graph4:
    if not df_filtrado.empty:
        cargo_data_scientist = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        #print(df_filtrado.head(10))
        media_ds = cargo_data_scientist.groupby('residencia_iso3')['usd'].mean().sort_values(ascending=True).reset_index()
        graph_paises = px.choropleth(
            media_ds,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'empresa': 'País'})
        graph_paises.update_layout(title_x=0.1)
        st.plotly_chart(graph_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
