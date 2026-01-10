-- ----------------------------------------------------------------
-- GOLD: Tables (with Star Schema)
-- ----------------------------------------------------------------

-- --------------------------------
-- GOLD: transactions
-- --------------------------------
CREATE OR REFRESH MATERIALIZED VIEW coffee_shop.layer_gold.fact_transaction
COMMENT "Fact table for transactions"
TBLPROPERTIES ("quality" = "gold") 
AS SELECT
  *,
  current_timestamp() as gold_processing_time
FROM
  coffee_shop.layer_silver.transaction_silver;

-- --------------------------------
-- GOLD: roster
-- --------------------------------
CREATE OR REFRESH MATERIALIZED VIEW coffee_shop.layer_gold.fact_roster
COMMENT "Fact table for roster"
TBLPROPERTIES ("quality" = "gold") 
AS SELECT
  *,
  current_timestamp() as gold_processing_time
FROM
  coffee_shop.layer_silver.roster_silver;

-- --------------------------------
-- GOLD: employee
-- --------------------------------
CREATE OR REFRESH MATERIALIZED VIEW coffee_shop.layer_gold.dim_employee
COMMENT "Dimension table for employee"
TBLPROPERTIES ("quality" = "gold") 
AS SELECT
  *,
  current_timestamp() as gold_processing_time
FROM
  coffee_shop.layer_silver.employee_silver;

-- --------------------------------
-- GOLD: store
-- --------------------------------
CREATE OR REFRESH MATERIALIZED VIEW coffee_shop.layer_gold.dim_store
COMMENT "Dimension table for store"
TBLPROPERTIES ("quality" = "gold") 
AS SELECT
  *,
  current_timestamp() as gold_processing_time
FROM
  coffee_shop.layer_silver.store_silver;



-- ----------------------------------------------------------------
-- GOLD: Views
-- ----------------------------------------------------------------
-- --------------------------------
-- Total Revenue (by...)
-- --------------------------------
-- CREATE OR REFRESH MATERIALIZED VIEW coffee_shop.layer_gold.vw_total_revenue
-- COMMENT "Total revenue"
-- TBLPROPERTIES ("quality" = "gold")
-- AS SELECT 
  

