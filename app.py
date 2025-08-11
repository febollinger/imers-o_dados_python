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
