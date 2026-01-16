"""
Generate Balance Sheet Data for financial reporting.
Monthly snapshots of assets, liabilities, and equity.
"""

import random
from datetime import datetime, timedelta, date as date_module
import pandas as pd

# Configuration
START_DATE = datetime(2025, 10, 1)
today = date_module.today()

# Balance Sheet structure
BALANCE_SHEET_STRUCTURE = {
    'Assets': {
        'Current Assets': {
            'Cash': {'base': 50000, 'variation': 0.20},
            'Accounts Receivable': {'base': 5000, 'variation': 0.30},
            'Inventory': {'base': 8000, 'variation': 0.15},
            'Prepaid Expenses': {'base': 2000, 'variation': 0.25}
        },
        'Fixed Assets': {
            'Equipment': {'base': 120000, 'variation': 0.05, 'depreciation': 2000},
            'Furniture & Fixtures': {'base': 40000, 'variation': 0.05, 'depreciation': 500},
            'Leasehold Improvements': {'base': 80000, 'variation': 0.05, 'depreciation': 1000},
            'Accumulated Depreciation': {'base': -30000, 'variation': 0.10, 'accumulating': True}
        }
    },
    'Liabilities': {
        'Current Liabilities': {
            'Accounts Payable': {'base': 6000, 'variation': 0.25},
            'Accrued Expenses': {'base': 3000, 'variation': 0.30},
            'Short-term Loans': {'base': 15000, 'variation': 0.10},
            'Credit Card Payable': {'base': 2000, 'variation': 0.40}
        },
        'Long-term Liabilities': {
            'Long-term Loans': {'base': 50000, 'variation': 0.05, 'decreasing': True},
            'Lease Obligations': {'base': 20000, 'variation': 0.05}
        }
    },
    'Equity': {
        'Owner\'s Equity': {
            'Owner\'s Capital': {'base': 100000, 'variation': 0.02},
            'Retained Earnings': {'base': 50000, 'variation': 0.15, 'accumulating': True}
        }
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
        months.append(last_day)
        current = next_month
    return months


def generate_balance_sheet_data():
    """Generate balance sheet data."""
    months = get_months_list(START_DATE.date(), today)
    balance_data = []
    
    # Track accumulating values
    accumulated_depreciation = -30000
    retained_earnings = 50000
    long_term_loans = 50000
    
    for idx, month_date in enumerate(months):
        year = month_date.year
        month_str = month_date.strftime('%Y-%m-%d')
        
        for balance_type, categories in BALANCE_SHEET_STRUCTURE.items():
            for category, items in categories.items():
                for item_name, item_data in items.items():
                    base = item_data['base']
                    variation = item_data.get('variation', 0.1)
                    
                    # Handle accumulating values
                    if item_data.get('accumulating'):
                        if 'Depreciation' in item_name:
                            accumulated_depreciation -= item_data.get('depreciation', 0)
                            value = accumulated_depreciation
                        elif 'Retained Earnings' in item_name:
                            # Retained earnings increase with profit (simplified)
                            monthly_profit = random.uniform(5000, 15000)
                            retained_earnings += monthly_profit
                            value = retained_earnings
                        else:
                            value = base * (1 + random.uniform(-variation, variation))
                    elif item_data.get('decreasing'):
                        # Long-term loans decrease over time
                        if idx > 0:
                            long_term_loans -= random.uniform(500, 1000)
                        value = max(0, long_term_loans)
                    elif 'Depreciation' in item_name:
                        # Fixed assets depreciate
                        dep_amount = item_data.get('depreciation', 0)
                        value = base - (dep_amount * (idx + 1))
                    else:
                        # Regular items with variation
                        value = base * (1 + random.uniform(-variation, variation))
                    
                    balance_value = round(value, 2)
                    
                    balance_data.append({
                        'Year': year,
                        'Balance Sheet Type': balance_type,
                        'Category': category,
                        'Sub Category': item_name,
                        'Balance Sheet Values': balance_value
                    })
    
    return balance_data


def main():
    """Main function to generate and save balance sheet data."""
    print("Generating Balance Sheet Data...")
    print(f"Date range: {START_DATE.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}\n")
    
    # Generate data
    balance_data = generate_balance_sheet_data()
    
    # Create DataFrame
    df = pd.DataFrame(balance_data)
    
    # Sort by Year, then Type, then Category
    df = df.sort_values(['Year', 'Balance Sheet Type', 'Category', 'Sub Category']).reset_index(drop=True)
    
    # Save to CSV
    output_file = '../financial/balance_sheet_data.csv'
    df.to_csv(output_file, index=False)
    print(f"Balance Sheet Data saved to {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    print(f"\nTotal Records: {len(df):,}")
    
    print("\nValues by Type:")
    type_totals = df.groupby('Balance Sheet Type')['Balance Sheet Values'].sum()
    for balance_type, total in type_totals.items():
        print(f"  {balance_type}: ${total:,.2f}")
    
    print("\nLatest Year Summary:")
    latest_year = df['Year'].max()
    latest_df = df[df['Year'] == latest_year]
    latest_totals = latest_df.groupby('Balance Sheet Type')['Balance Sheet Values'].sum()
    for balance_type, total in latest_totals.items():
        print(f"  {balance_type}: ${total:,.2f}")
    
    print("\n" + "="*60)
    print("Generation complete!")


if __name__ == '__main__':
    main()

