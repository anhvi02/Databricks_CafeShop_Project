-- --------------------------------
-- BRONZE: transactions
-- --------------------------------
CREATE OR REFRESH STREAMING TABLE 
  coffee_shop.layer_bronze.transaction_bronze
  COMMENT "Ingest POS transactions from S3 to Bronze Layer" 
  TBLPROPERTIES ("quality" = "bronze") 
AS SELECT 
        *,
        current_timestamp() as bronze_processing_time,
        _metadata.file_name as source_file
FROM 
  STREAM read_files(
    's3://coffee-shop-bi-project/data_source/pos/',
    format => 'csv',
    header => 'true',
    badRecordsPath => 's3://coffee-shop-bi-project/data_corrupted/layer_bronze/transaction/',
    schema => '
      transaction_id STRING,
      order_id STRING,
      transaction_datetime TIMESTAMP,
      category_name STRING,
      item_name STRING,
      variation_name STRING,
      size STRING,
      milk_type STRING,
      quantity INT,
      unit_price DOUBLE,
      line_total DOUBLE,
      modifiers STRING,
      employee_id STRING,
      payment_method STRING,
      customer_name STRING,
      location_id STRING'
  );

-- --------------------------------
-- BRONZE: roster
-- --------------------------------
CREATE OR REFRESH STREAMING TABLE 
  coffee_shop.layer_bronze.roster_bronze
  COMMENT "Ingest employee roster from S3 to Bronze Layer" 
  TBLPROPERTIES ("quality" = "bronze") 
AS SELECT 
  *,
  current_timestamp() as bronze_processing_time,
  _metadata.file_name as source_file
FROM  
  STREAM read_files(
    's3://coffee-shop-bi-project/data_source/roster/',
    format => 'csv',
    header => 'true',
    badRecordsPath => 's3://coffee-shop-bi-project/data_corrupted/layer_bronze/roster/',
    schema =>'
      employee_id STRING,
      role STRING,
      start_time TIMESTAMP,
      end_time TIMESTAMP,
      area_department STRING,
      pay_rate DOUBLE,
      notes STRING,
      published STRING,
      break_duration DOUBLE'
  );

-- --------------------------------
-- BRONZE: employee master data
-- --------------------------------
CREATE OR REFRESH STREAMING TABLE 
  coffee_shop.layer_bronze.employee_bronze
  COMMENT "Ingest employee master data from S3 to Bronze Layer" 
  TBLPROPERTIES ("quality" = "bronze") 
AS SELECT
  *,
  current_timestamp() as bronze_processing_time,
  _metadata.file_name as source_file
FROM 
  STREAM read_files(
    's3://coffee-shop-bi-project/data_source/employee/',
    format => 'csv',
    header => 'true',
    badRecordsPath => 's3://coffee-shop-bi-project/data_corrupted/layer_bronze/employee/',
    schema => '
      employee_id STRING,
      employee_name STRING,
      role STRING,
      primary_location STRING,
      pay_rate DOUBLE,
      work_pattern STRING'
  );

-- --------------------------------
-- BRONZE: store master data
-- --------------------------------
CREATE OR REFRESH STREAMING TABLE 
  coffee_shop.layer_bronze.store_bronze
  COMMENT "Ingest store master data from S3 to Bronze Layer" 
  TBLPROPERTIES ("quality" = "bronze")
AS SELECT
  *,
  current_timestamp() as bronze_processing_time,
  _metadata.file_name as source_file
FROM 
  STREAM read_files(
    's3://coffee-shop-bi-project/data_source/store/',
    format => 'csv',
    header => 'true',
    badRecordsPath => 's3://coffee-shop-bi-project/data_corrupted/layer_bronze/store/',
    schema => '
      location_id STRING,
      cafe_name STRING,
      address STRING
    '
  )