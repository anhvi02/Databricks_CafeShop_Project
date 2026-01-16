"""
Generate realistic fake cafe POS transaction data using Faker library.
Generates 3 months of data (65 operating days, Monday-Friday only).
Target: ~50,000 transactions, ~$675,000 AUD total sales.
"""

import random
import json
from datetime import datetime, timedelta, date as date_module
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker('en_AU')  # Australian locale for realistic names

# Configuration
START_DATE = datetime(2025, 10, 1)  # Start date: October 1, 2025
# Calculate operating days from start date to today (Monday-Friday only)
today = date_module.today()
# Calculate number of weekdays between start date and today
current_date = START_DATE.date()
operating_days_count = 0
while current_date <= today:
    if current_date.weekday() < 5:  # Monday=0, Friday=4
        operating_days_count += 1
    current_date += timedelta(days=1)
OPERATING_DAYS = operating_days_count
TARGET_TOTAL_SALES = 675000  # AUD (will scale with actual days)
TARGET_TRANSACTIONS = 50000  # (will scale with actual days)
TARGET_AVG_TRANSACTION_VALUE = 13.50

# Location distribution (updated: 0.5, 0.2, 0.2, 0.1)
LOCATIONS = {
    'LOC-001': {'weight': 0.50, 'target_sales': 337500},  # 50%
    'LOC-002': {'weight': 0.20, 'target_sales': 135000},  # 20%
    'LOC-003': {'weight': 0.20, 'target_sales': 135000},  # 20%
    'LOC-004': {'weight': 0.10, 'target_sales': 67500}    # 10%
}

# Employee shifts
EMPLOYEES = {
    'EMP-001': {'shift': 'morning'},
    'EMP-002': {'shift': 'morning'},
    'EMP-003': {'shift': 'morning'},
    'EMP-004': {'shift': 'afternoon'},
    'EMP-005': {'shift': 'afternoon'},
    'EMP-006': {'shift': 'all-day'},
    'EMP-007': {'shift': 'all-day'}
}

# Milk types distribution
MILK_TYPES = {
    'full cream': 0.60,
    'oat': 0.15,
    'almond': 0.10,
    'soy': 0.08,
    'skinny': 0.05,
    'lactose free': 0.02,
    None: 0.00  # Will be set for non-milk items
}

# Payment methods
PAYMENT_METHODS = {'card': 0.97, 'cash': 0.03}

# Category distribution
CATEGORY_DISTRIBUTION = {
    'Hot Drinks': 0.65,
    'Iced Drinks': 0.20,
    'Food': 0.15
}

# Iced Drinks item popularity (within Iced Drinks category)
ICED_DRINKS_ITEM_WEIGHTS = {
    'Iced Coffee': 17,      # Highest
    'Iced Juice': 13,
    'Signature Beverage': 9,
    'Iced Tea': 5          # Lowest
}

