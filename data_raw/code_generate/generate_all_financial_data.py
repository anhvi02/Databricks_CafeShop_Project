"""
Master script to generate all financial data tables.
Run this to generate all financial reporting data at once.
"""

import subprocess
import sys
import os

# Change to script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

scripts = [
    'generate_company_expenses.py',
    'generate_channel_revenues.py',
    'generate_income_statement.py',
    'generate_balance_sheet.py',
    'generate_cash_flow.py'
]

def main():
    """Run all financial data generation scripts."""
    print("="*60)
    print("GENERATING ALL FINANCIAL DATA")
    print("="*60)
    print()
    
    for script in scripts:
        print(f"\n{'='*60}")
        print(f"Running {script}...")
        print('='*60)
        
        try:
            result = subprocess.run(
                [sys.executable, script],
                capture_output=False,
                text=True,
                check=True
            )
            print(f"✓ {script} completed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error running {script}: {e}")
            continue
    
    print("\n" + "="*60)
    print("ALL FINANCIAL DATA GENERATION COMPLETE")
    print("="*60)
    print("\nGenerated files:")
    print("  - financial/company_expenses.csv")
    print("  - financial/channel_revenues.csv")
    print("  - financial/income_statement_data.csv")
    print("  - financial/balance_sheet_data.csv")
    print("  - financial/cash_flow_data.csv")


if __name__ == '__main__':
    main()

