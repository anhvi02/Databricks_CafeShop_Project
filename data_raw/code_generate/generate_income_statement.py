"""
Generate Income Statement Data for financial reporting.
Monthly aggregated revenue and expenses.
"""

import random
from datetime import datetime, timedelta, date as date_module
import pandas as pd

# Configuration
START_DATE = datetime(2025, 10, 1)
END_DATE = datetime(2026, 1, 23)  # End date: January 23, 2026 (matches POS data)

# Income Statement structure
INCOME_STATEMENT_ITEMS = {
    'Revenue': {
        'items': [
            'Total Sales Revenue',
            'Catering Revenue',
            'Delivery Revenue',
            'Wholesale Revenue'
        ],
        'is_expense': False
    },
    'Cost of Goods Sold': {
        'items': [
            'Coffee Beans',
            'Milk & Dairy',
            'Food Ingredients',
            'Packaging & Supplies',
            'Inventory Adjustments'
        ],
        'is_expense': True
    },
    'Operating Expenses': {
        'items': [
            'Rent',
            'Utilities',
            'Salaries & Wages',
            'Marketing & Advertising',
            'Supplies',
            'Equipment Maintenance',
            'Insurance',
            'Professional Services',
            'Depreciation',
            'Other Operating Expenses'
        ],
        'is_expense': True
    },
    'Other Income/Expenses': {
        'items': [
            'Interest Income',
            'Interest Expense',
            'Other Income',
            'Other Expenses'
        ],
        'is_expense': True  # Most are expenses, but can be income
    }
}


def get_months_list(start_date, end_date):
    """Generate list of month-end dates."""
    months = []
    current = start_date.replace(day=1)
    while current <= end_date:
        if current.month == 12:
            next_month = current.replace(year=current.year + 1, month=1, day=1)
        else:
            next_month = current.replace(month=current.month + 1, day=1)
        last_day = next_month - timedelta(days=1)
        # Only append if the month-end date doesn't exceed end_date
        if last_day <= end_date:
            months.append(last_day)
        current = next_month
    return months


def generate_income_statement_data():
    """Generate income statement data."""
    months = get_months_list(START_DATE.date(), END_DATE.date())
    income_data = []
    
    for month_date in months:
        month_str = month_date.strftime('%Y-%m-%d')
        
        # Base monthly revenue (will be calculated from channel revenues)
        base_revenue = random.uniform(80000, 120000)
        
        for category, category_data in INCOME_STATEMENT_ITEMS.items():
            for item in category_data['items']:
                if category == 'Revenue':
                    # Revenue items
                    if item == 'Total Sales Revenue':
                        value = base_revenue
                    elif item == 'Catering Revenue':
                        value = base_revenue * random.uniform(0.03, 0.05)
                    elif item == 'Delivery Revenue':
                        value = base_revenue * random.uniform(0.08, 0.12)
                    elif item == 'Wholesale Revenue':
                        value = base_revenue * random.uniform(0.005, 0.015)
                    else:
                        value = 0
                elif category == 'Cost of Goods Sold':
                    # COGS as percentage of revenue
                    if item == 'Coffee Beans':
                        value = base_revenue * random.uniform(0.12, 0.18)
                    elif item == 'Milk & Dairy':
                        value = base_revenue * random.uniform(0.08, 0.12)
                    elif item == 'Food Ingredients':
                        value = base_revenue * random.uniform(0.15, 0.22)
                    elif item == 'Packaging & Supplies':
                        value = base_revenue * random.uniform(0.03, 0.05)
                    elif item == 'Inventory Adjustments':
                        value = random.uniform(-500, 500)  # Can be positive or negative
                    else:
                        value = 0
                elif category == 'Operating Expenses':
                    # Operating expenses
                    if item == 'Rent':
                        value = random.uniform(32000, 40000)  # 4 locations
                    elif item == 'Utilities':
                        value = random.uniform(2000, 4000)
                    elif item == 'Salaries & Wages':
                        value = random.uniform(18000, 25000)
                    elif item == 'Marketing & Advertising':
                        value = random.uniform(1000, 2500)
                    elif item == 'Supplies':
                        value = random.uniform(1200, 2000)
                    elif item == 'Equipment Maintenance':
                        value = random.uniform(500, 1500) if random.random() < 0.7 else 0
                    elif item == 'Insurance':
                        value = random.uniform(1600, 2400)
                    elif item == 'Professional Services':
                        value = random.uniform(600, 1500) if random.random() < 0.6 else 0
                    elif item == 'Depreciation':
                        value = random.uniform(2000, 3000)  # Fixed
                    elif item == 'Other Operating Expenses':
                        value = random.uniform(800, 1500)
                    else:
                        value = 0
                else:  # Other Income/Expenses
                    if item == 'Interest Income':
                        value = random.uniform(50, 200) if random.random() < 0.3 else 0
                    elif item == 'Interest Expense':
                        value = random.uniform(200, 500)
                    elif item == 'Other Income':
                        value = random.uniform(100, 400) if random.random() < 0.4 else 0
                    elif item == 'Other Expenses':
                        value = random.uniform(100, 300) if random.random() < 0.5 else 0
                    else:
                        value = 0
                
                # Add small variation
                value = value * random.uniform(0.95, 1.05)
                expense_value = round(abs(value), 2)
                
                income_data.append({
                    'Month': month_str,
                    'Expense Category': category,
                    'Expense Items': item,
                    'Expense Values': expense_value
                })
    
    return income_data


def main():
    """Main function to generate and save income statement data."""
    print("Generating Income Statement Data...")
    print(f"Date range: {START_DATE.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}\n")
    
    # Generate data
    income_data = generate_income_statement_data()
    
    # Create DataFrame
    df = pd.DataFrame(income_data)
    
    # Sort by Month, then Category
    df['Month_dt'] = pd.to_datetime(df['Month'])
    df = df.sort_values(['Month_dt', 'Expense Category', 'Expense Items']).reset_index(drop=True)
    df = df.drop('Month_dt', axis=1)
    
    # Save to CSV
    output_file = '../financial/income_statement_data.csv'
    df.to_csv(output_file, index=False)
    print(f"Income Statement Data saved to {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    print(f"\nTotal Records: {len(df):,}")
    
    print("\nValues by Category:")
    category_totals = df.groupby('Expense Category')['Expense Values'].sum().sort_values(ascending=False)
    for category, total in category_totals.items():
        print(f"  {category}: ${total:,.2f}")
    
    print("\n" + "="*60)
    print("Generation complete!")


if __name__ == '__main__':
    main()