# Menu structure with category mapping
# category_name: "Hot Drinks", "Iced Drinks", "Food"
MENU = {
    'Hot Coffee': {
        'category_name': 'Hot Drinks',
        'item_name': 'Hot Coffee',
        'variations': ['Flat White', 'Long Black', 'Long Machiato', 'Cappuccino', 'Latte', 
                      'Mocha', 'Espresso', 'Chai', 'Matcha', 'Dirty Chai', 'Short Machiato', 'Hot Chocolate', 'Batch/Filter Coffee'],
        'variation_weights': [23, 18, 16, 14, 12, 10, 8, 6, 5, 4, 2, 1, 3],  # Popularity descending (random pattern)
        'sizes': ['small', 'large'],
        'price_ranges': {'small': (4.00, 5.50), 'large': (4.80, 6.20), None: (3.50, 4.50)},  # Batch/Filter Coffee has no size
        'milk_types': ['full cream', 'oat', 'almond', 'soy', 'skinny', 'lactose free'],
        'modifiers': {
            'default': [['Decaf'], ['1 sugar'], ['2 sugar'], ['3 sugar'], ['Very hot'], 
                       ['Decaf', '2 sugar'], ['Very hot', '1 sugar'], []],
            'machiatos': [['Decaf'], ['1 sugar'], ['2 sugar'], ['3 sugar'], ['Very hot'], 
                         ['Decaf', '2 sugar'], ['Very hot', '1 sugar'], ['Topped up'], 
                         ['Topped up', 'Decaf'], []],
            'long_machiato_preferred': [['Topped up'], ['Topped up', 'Decaf'], ['Topped up', '1 sugar'], 
                                       ['Topped up', '2 sugar'], ['Topped up', 'Very hot']]
        }
    },
    'Signature Beverage': {
        'category_name': 'Iced Drinks',
        'item_name': 'Signature Beverage',
        'variations': ['Mont Blanc', 'Coconut Matcha', 'Orange Matcha', 'Jasmine Matcha'],
        'sizes': ['small', 'large'],
        'price_ranges': {'small': (7.00, 8.00), 'large': (8.50, 9.50)},
        'milk_types': ['full cream', 'oat', 'almond', 'soy', 'skinny', 'lactose free'],
        'modifiers': [[], ['1 sugar'], ['2 sugar']]
    },
    'Hot Tea': {
        'category_name': 'Hot Drinks',
        'item_name': 'Hot Tea',
        'variations': ['Perfect Peach', 'Chamomile', 'Peppermint', 'Honey Lemon'],
        'sizes': [None],
        'price_ranges': {None: (2.00, 2.50)},
        'milk_types': [],
        'modifiers': [[]]
    },
    'Iced Coffee': {
        'category_name': 'Iced Drinks',
        'item_name': 'Iced Coffee',
        'variations': ['Iced White', 'Iced Black', 'Iced Mocha', 'Iced Chocolate', 'Iced Matcha'],
        'variation_weights': None,  # Equal weights for all iced coffee variations
        'sizes': ['small', 'large'],
        'price_ranges': {'small': (5.00, 6.00), 'large': (5.80, 7.00)},
        'milk_types': ['full cream', 'oat', 'almond', 'soy', 'skinny', 'lactose free'],
        'modifiers': [['1 sugar'], ['2 sugar'], []]
    },
    'Iced Juice': {
        'category_name': 'Iced Drinks',
        'item_name': 'Iced Juice',
        'variations': ['Orange Juice'],
        'sizes': ['small', 'large'],
        'price_ranges': {'small': (5.00, 6.00), 'large': (5.80, 7.00)},
        'milk_types': [],
        'modifiers': [[]]
    },
    'Iced Tea': {
        'category_name': 'Iced Drinks',
        'item_name': 'Iced Tea',
        'variations': ['Iced Tea'],
        'sizes': [None],
        'price_ranges': {None: (2.00, 2.50)},
        'milk_types': [],
        'modifiers': [[]]
    },
    'Muffin': {
        'category_name': 'Food',
        'item_name': 'Muffin',
        'variations': ['Blueberry Muffin', 'Double Chocolate Chip Muffin', 'Banana Nut Muffin', 
                      'Apple Cinnamon Muffin', 'Plain Muffin'],
        'sizes': [None],
        'price_ranges': {None: (2.50, 3.50)},
        'milk_types': [],
        'modifiers': [[]]
    },
    'Croissant': {
        'category_name': 'Food',
        'item_name': 'Croissant',
        'variations': ['Regular Croissant', 'Chocolate Croissant', 'Ham & Swiss Croissant'],
        'sizes': [None],
        'price_ranges': {None: (3.50, 4.50)},
        'milk_types': [],
        'modifiers': [[]]
    },
    'French Toast': {
        'category_name': 'Food',
        'item_name': 'French Toast',
        'variations': ['Regular French Toast', 'Nutella & Strawberries French Toast', 'Coconut Cream French Toast'],
        'sizes': [None],
        'price_ranges': {None: (9.99, 13.00)},
        'milk_types': [],
        'modifiers': [[]]
    },
    'Eggs Benedict': {
        'category_name': 'Food',
        'item_name': 'Eggs Benedict',
        'variations': ['Eggs Benedict - White English Muffin', 'Eggs Benedict - Whole Wheat English Muffin'],
        'sizes': [None],
        'price_ranges': {None: (13.50, 13.50)},
        'milk_types': [],
        'modifiers': [[]]
    },
    'Pancakes': {
        'category_name': 'Food',
        'item_name': 'Pancakes',
        'variations': ['Regular Pancakes'],
        'sizes': [None],
        'price_ranges': {None: (7.99, 7.99)},
        'milk_types': [],
        'modifiers': [[]]
    },
    'Coffee Cake': {
        'category_name': 'Food',
        'item_name': 'Coffee Cake',
        'variations': ['Regular Coffee Cake'],
        'sizes': [None],
        'price_ranges': {None: (3.50, 3.50)},
        'milk_types': [],
        'modifiers': [[]]
    },
    'Granola': {
        'category_name': 'Food',
        'item_name': 'Granola',
        'variations': ['Regular Granola', 'Berry Granola', 'Chocolate Granola', 'Honey Granola'],
        'sizes': [None],
        'price_ranges': {None: (4.50, 6.50)},
        'milk_types': [],
        'modifiers': [[]]
    }
}


