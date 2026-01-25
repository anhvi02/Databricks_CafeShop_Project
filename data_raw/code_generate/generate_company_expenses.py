"""
Generate Company Expenses data for financial reporting.
Monthly expense tracking by category and location.
"""

import random
from datetime import datetime, timedelta, date as date_module
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker('en_AU')

# Configuration
START_DATE = datetime(2025, 10, 1)
END_DATE = datetime(2026, 1, 23)  # End date: January 23, 2026 (matches POS data)

# Calculate months from start date to end date
def get_months_list(start_date, end_date):
    """Generate list of month-end dates."""
    months = []
    current = start_date.replace(day=1)
    while current <= end_date:
        # Get last day of month
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

# Expense categories and items
EXPENSE_CATEGORIES = {
    'Rent': {
        'items': ['Store Rent - LOC-001', 'Store Rent - LOC-002', 'Store Rent - LOC-003', 'Store Rent - LOC-004'],
        'base_amount_range': (8000, 12000),  # Per location per month
        'variation': 0.02  # 2% variation
    },
    'Utilities': {
        'items': ['Electricity', 'Water', 'Gas', 'Internet & Phone'],
        'base_amount_range': (500, 1500),
        'variation': 0.15
    },
    'Salaries & Wages': {
        'items': ['Barista Wages', 'FOH Wages', 'Kitchen Staff Wages', 'Manager Salaries', 'Overtime'],
        'base_amount_range': (15000, 25000),  # Total monthly
        'variation': 0.10
    },
    'Marketing & Advertising': {
        'items': ['Social Media Ads', 'Print Advertising', 'Promotional Materials', 'Events & Sponsorships'],
        'base_amount_range': (500, 2000),
        'variation': 0.30
    },
    'Supplies': {
        'items': ['Cleaning Supplies', 'Office Supplies', 'Paper Products', 'Disposables'],
        'base_amount_range': (300, 800),
        'variation': 0.20
    },
    'Equipment Maintenance': {
        'items': ['Coffee Machine Service', 'Equipment Repairs', 'Maintenance Contracts'],
        'base_amount_range': (200, 1000),
        'variation': 0.25
    },
    'Insurance': {
        'items': ['Public Liability Insurance', 'Property Insurance', 'Workers Compensation'],
        'base_amount_range': (400, 800),
        'variation': 0.05
    },
    'Professional Services': {
        'items': ['Accounting Services', 'Legal Services', 'Consulting'],
        'base_amount_range': (300, 1200),
        'variation': 0.20
    },
    'Other Operating Expenses': {
        'items': ['Bank Fees', 'Licenses & Permits', 'Training', 'Uniforms', 'Miscellaneous'],
        'base_amount_range': (200, 600),
        'variation': 0.25
    }
}

LOCATIONS = ['LOC-001', 'LOC-002', 'LOC-003', 'LOC-004']


def generate_company_expenses():
    """Generate company expenses data."""
    months = get_months_list(START_DATE.date(), END_DATE.date())
    expenses_data = []
    
    for month_date in months:
        month_str = month_date.strftime('%Y-%m-%d')
        
        # Generate expenses for each category
        for category, category_data in EXPENSE_CATEGORIES.items():
            # Rent is per location
            if category == 'Rent':
                for item in category_data['items']:
                    location = item.split(' - ')[-1]
                    base_amount = random.uniform(*category_data['base_amount_range'])
                    variation = base_amount * random.uniform(-category_data['variation'], category_data['variation'])
                    expense_value = round(base_amount + variation, 2)
                    
                    expenses_data.append({
                        'Month': month_str,
                        'Expense Category': category,
                        'Expense Items': item,
                        'Expense Values': expense_value
                    })
            else:
                # Other expenses - generate for each item
                for item in category_data['items']:
                    # Some items might not occur every month (e.g., equipment maintenance)
                    if category == 'Equipment Maintenance' and random.random() < 0.3:
                        continue  # Skip 30% of the time
                    if category == 'Professional Services' and random.random() < 0.4:
                        continue  # Skip 40% of the time
                    
                    base_amount = random.uniform(*category_data['base_amount_range'])
                    variation = base_amount * random.uniform(-category_data['variation'], category_data['variation'])
                    expense_value = round(base_amount + variation, 2)
                    
                    expenses_data.append({
                        'Month': month_str,
                        'Expense Category': category,
                        'Expense Items': item,
                        'Expense Values': expense_value
                    })
    
    return expenses_data


def main():
    """Main function to generate and save company expenses data."""
    print("Generating Company Expenses data...")
    print(f"Date range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}\n")
    
    # Generate expenses
    expenses_data = generate_company_expenses()
    
    # Create DataFrame
    df = pd.DataFrame(expenses_data)
    
    # Sort by Month, then Category
    df['Month_dt'] = pd.to_datetime(df['Month'])
    df = df.sort_values(['Month_dt', 'Expense Category', 'Expense Items']).reset_index(drop=True)
    df = df.drop('Month_dt', axis=1)
    
    # Save to CSV
    output_file = '../financial/company_expenses.csv'
    df.to_csv(output_file, index=False)
    print(f"Company Expenses data saved to {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    print(f"\nTotal Expense Records: {len(df):,}")
    print(f"Total Expenses: ${df['Expense Values'].sum():,.2f} AUD")
    print(f"Date Range: {df['Month'].min()} to {df['Month'].max()}")
    
    print("\nExpenses by Category:")
    category_totals = df.groupby('Expense Category')['Expense Values'].sum().sort_values(ascending=False)
    for category, total in category_totals.items():
        pct = (total / df['Expense Values'].sum()) * 100
        print(f"  {category}: ${total:,.2f} ({pct:.1f}%)")
    
    print("\n" + "="*60)
    print("Generation complete!")


if __name__ == '__main__':
    main()

