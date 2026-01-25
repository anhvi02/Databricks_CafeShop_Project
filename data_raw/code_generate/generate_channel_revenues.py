"""
Generate Channel Revenues data for financial reporting.
Revenue breakdown by channel (POS, Delivery, Catering, etc.).
"""

import random
from datetime import datetime, timedelta, date as date_module
import pandas as pd

# Configuration
START_DATE = datetime(2025, 10, 1)
END_DATE = datetime(2026, 1, 23)  # End date: January 23, 2026 (matches POS data)

# Channels and their distribution
CHANNELS = {
    'POS': {
        'category': 'In-Store',
        'percentage': 0.85,  # 85% of revenue from POS
        'base_daily': 10000  # Base daily revenue
    },
    'Delivery': {
        'category': 'Delivery',
        'percentage': 0.10,  # 10% of revenue
        'base_daily': 1200
    },
    'Catering': {
        'category': 'Catering',
        'percentage': 0.04,  # 4% of revenue
        'base_daily': 500
    },
    'Wholesale': {
        'category': 'Wholesale',
        'percentage': 0.01,  # 1% of revenue
        'base_daily': 150
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


def get_weekdays_in_month(year, month):
    """Get number of weekdays (Mon-Fri) in a month."""
    from calendar import monthrange
    weekdays = 0
    days_in_month = monthrange(year, month)[1]
    for day in range(1, days_in_month + 1):
        date_obj = datetime(year, month, day).date()
        if date_obj.weekday() < 5:  # Monday=0, Friday=4
            weekdays += 1
    return weekdays


def generate_channel_revenues():
    """Generate channel revenues data."""
    months = get_months_list(START_DATE.date(), END_DATE.date())
    revenues_data = []
    
    for month_date in months:
        year = month_date.year
        month = month_date.month
        month_year = month_date.strftime('%b %Y')
        first_date = month_date.replace(day=1).strftime('%Y-%m-%d')
        
        # Calculate weekdays in month
        weekdays = get_weekdays_in_month(year, month)
        
        for channel_name, channel_data in CHANNELS.items():
            # Calculate monthly revenue based on weekdays
            base_monthly = channel_data['base_daily'] * weekdays
            
            # Add variation (±10-20%)
            variation = random.uniform(-0.15, 0.15)
            sales_value = round(base_monthly * (1 + variation), 2)
            
            revenues_data.append({
                'Month & Year': month_year,
                'First Date': first_date,
                'Channel': channel_name,
                'Category': channel_data['category'],
                'Sales Values': sales_value
            })
    
    return revenues_data


def main():
    """Main function to generate and save channel revenues data."""
    print("Generating Channel Revenues data...")
    print(f"Date range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}\n")
    
    # Generate revenues
    revenues_data = generate_channel_revenues()
    
    # Create DataFrame
    df = pd.DataFrame(revenues_data)
    
    # Sort by First Date, then Channel
    df['First Date_dt'] = pd.to_datetime(df['First Date'])
    df = df.sort_values(['First Date_dt', 'Channel']).reset_index(drop=True)
    df = df.drop('First Date_dt', axis=1)
    
    # Save to CSV
    output_file = '../financial/channel_revenues.csv'
    df.to_csv(output_file, index=False)
    print(f"Channel Revenues data saved to {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    print(f"\nTotal Revenue Records: {len(df):,}")
    print(f"Total Revenue: ${df['Sales Values'].sum():,.2f} AUD")
    
    print("\nRevenue by Channel:")
    channel_totals = df.groupby('Channel')['Sales Values'].sum().sort_values(ascending=False)
    for channel, total in channel_totals.items():
        pct = (total / df['Sales Values'].sum()) * 100
        print(f"  {channel}: ${total:,.2f} ({pct:.1f}%)")
    
    print("\n" + "="*60)
    print("Generation complete!")


if __name__ == '__main__':
    main()