def get_operating_days(start_date, num_days):
    """Generate list of operating days (Monday-Friday only)."""
    operating_days = []
    current_date = start_date
    days_added = 0
    
    while days_added < num_days:
        # Skip weekends (Saturday=5, Sunday=6)
        if current_date.weekday() < 5:  # Monday=0, Friday=4
            operating_days.append(current_date)
            days_added += 1
        current_date += timedelta(days=1)
    
    return operating_days


def get_menu_item():
    """Randomly select a menu item with all its properties based on category distribution."""
    # First, select category based on distribution
    category_name = random.choices(
        list(CATEGORY_DISTRIBUTION.keys()),
        weights=list(CATEGORY_DISTRIBUTION.values())
    )[0]
    
    # Then, select an item from that category (with weights for Iced Drinks)
    items_in_category = [key for key, data in MENU.items() 
                         if data['category_name'] == category_name]
    
    if category_name == 'Iced Drinks':
        # Use weighted selection for Iced Drinks items
        weights = [ICED_DRINKS_ITEM_WEIGHTS.get(key, 1) for key in items_in_category]
        item_key = random.choices(items_in_category, weights=weights)[0]
    else:
        item_key = random.choice(items_in_category)
    
    menu_data = MENU[item_key]
    
    item_name = menu_data['item_name']
    
    # Select variation (with weights if specified)
    if 'variation_weights' in menu_data and menu_data['variation_weights'] is not None:
        variation = random.choices(
            menu_data['variations'],
            weights=menu_data['variation_weights']
        )[0]
    else:
        variation = random.choice(menu_data['variations'])
    
    # Batch/Filter Coffee has no size
    if variation == 'Batch/Filter Coffee':
        size = None
    else:
        size = random.choice(menu_data['sizes'])
    
    # Get milk type
    if category_name in ['Hot Drinks', 'Iced Drinks']:
        # Espresso, Long Black, and Batch/Filter Coffee don't have milk
        if item_key in ['Iced Juice', 'Iced Tea', 'Hot Tea'] or variation in ['Espresso', 'Long Black', 'Batch/Filter Coffee']:
            milk_type = None
        else:
            milk_type = random.choices(
                list(MILK_TYPES.keys())[:-1],  # Exclude None
                weights=[MILK_TYPES[k] for k in list(MILK_TYPES.keys())[:-1]]
            )[0]
    else:
        milk_type = None
    
    # Get modifiers
    if item_key == 'Hot Coffee':
        if variation == 'Long Machiato':
            # Long Machiato should prefer "Topped up" modifier
            modifiers = random.choices(
                menu_data['modifiers']['long_machiato_preferred'],
                weights=[5, 3, 2, 2, 1]  # Higher weight for "Topped up"
            )[0]
        elif 'Machiato' in variation:
            modifiers = random.choice(menu_data['modifiers']['machiatos'])
        else:
            modifiers = random.choice(menu_data['modifiers']['default'])
    elif item_key in ['Iced Coffee', 'Signature Beverage']:
        modifiers = random.choice(menu_data['modifiers'])
    else:
        modifiers = []
    
    # Variation name is simply the variation (size and milk info are in separate columns)
    variation_name = variation
    
    return {
        'category_name': category_name,
        'item_name': item_name,
        'variation': variation,  # Keep original for order ID generation
        'variation_name': variation_name,  # Descriptive version
        'size': size,
        'milk_type': milk_type,
        'modifiers': modifiers,
        'item_key': item_key  # Keep for price calculation
    }


def calculate_price(item_key, variation, size):
    """Calculate unit price based on item key, variation, and size."""
    menu_data = MENU[item_key]
    price_range = menu_data['price_ranges'][size]
    
    # For fixed prices, return the exact value
    if price_range[0] == price_range[1]:
        return price_range[0]
    
    # Otherwise, random price within range
    return round(random.uniform(price_range[0], price_range[1]), 2)


def get_employee_for_time(datetime_obj, location_id):
    """Assign employee based on time of day and location."""
    hour = datetime_obj.hour
    
    # Morning shift: 6:30 AM - 12:00 PM
    # Afternoon shift: 12:00 PM - 2:30 PM
    # All-day: any time
    
    if 6 <= hour < 12:
        # Morning or all-day employees
        available = [eid for eid, data in EMPLOYEES.items() 
                    if data['shift'] in ['morning', 'all-day']]
    else:
        # Afternoon or all-day employees
        available = [eid for eid, data in EMPLOYEES.items() 
                    if data['shift'] in ['afternoon', 'all-day']]
    
    return random.choice(available) if available else 'EMP-001'


