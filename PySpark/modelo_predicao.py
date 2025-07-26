#Bibliotecas
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Carregar os dados parquet
df = pd.read_parquet("Data/Atividade da MBA Follow - up - Página1.parquet")

# Pré-processamento dos dados
df['Data pedido'] = pd.to_datetime(df['Data pedido'], format='%d/%m/%Y')
df['Data prevista'] = pd.to_datetime(df['Data prevista'], format='%d/%m/%Y')
df['Data entregue'] = pd.to_datetime(df['Data entregue'], format='%d/%m/%Y')

# Coluna de diferença de dias entre data do pedido e data entregue
df['Dias_para_Entrega'] = (df['Data entregue'] - df['Data pedido']).dt.days

# Apenas pedidos entregues
df_treino = df[df['Status da Entrega'] == 'Entregue'].copy()

# Medidas para calibrar a pontualidade
df_treino['Dias_previsto'] = (df_treino['Data prevista'] - df_treino['Data pedido']).dt.days

# Variáveis preditoras e alvo
x = df_treino[['Dias_previsto']]
y = df_treino['Dias_para_Entrega']

# Modelo de Regressão
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
modelo = RandomForestRegressor()
modelo.fit(x_train, y_train)

# Previsões
y_pred = modelo.predict(x_test)

# Salvar o modelo
joblib.dump(modelo, 'models/modelo_pontualidade.joblib')


# Visualizar resultados
print("Precisão do Modelo:", accuracy_score(y_test, y_pred.round()))
print(classification_report(y_test, y_pred.round()))

# Aplicação dos modelos aos pedidos não entregues
df_previsao_modelo = df[df['Status da Entrega'] == 'Não entregue'].copy()
df_previsao_modelo['Dias_previsto'] = (df_previsao_modelo['Data prevista'] - df_previsao_modelo['Data pedido']).dt.days
df_previsao_modelo['Predição_dias_para_Entrega'] = modelo.predict(df_previsao_modelo[['Dias_previsto']].fillna(0)).round().astype(int)
df_previsao_modelo['Predição_data_de_entrega'] = (
    df_previsao_modelo['Data pedido'] + pd.to_timedelta(df_previsao_modelo['Predição_dias_para_Entrega'], unit='d')
).dt.date

# Juntar os resultados com o DataFrame original
df_final = pd.concat([df_treino, df_previsao_modelo], ignore_index=True)
df_final.to_parquet("Data/Followup_Predicoes.parquet", index=False)
df_final.to_csv("Data/Followup_Predicoes.csv", index=False, encoding="utf-8-sig")

# Exibir o DataFrame final
print(
    df_final[df_final['Status da Entrega'] == 'Não entregue'][
        ['Pedido', 'Data pedido', 'Fornecedor', 'Data prevista', 'Data entregue', 'Status da Entrega', 'Dias_para_Entrega', 'Predição_dias_para_Entrega', 'Predição_data_de_entrega']
    ].head(10)
)