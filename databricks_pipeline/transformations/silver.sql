-- --------------------------------
-- SILVER: transactions
-- --------------------------------
CREATE OR REFRESH STREAMING TABLE
    coffee_shop.layer_silver.transaction_silver
    (
        CONSTRAINT valid_transaction_id EXPECT (transaction_id IS NOT NULL) ON VIOLATION DROP ROW,
        CONSTRAINT valid_location_id EXPECT (location_id IS NOT NULL) ON VIOLATION DROP ROW,
        CONSTRAINT valid_employee_id EXPECT (employee_id IS NOT NULL) ON VIOLATION DROP ROW,
        CONSTRAINT valid_order_id EXPECT (order_id IS NOT NULL) ON VIOLATION DROP ROW,
        CONSTRAINT valid_quantity EXPECT (quantity > 0),
        CONSTRAINT valid_unit_price EXPECT (unit_price >= 0),
        CONSTRAINT valid_line_total EXPECT (line_total >= 0)
    )
    COMMENT "Transform transaction data from bronze to silver"
    TBLPROPERTIES ("quality" = "silver") 
AS SELECT 
    -- Transaction identifiers
    transaction_id,
    order_id,
    
    -- Timestamp
    transaction_datetime,
    CAST(transaction_datetime AS DATE) as transaction_date,
    
    -- Product information
    category_name,
    item_name,
    variation_name,
        CASE 
        -- Food items
        WHEN category_name = 'Food' THEN 'Food'
        
        -- Decaf
        WHEN modifiers LIKE '%Decaf%' OR modifiers LIKE '%decaf%' THEN 'Decaf Coffee'
        
        -- White Coffee (coffee with milk)
        WHEN variation_name IN (
            'Flat White',
            'Long Machiato',
            'Cappuccino',
            'Latte',
            'Mocha',
            'Short Machiato',
            'Iced White',
            'Iced Mocha'
        ) THEN 'House Blend Coffee'
        
        -- Black Coffee (coffee without milk)
        WHEN variation_name IN (
            'Espresso',
            'Long Black',
            'Iced Black'
        ) THEN 'Single Origin Coffee'
        
        -- Batch/Filter Coffee
        WHEN variation_name = 'Batch/Filter Coffee' THEN 'Filter Coffee'
        
        -- Matcha-based (hot, iced, signature beverage)
        WHEN variation_name IN (
            'Matcha',
            'Iced Matcha',
            'Mont Blanc',
            'Coconut Matcha',
            'Orange Matcha',
            'Jasmine Matcha'
        ) THEN 'Matcha'
        
        -- Chai-based
        WHEN variation_name IN (
            'Chai',
            'Dirty Chai'
        ) THEN 'Chai'
        
        -- Tea-based
        WHEN variation_name IN (
            'Perfect Peach',
            'Chamomile',
            'Peppermint',
            'Honey Lemon',
            'Iced Tea'
        ) THEN 'Tea'
        
        -- Chocolate-based
        WHEN variation_name IN (
            'Hot Chocolate',
            'Iced Chocolate'
        ) THEN 'Chocolate'
        
        -- Juice-based
        WHEN variation_name = 'Orange Juice' THEN 'Juice'
        
        -- If none of the above match, return "Unknown"
        -- This will catch any unexpected variations not explicitly categorized
        ELSE 'Unknown'
    END AS derived_drink_by_ingredient,

    COALESCE(size, CASE 
                    WHEN category_name = 'Food' THEN 'Food'
                    ELSE 'no size'
                  END) AS size,
    COALESCE(milk_type, CASE 
                          WHEN category_name = 'Food' THEN 'Food'
                          ELSE 'no milk'
                        END ) AS milk_type,
    
    -- Quantities and pricing
    quantity,
    unit_price,
    line_total,
    
    -- Additional details
    modifiers,
    
    -- Employee and customer
    employee_id,
    COALESCE(customer_name, 'Unknown') AS customer_name,
    
    -- Payment and location
    payment_method,
    location_id,
    
    -- Metadata
    bronze_processing_time,
    current_timestamp() as silver_processing_time
FROM STREAM coffee_shop.layer_bronze.transaction_bronze;


-- --------------------------------
-- SILVER: roster
-- --------------------------------
CREATE OR REFRESH STREAMING TABLE
    coffee_shop.layer_silver.roster_silver
    (
        CONSTRAINT valid_role EXPECT (role IN ('Barista', 'Front of House', 'Kitchen')),
        CONSTRAINT valid_employee_id EXPECT (employee_id IS NOT NULL) ON VIOLATION DROP ROW,
        CONSTRAINT valid_start_time EXPECT (start_time IS NOT NULL),
        CONSTRAINT valid_end_time EXPECT (end_time IS NOT NULL),
        CONSTRAINT valid_time_range EXPECT (end_time > start_time)
    )
    COMMENT "Transform roster data from bronze to silver"
    TBLPROPERTIES ("quality" = "silver") 
AS SELECT 
    *,
    current_timestamp() as silver_processing_time
FROM STREAM coffee_shop.layer_bronze.roster_bronze;


-- --------------------------------
-- SILVER: employee (with SCD Type 2 applied)
CREATE OR REFRESH STREAMING TABLE 
  coffee_shop.layer_silver.employee_silver
  (
    CONSTRAINT valid_employee_id EXPECT (employee_id IS NOT NULL) ON VIOLATION DROP ROW
  )
  COMMENT "Employee master data with historical changes (SCD Type 2)"
  TBLPROPERTIES ("quality" = "silver");

CREATE FLOW scd_employee_type2 AS
AUTO CDC INTO coffee_shop.layer_silver.employee_silver
FROM (
    SELECT *,
    current_timestamp() as silver_processing_time
    FROM STREAM(coffee_shop.layer_bronze.employee_bronze)
    )   
KEYS (employee_id)
SEQUENCE BY bronze_processing_time
COLUMNS * EXCEPT (source_file, bronze_processing_time)
STORED AS SCD TYPE 2;


-- --------------------------------
-- SILVER: store (with CDC applied)
-- --------------------------------
CREATE OR REFRESH STREAMING TABLE 
    coffee_shop.layer_silver.store_silver
    (
        CONSTRAINT valid_location_id EXPECT (location_id IS NOT NULL) ON VIOLATION FAIL UPDATE
    );


CREATE FLOW scd_store_type2 AS
AUTO CDC INTO coffee_shop.layer_silver.store_silver
FROM (
    SELECT 
        *,  
        current_timestamp() as silver_processing_time
    FROM STREAM(coffee_shop.layer_bronze.store_bronze)
)
KEYS (location_id)
SEQUENCE BY bronze_processing_time
COLUMNS * EXCEPT (source_file, bronze_processing_time)
STORED AS SCD TYPE 2;