def generate_transaction_datetime(date, peak_hour_weight=0.4, is_batch_filter=False):
    """Generate transaction datetime within operating hours (6:30 AM - 2:30 PM).
    
    If is_batch_filter is True, generate time between 8:15 AM and 1:45 PM.
    """
    if is_batch_filter:
        # Batch/Filter Coffee: 8:15 AM to 1:45 PM
        start_hour = 8
        start_minute = 15
        end_hour = 13  # 1 PM
        end_minute = 45
        
        # Generate random time within this range
        start_total_minutes = start_hour * 60 + start_minute
        end_total_minutes = end_hour * 60 + end_minute
        random_minutes = random.randint(start_total_minutes, end_total_minutes)
        
        hour = random_minutes // 60
        minute = random_minutes % 60
    else:
        # Peak hours: 8-10 AM (40%), 12-2 PM (30%), other hours (30%)
        rand = random.random()
        
        if rand < 0.40:  # Peak morning: 8-10 AM
            hour = random.randint(8, 9)
            minute = random.randint(0, 59)
        elif rand < 0.70:  # Peak lunch: 12-2 PM
            hour = random.randint(12, 13)
            minute = random.randint(0, 59)
        else:  # Other hours: 6:30-8 AM, 10 AM-12 PM, 2-2:30 PM
            hour_choices = [
                (6, 30, 59),  # 6:30-6:59
                (7, 0, 59),   # 7:00-7:59
                (10, 0, 59),  # 10:00-10:59
                (11, 0, 59),  # 11:00-11:59
                (14, 0, 30)   # 2:00-2:30
            ]
            hour, min_start, min_end = random.choice(hour_choices)
            minute = random.randint(min_start, min_end)
    
    second = random.randint(0, 59)
    return datetime(date.year, date.month, date.day, hour, minute, second)


def generate_transaction(transaction_id, date, location_id, order_counter):
    """Generate a single transaction with 1-3 items."""
    # Determine number of items: 70% single, 25% double, 5% triple+
    items_count_rand = random.random()
    if items_count_rand < 0.70:
        num_items = 1
    elif items_count_rand < 0.95:
        num_items = 2
    else:
        num_items = random.randint(3, 4)
    
    # Generate line items first to check if Batch/Filter Coffee is included
    line_items = []
    order_id_base = order_counter
    has_batch_filter = False
    items_list = []
    
    # First pass: collect items to check for Batch/Filter Coffee
    for i in range(num_items):
        item = get_menu_item()
        items_list.append(item)
        if item['variation'] == 'Batch/Filter Coffee':
            has_batch_filter = True
    
    # Generate transaction datetime based on whether Batch/Filter Coffee is included
    transaction_datetime = generate_transaction_datetime(date, is_batch_filter=has_batch_filter)
    
    # Generate customer name (15% null)
    customer_name = None if random.random() < 0.15 else fake.first_name()
    
    # Payment method
    payment_method = random.choices(
        list(PAYMENT_METHODS.keys()),
        weights=list(PAYMENT_METHODS.values())
    )[0]
    
    # Employee
    employee_id = get_employee_for_time(transaction_datetime, location_id)
    
    # Second pass: create line items with the generated datetime
    for item in items_list:
        quantity = 1 if random.random() < 0.80 else 2
        unit_price = calculate_price(item['item_key'], item['variation'], item['size'])
        line_total = round(unit_price * quantity, 2)
        
        # Create order ID - format: ORD-{VARIATION}-####
        variation_clean = item['variation'].upper().replace(' ', '').replace('&', '').replace('-', '').replace('/', '')
        order_id = f"ORD-{variation_clean}-{order_id_base:04d}"
        order_id_base += 1
        
        # Format modifiers as JSON string
        modifiers_json = json.dumps(item['modifiers'])
        
        line_items.append({
            'transaction_id': transaction_id,
            'order_id': order_id,
            'transaction_datetime': transaction_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'category_name': item['category_name'],
            'item_name': item['item_name'],
            'variation_name': item['variation_name'],
            'size': item['size'] if item['size'] else None,
            'milk_type': item['milk_type'],
            'quantity': quantity,
            'unit_price': unit_price,
            'line_total': line_total,
            'modifiers': modifiers_json,
            'employee_id': employee_id,
            'payment_method': payment_method,
            'customer_name': customer_name,
            'location_id': location_id
        })
    
    return line_items, order_id_base


