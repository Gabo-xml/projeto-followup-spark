import streamlit as st
import pandas as pd 
import plotly.express as px

# Carregar o DataFrame
df_final = pd.read_parquet("Data/Followup_Predicoes.parquet")

st.title("Dashbard de Follow-up de Fornecedores")
st.write("Este dashboard apresenta as previsões de pontualidade dos fornecedores com base nos pedidos realizados.")

st.metric("Total de Pedidos", len(df_final))

# Gráfico de Pontualidade
st.subheader("Pontualidade dos Pedidos")
pontualidade_counts = df_final['Status da Entrega'].value_counts()
st.bar_chart(pontualidade_counts)

# Gráfico de Pedidos por Fornecedor (Pie Chart)
st.subheader("Pedidos por Fornecedor")
fornecedor_contagem = df_final['Fornecedor'].value_counts().reset_index()
fornecedor_contagem.columns = ['Fornecedor', 'Total Pedidos']
fig = px.pie(fornecedor_contagem, names='Fornecedor', values='Total Pedidos', hole = 0.5, title='Distribuição de Pedidos por Fornecedor')
fig.update_traces(textinfo='label')
st.plotly_chart(fig, use_container_width=True)

# Entregas fora do prazo
st.subheader("Entregas Fora do Prazo")
entregas_fora_prazo = df_final.sort_values(by='Pedido', ascending=True)[df_final['Status da Entrega'] == 'Não entregue']
cols_to_show = ['Pedido', 'Fornecedor', 'Data pedido', 'Data prevista', 'Status da Entrega']
st.dataframe(entregas_fora_prazo[cols_to_show])

# Top Fornecedores com Mais Atrasos
st.subheader("Top Fornecedores com Mais Atrasos")
st.dataframe(
    fornecedores_atrasos := df_final[df_final['Pontualidade'] == 'Fora do Prazo']
    .groupby('Fornecedor').size()
    .sort_values(ascending=False).head(10).rename('Total Atrasos')
)

# Previsões de Entregas feitas pelo modelo treinado
st.subheader("Previsões de Entregas (Pedidos Não Entregues)")
df_previsao = df_final[df_final['Status da Entrega'] == 'Não entregue']
df_previsao = df_previsao.sort_values(by='Pedido', ascending=True)
st.dataframe(df_previsao[['Pedido', 'Fornecedor','Data pedido', 'Data prevista', 'Predição_dias_para_Entrega', 'Predição_data_de_entrega']])