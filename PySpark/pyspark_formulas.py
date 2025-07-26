import os

os.environ['HADOOP_HOME'] = r'C:\hadoop'
os.environ['PATH'] += r';C:\hadoop\bin'
os.environ['JAVA_HOME'] = r'C:\Program Files\Zulu\zulu-21'

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.sql.functions import col, when, to_date

#Criar o app
spark = SparkSession.builder \
.appName("Análise de Followup dos fornecedores") \
.getOrCreate()

#Ler a planilha (csv)
df = spark.read.csv("Data/Atividade da MBA Follow - up - Página1.csv", header=True, inferSchema=True)

#Converter colunas de data modelo americano para o formato brasileiro
df = df.withColumn("Data pedido", to_date(col("Data pedido"), "dd/MM/yyyy"))
df = df.withColumn("Data prevista", to_date(col("Data prevista"), "dd/MM/yyyy"))
df = df.withColumn("Data entregue", to_date(col("Data entregue"), "dd/MM/yyyy"))

#Definir se pedido foi entregue ou não
df = df.withColumn(
    "Status da Entrega",
    when(
        col("Data entregue").isNull(), "Não entregue").otherwise("Entregue")
    )

#Pedido chegou no tempo previsto?
df = df.withColumn(
    "Pontualidade",
    when(
        (col("Data entregue").isNotNull()) &
        (col("Data entregue") <= col("Data prevista")),
        "Dentro do prazo").when(col("Data entregue") >col("Data prevista"), "Fora do Prazo").otherwise(None))


# Exibir os resultados com as novas colunas
df.select("Pedido", "Data pedido", "Fornecedor", "Data prevista", "Data entregue", "Status da Entrega", "Pontualidade").show(100)

# Salvar o DataFrame final como CSV para fácil visualização
df.toPandas().to_csv("Data/Atividade_da_MBA_Follow_up_com_formulas.csv", index=False, encoding="utf-8-sig")

# Salvar o arquivo com as novas colunas como Parquet para aplicar aos modelos
df.write.mode("overwrite").parquet(r"Data/Atividade da MBA Follow - up - Página1.parquet")

spark.stop()