def generate_all_transactions():
    """Generate all transactions for the specified period."""
    operating_days = get_operating_days(START_DATE, OPERATING_DAYS)
    
    all_transactions = []
    transaction_counter = 1
    order_counter = 1
    
    # Calculate transactions per location per day (updated distribution: 0.5, 0.2, 0.2, 0.1)
    transactions_per_location = {
        'LOC-001': 385,  # 50% - Flagship location
        'LOC-002': 154,  # 20%
        'LOC-003': 154,  # 20%
        'LOC-004': 77   # 10%
    }
    
    for date in operating_days:
        for location_id, daily_count in transactions_per_location.items():
            for _ in range(daily_count):
                # Generate transaction ID
                date_str = date.strftime('%Y%m%d')
                transaction_id = f"TXN-{date_str}-{transaction_counter:04d}"
                
                # Generate transaction
                line_items, order_counter = generate_transaction(
                    transaction_id, date, location_id, order_counter
                )
                all_transactions.extend(line_items)
                
                transaction_counter += 1
    
    return all_transactions


def main():
    """Main function to generate and save POS transaction data."""
    print("Generating POS transaction data...")
    print(f"Date range: {START_DATE.strftime('%Y-%m-%d')} to {date_module.today().strftime('%Y-%m-%d')} (current date)")
    print(f"Operating days: {OPERATING_DAYS} (Monday-Friday only)")
    print(f"Target transactions: ~{TARGET_TRANSACTIONS}")
    print(f"Target total sales: ${TARGET_TOTAL_SALES:,.2f} AUD")
    print(f"Location distribution: LOC-001: 50%, LOC-002: 20%, LOC-003: 20%, LOC-004: 10%\n")
    
    # Generate transactions
    transactions = generate_all_transactions()
    
    # Create DataFrame
    df = pd.DataFrame(transactions)
    
    # Sort by transaction_datetime
    df['transaction_datetime'] = pd.to_datetime(df['transaction_datetime'])
    df = df.sort_values('transaction_datetime').reset_index(drop=True)
    
    # Save to CSV
    output_file = 'pos_transactions.csv'
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
    
    # Print summary statistics
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    
    # Total transactions (unique transaction IDs)
    unique_transactions = df['transaction_id'].nunique()
    print(f"\nTotal Transactions: {unique_transactions:,}")
    print(f"Total Line Items: {len(df):,}")
    
    # Total revenue
    total_revenue = df['line_total'].sum()
    print(f"\nTotal Revenue: ${total_revenue:,.2f} AUD")
    print(f"Target Revenue: ${TARGET_TOTAL_SALES:,.2f} AUD")
    print(f"Average Transaction Value: ${total_revenue / unique_transactions:.2f} AUD")
    print(f"Target Average: ${TARGET_AVG_TRANSACTION_VALUE:.2f} AUD")
    
    # Items sold by category_name
    print("\nItems Sold by Category:")
    category_counts = df['category_name'].value_counts()
    for category, count in category_counts.items():
        print(f"  {category}: {count:,}")
    
    # Items sold by item_name
    print("\nItems Sold by Item Type:")
    item_counts = df['item_name'].value_counts()
    for item, count in item_counts.items():
        print(f"  {item}: {count:,}")
    
    # Location distribution
    print("\nLocation Distribution:")
    location_counts = df['location_id'].value_counts()
    location_revenue = df.groupby('location_id')['line_total'].sum()
    for location in ['LOC-001', 'LOC-002', 'LOC-003', 'LOC-004']:
        count = location_counts.get(location, 0)
        revenue = location_revenue.get(location, 0)
        pct = (count / len(df)) * 100
        print(f"  {location}: {count:,} items ({pct:.1f}%), Revenue: ${revenue:,.2f}")
    
    # Payment method distribution
    print("\nPayment Method Distribution:")
    payment_counts = df['payment_method'].value_counts()
    for method, count in payment_counts.items():
        pct = (count / len(df)) * 100
        print(f"  {method}: {count:,} ({pct:.1f}%)")
    
    # Employee distribution
    print("\nEmployee Distribution (Top 10):")
    employee_counts = df['employee_id'].value_counts().head(10)
    for emp, count in employee_counts.items():
        pct = (count / len(df)) * 100
        print(f"  {emp}: {count:,} items ({pct:.1f}%)")
    
    # Date range
    print(f"\nDate Range: {df['transaction_datetime'].min()} to {df['transaction_datetime'].max()}")
    
    print("\n" + "="*60)
    print("Generation complete!")


if __name__ == '__main__':
    main()

