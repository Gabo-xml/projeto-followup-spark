# Projeto de Análise de Follow-up de Fornecedores com PySpark

Este projeto realiza o processamento, análise e previsão de entregas de pedidos feitos a fornecedores com base em dados extraídos de planilhas .csv. Utiliza PySpark para tratamento de dados, Scikit-Learn para predição, e Streamlit para visualização interativa.

📁 Pastas
Projeto Spark/
- Data/ -> Arquivos CSV e Parquet
- PySpark/ -> Scripts com formulas em PySpark, aplicação dos modelos e dashboards
- Artifacts/ -> (opcional) libs de suporte
- Models/ -> Modelo treinado - Random Forest (joblib)

⚠ Requisitos
- Python
- Pyspark
- Java (JDK para ambiente)
- Spark
- Hadoop winutils (apenas para usuários Windows)

🚨 IMPORTANTE 🚨
Se você estiver em Windows, descomente a configuração de ambiente no script spark_processing.py e instale winutils (https://github.com/cdarlint/winutils).
