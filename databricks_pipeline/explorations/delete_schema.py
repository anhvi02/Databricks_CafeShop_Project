# Databricks notebook source
# MAGIC %md
# MAGIC ## DROP all tables in SCHEMA layer_bronze

# COMMAND ----------

tables = spark.sql("SHOW TABLES IN coffee_shop.layer_bronze").toPandas()
for table in tables["tableName"]:
    spark.sql(f"DROP TABLE coffee_shop.layer_bronze.{table}")

# COMMAND ----------

# MAGIC %md
# MAGIC %md
# MAGIC ## DROP all tables in SCHEMA layer_silver

# COMMAND ----------

tables = spark.sql("SHOW TABLES IN coffee_shop.layer_silver").toPandas()
for table in tables["tableName"]:
    spark.sql(f"DROP TABLE coffee_shop.layer_silver.{table}")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## DROP all tables in SCHEMA layer_gold

# COMMAND ----------

tables = spark.sql("SHOW TABLES IN coffee_shop.layer_gold").toPandas()
for table in tables["tableName"]:
    spark.sql(f"DROP TABLE coffee_shop.layer_gold.{table}")

# COMMAND ----------

