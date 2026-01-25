"""
Generate Cash Flow Data for financial reporting.
Monthly cash movements by type (Operating, Investing, Financing).
"""

import random
from datetime import datetime, timedelta, date as date_module
import pandas as pd

# Configuration
START_DATE = datetime(2025, 10, 1)
END_DATE = datetime(2026, 1, 23)  # End date: January 23, 2026 (matches POS data)

# Cash Flow structure
CASH_FLOW_STRUCTURE = {
    'Operating': {
        'Cash from Sales': {
            'sub_category': 'Sales Revenue',
            'base': 100000,
            'variation': 0.15,
            'is_positive': True
        },
        'Cash Paid to Suppliers': {
            'sub_category': 'Inventory Purchases',
            'base': 35000,
            'variation': 0.20,
            'is_positive': False
        },
        'Cash Paid to Employees': {
            'sub_category': 'Salaries & Wages',
            'base': 20000,
            'variation': 0.10,
            'is_positive': False
        },
        'Cash Paid for Operating Expenses': {
            'sub_category': 'Rent & Utilities',
            'base': 15000,
            'variation': 0.15,
            'is_positive': False
        },
        'Interest Received': {
            'sub_category': 'Interest Income',
            'base': 100,
            'variation': 0.50,
            'is_positive': True
        },
        'Interest Paid': {
            'sub_category': 'Interest Expense',
            'base': 300,
            'variation': 0.30,
            'is_positive': False
        },
        'Taxes Paid': {
            'sub_category': 'Income Tax',
            'base': 2000,
            'variation': 0.25,
            'is_positive': False
        }
    },
    'Investing': {
        'Equipment Purchases': {
            'sub_category': 'Coffee Machines',
            'base': 0,
            'variation': 0,
            'is_positive': False,
            'frequency': 0.1  # 10% chance per month
        },
        'Furniture Purchases': {
            'sub_category': 'Furniture & Fixtures',
            'base': 0,
            'variation': 0,
            'is_positive': False,
            'frequency': 0.15
        },
        'Property Improvements': {
            'sub_category': 'Leasehold Improvements',
            'base': 0,
            'variation': 0,
            'is_positive': False,
            'frequency': 0.05
        }
    },
    'Financing': {
        'Loan Proceeds': {
            'sub_category': 'Business Loans',
            'base': 0,
            'variation': 0,
            'is_positive': True,
            'frequency': 0.05  # Rare
        },
        'Loan Repayments': {
            'sub_category': 'Principal Payments',
            'base': 1000,
            'variation': 0.20,
            'is_positive': False
        },
        'Owner Contributions': {
            'sub_category': 'Capital Contributions',
            'base': 0,
            'variation': 0,
            'is_positive': True,
            'frequency': 0.08
        },
        'Dividends Paid': {
            'sub_category': 'Owner Distributions',
            'base': 0,
            'variation': 0,
            'is_positive': False,
            'frequency': 0.2  # 20% chance
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
        # Only append if the month-end date doesn't exceed end_date
        if last_day <= end_date:
            months.append(last_day)
        current = next_month
    return months


def generate_cash_flow_data():
    """Generate cash flow data."""
    months = get_months_list(START_DATE.date(), END_DATE.date())
    cash_flow_data = []
    
    for month_date in months:
        year = month_date.year
        month_str = month_date.strftime('%Y-%m-%d')
        
        for flow_type, categories in CASH_FLOW_STRUCTURE.items():
            for category, category_data in categories.items():
                # Check if this item occurs this month
                frequency = category_data.get('frequency', 1.0)
                if frequency < 1.0 and random.random() > frequency:
                    continue  # Skip this month
                
                base = category_data['base']
                variation = category_data.get('variation', 0.1)
                is_positive = category_data.get('is_positive', True)
                
                # Generate value
                if base == 0 and frequency < 1.0:
                    # Occasional large transactions
                    if flow_type == 'Investing':
                        value = random.uniform(5000, 25000) if 'Equipment' in category else random.uniform(2000, 10000)
                    elif flow_type == 'Financing':
                        if 'Loan Proceeds' in category:
                            value = random.uniform(20000, 50000)
                        elif 'Owner Contributions' in category:
                            value = random.uniform(5000, 20000)
                        elif 'Dividends' in category:
                            value = random.uniform(3000, 8000)
                        else:
                            value = 0
                    else:
                        value = 0
                else:
                    value = base * (1 + random.uniform(-variation, variation))
                
                # Apply sign
                if not is_positive:
                    value = -abs(value)
                else:
                    value = abs(value)
                
                cash_flow_value = round(value, 2)
                
                cash_flow_data.append({
                    'Year': year,
                    'Cash Flow Type': flow_type,
                    'Cash Flow Category': category,
                    'Cash Flow Sub Category': category_data['sub_category'],
                    'Cash Flow Values': cash_flow_value
                })
    
    return cash_flow_data


def main():
    """Main function to generate and save cash flow data."""
    print("Generating Cash Flow Data...")
    print(f"Date range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}\n")
    
    # Generate data
    cash_flow_data = generate_cash_flow_data()
    
    # Create DataFrame
    df = pd.DataFrame(cash_flow_data)
    
    # Sort by Year, then Type, then Category
    df = df.sort_values(['Year', 'Cash Flow Type', 'Cash Flow Category']).reset_index(drop=True)
    
    # Save to CSV
    output_file = '../financial/cash_flow_data.csv'
    df.to_csv(output_file, index=False)
    print(f"Cash Flow Data saved to {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    print(f"\nTotal Records: {len(df):,}")
    
    print("\nCash Flow by Type:")
    type_totals = df.groupby('Cash Flow Type')['Cash Flow Values'].sum()
    for flow_type, total in type_totals.items():
        print(f"  {flow_type}: ${total:,.2f}")
    
    print("\nLatest Year Summary:")
    latest_year = df['Year'].max()
    latest_df = df[df['Year'] == latest_year]
    latest_totals = latest_df.groupby('Cash Flow Type')['Cash Flow Values'].sum()
    for flow_type, total in latest_totals.items():
        print(f"  {flow_type}: ${total:,.2f}")
    
    print("\n" + "="*60)
    print("Generation complete!")


if __name__ == '__main__':
    main()

