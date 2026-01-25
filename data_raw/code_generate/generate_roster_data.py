"""
Generate realistic fake cafe rostering data matching POS transaction data.
Generates 65 operating days (Monday-Friday only) of shift schedules.
"""

import random
import json
from datetime import datetime, timedelta, date as date_module
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker('en_AU')  # Australian locale for realistic names

# Configuration
START_DATE = datetime(2025, 10, 1)  # Start date: October 1, 2025 (matches POS data)
END_DATE = datetime(2026, 1, 23)  # End date: January 23, 2026 (last business day of the week)
# Calculate operating days from start date to end date (Monday-Friday only)
current_date = START_DATE.date()
end_date = END_DATE.date()
operating_days_count = 0
while current_date <= end_date:
    if current_date.weekday() < 5:  # Monday=0, Friday=4
        operating_days_count += 1
    current_date += timedelta(days=1)
OPERATING_DAYS = operating_days_count
CAFE_OPEN = datetime(2025, 10, 1, 6, 30)  # 6:30 AM
CAFE_CLOSE = datetime(2025, 10, 1, 14, 30)  # 2:30 PM

# Employee Master List
EMPLOYEES = {
    # Baristas (7 total)
    'EMP-001': {'role': 'Barista', 'pay_rate_range': (30.00, 33.00), 'primary_locations': ['LOC-001', 'LOC-002'], 'work_pattern': 'full-time'},
    'EMP-002': {'role': 'Barista', 'pay_rate_range': (30.00, 33.00), 'primary_locations': ['LOC-001', 'LOC-003'], 'work_pattern': 'full-time'},
    'EMP-004': {'role': 'Barista', 'pay_rate_range': (30.00, 33.00), 'primary_locations': ['LOC-001'], 'work_pattern': 'full-time'},
    'EMP-007': {'role': 'Barista', 'pay_rate_range': (30.00, 33.00), 'primary_locations': ['LOC-002', 'LOC-004'], 'work_pattern': 'full-time'},
    'EMP-009': {'role': 'Barista', 'pay_rate_range': (30.00, 33.00), 'primary_locations': ['LOC-003'], 'work_pattern': 'part-time'},
    'EMP-012': {'role': 'Barista', 'pay_rate_range': (30.00, 33.00), 'primary_locations': ['LOC-004'], 'work_pattern': 'part-time'},
    'EMP-016': {'role': 'Barista', 'pay_rate_range': (30.00, 33.00), 'primary_locations': ['LOC-002', 'LOC-003'], 'work_pattern': 'part-time'},
    
    # Front of House (8 total)
    'EMP-003': {'role': 'Front of House', 'pay_rate_range': (26.00, 33.00), 'primary_locations': ['LOC-001'], 'work_pattern': 'full-time'},
    'EMP-006': {'role': 'Front of House', 'pay_rate_range': (26.00, 33.00), 'primary_locations': ['LOC-001', 'LOC-002'], 'work_pattern': 'full-time'},
    'EMP-008': {'role': 'Front of House', 'pay_rate_range': (26.00, 33.00), 'primary_locations': ['LOC-001'], 'work_pattern': 'full-time'},
    'EMP-010': {'role': 'Front of House', 'pay_rate_range': (26.00, 33.00), 'primary_locations': ['LOC-002'], 'work_pattern': 'full-time'},
    'EMP-013': {'role': 'Front of House', 'pay_rate_range': (26.00, 33.00), 'primary_locations': ['LOC-003'], 'work_pattern': 'full-time'},
    'EMP-015': {'role': 'Front of House', 'pay_rate_range': (26.00, 33.00), 'primary_locations': ['LOC-004'], 'work_pattern': 'full-time'},
    'EMP-017': {'role': 'Front of House', 'pay_rate_range': (26.00, 33.00), 'primary_locations': ['LOC-003', 'LOC-004'], 'work_pattern': 'part-time'},
    'EMP-018': {'role': 'Front of House', 'pay_rate_range': (26.00, 33.00), 'primary_locations': ['LOC-002', 'LOC-003'], 'work_pattern': 'part-time'},
    
    # Kitchen (4 total - fixed location assignment)
    'EMP-005': {'role': 'Kitchen', 'pay_rate_range': (28.50, 33.00), 'primary_locations': ['LOC-001'], 'work_pattern': 'full-time', 'fixed_location': 'LOC-001'},
    'EMP-011': {'role': 'Kitchen', 'pay_rate_range': (28.50, 33.00), 'primary_locations': ['LOC-002'], 'work_pattern': 'full-time', 'fixed_location': 'LOC-002'},
    'EMP-014': {'role': 'Kitchen', 'pay_rate_range': (28.50, 33.00), 'primary_locations': ['LOC-003'], 'work_pattern': 'full-time', 'fixed_location': 'LOC-003'},
    'EMP-019': {'role': 'Kitchen', 'pay_rate_range': (28.50, 33.00), 'primary_locations': ['LOC-004'], 'work_pattern': 'full-time', 'fixed_location': 'LOC-004'},
}

# Locations
LOCATIONS = ['LOC-001', 'LOC-002', 'LOC-003', 'LOC-004']

# Shift notes templates
SHIFT_NOTES = [
    'Opening shift',
    'Closing shift',
    'Peak hour coverage',
    'Training new staff',
    'Lunch rush support',
    'Covering for colleague',
    'Manager on duty',
    'Stock delivery',
    'Deep clean',
    'Morning prep',
    'Mid-shift',
    'Part-time',
    'Student shift',
    ''
]

# Generate employee names and assign pay rates
employee_master = {}
for emp_id, emp_data in EMPLOYEES.items():
    employee_master[emp_id] = {
        'employee_id': emp_id,
        'employee_name': fake.name(),
        'role': emp_data['role'],
        'primary_location': emp_data['primary_locations'][0],
        'pay_rate': round(random.uniform(*emp_data['pay_rate_range']), 2),
        'work_pattern': emp_data['work_pattern']
    }


def get_operating_days(start_date, end_date):
    """Generate list of operating days (Monday-Friday only) between start and end dates."""
    operating_days = []
    current_date = start_date.date() if isinstance(start_date, datetime) else start_date
    end_date_obj = end_date.date() if isinstance(end_date, datetime) else end_date
    
    while current_date <= end_date_obj:
        # Skip weekends (Saturday=5, Sunday=6)
        if current_date.weekday() < 5:  # Monday=0, Friday=4
            operating_days.append(current_date)
        current_date += timedelta(days=1)
    
    return operating_days


def generate_shift_notes():
    """Generate realistic shift notes."""
    if random.random() < 0.20:  # 20% have no notes
        return ''
    return random.choice(SHIFT_NOTES)


def calculate_break_duration(start_time, end_time):
    """Calculate break duration based on shift length."""
    duration = (end_time - start_time).total_seconds() / 3600  # hours
    if duration > 5:
        return 30
    return 0


def generate_opening_shift(date, location):
    """Generate opening shift (6 AM - 7 AM start, ends 2:30 PM - 3 PM)."""
    start_hour = random.choice([6, 6, 6, 7])  # Mostly 6 AM
    start_minute = random.choice([0, 15, 30]) if start_hour == 6 else random.choice([0, 15])
    start_time = datetime(date.year, date.month, date.day, start_hour, start_minute)
    
    end_hour = random.choice([14, 15])  # 2:30 PM or 3 PM
    end_minute = random.choice([30, 0]) if end_hour == 14 else 0
    end_time = datetime(date.year, date.month, date.day, end_hour, end_minute)
    
    return start_time, end_time


def generate_mid_shift(date, location):
    """Generate mid shift (8:30 AM - 9:30 AM start, ends 2:30 PM - 4:30 PM)."""
    start_hour = random.choice([8, 9])
    start_minute = random.choice([30, 45, 0]) if start_hour == 8 else random.choice([0, 15, 30])
    start_time = datetime(date.year, date.month, date.day, start_hour, start_minute)
    
    end_hour = random.choice([14, 15, 16])
    end_minute = random.choice([30, 0]) if end_hour == 14 else 0
    end_time = datetime(date.year, date.month, date.day, end_hour, end_minute)
    
    return start_time, end_time


def generate_part_time_shift(date, location):
    """Generate part-time shift (10 AM - 11 AM start, ends 2 PM - 2:30 PM)."""
    start_hour = random.choice([10, 11])
    start_minute = random.choice([0, 15, 30])
    start_time = datetime(date.year, date.month, date.day, start_hour, start_minute)
    
    end_hour = 14  # 2 PM
    end_minute = random.choice([0, 30])
    end_time = datetime(date.year, date.month, date.day, end_hour, end_minute)
    
    return start_time, end_time


def get_available_employees(role, location, date, existing_shifts, all_shifts_so_far):
    """Get employees available for a role at a location on a date."""
    available = []
    for emp_id, emp_data in EMPLOYEES.items():
        if emp_data['role'] != role:
            continue
        
        # Kitchen staff only work at fixed location
        if role == 'Kitchen':
            if emp_data.get('fixed_location') != location:
                continue
        
        # Check if employee works at this location
        if location not in emp_data['primary_locations']:
            continue
        
        # Check for overlapping shifts (same day)
        has_overlap = False
        date_obj = date.date() if isinstance(date, datetime) else date
        for shift in existing_shifts:
            if shift['employee_id'] == emp_id:
                shift_date = shift['start_time'].date() if isinstance(shift['start_time'], datetime) else shift['start_time']
                if shift_date == date_obj:
                    has_overlap = True
                    break
        
        # Check work pattern constraints
        if not should_employee_work(emp_id, date, all_shifts_so_far):
            continue
        
        if not has_overlap:
            available.append(emp_id)
    
    return available


def should_employee_work(emp_id, date, all_shifts_so_far):
    """Determine if employee should work based on work pattern and recent shifts."""
    emp_data = EMPLOYEES[emp_id]
    work_pattern = emp_data['work_pattern']
    
    # Convert date to date object if it's datetime
    if isinstance(date, datetime):
        date_obj = date.date()
    else:
        date_obj = date
    
    # Get recent shifts for this employee (last 7 days)
    recent_shifts = [s for s in all_shifts_so_far 
                    if s['employee_id'] == emp_id and 
                    isinstance(s['start_time'], datetime) and
                    (date_obj - s['start_time'].date()).days <= 7 and
                    (date_obj - s['start_time'].date()).days >= 0]
    
    # Check consecutive days
    consecutive_days = 0
    check_date = date_obj
    while True:
        day_shifts = [s for s in all_shifts_so_far 
                     if s['employee_id'] == emp_id and 
                     isinstance(s['start_time'], datetime) and
                     s['start_time'].date() == check_date]
        if day_shifts:
            consecutive_days += 1
            check_date -= timedelta(days=1)
        else:
            break
    
    # Don't work more than 5 consecutive days
    if consecutive_days >= 5:
        return False
    
    # Full-time: 4-5 shifts per week
    if work_pattern == 'full-time':
        shifts_this_week = len([s for s in recent_shifts 
                               if isinstance(s['start_time'], datetime) and
                               (date_obj - s['start_time'].date()).days <= 7])
        if shifts_this_week >= 5:
            return False
        # 80% chance if they have 0-3 shifts this week
        if shifts_this_week < 4:
            return random.random() < 0.8
    
    # Part-time: 2-3 shifts per week
    elif work_pattern == 'part-time':
        shifts_this_week = len([s for s in recent_shifts 
                               if isinstance(s['start_time'], datetime) and
                               (date_obj - s['start_time'].date()).days <= 7])
        if shifts_this_week >= 3:
            return False
        # 50% chance if they have 0-2 shifts this week
        if shifts_this_week < 3:
            return random.random() < 0.5
    
    return True


def generate_roster():
    """Generate complete roster for all operating days."""
    operating_days = get_operating_days(START_DATE, END_DATE)
    all_shifts = []
    
    for date in operating_days:
        # Generate shifts for each location
        for location in LOCATIONS:
            location_shifts = []
            
            # LOC-001 has higher staffing requirements
            if location == 'LOC-001':
                # Opening: 1 FOH + 2 Baristas
                foh_available = get_available_employees('Front of House', location, date, location_shifts, all_shifts)
                barista_available = get_available_employees('Barista', location, date, location_shifts, all_shifts)
                
                # Opening FOH
                if foh_available:
                    emp_id = random.choice(foh_available)
                    start_time, end_time = generate_opening_shift(date, location)
                    location_shifts.append({
                        'employee_id': emp_id,
                        'start_time': start_time,
                        'end_time': end_time,
                        'location': location
                    })
                
                # Opening Baristas (2)
                for _ in range(2):
                    if barista_available:
                        emp_id = random.choice(barista_available)
                        barista_available.remove(emp_id)
                        start_time, end_time = generate_opening_shift(date, location)
                        location_shifts.append({
                            'employee_id': emp_id,
                            'start_time': start_time,
                            'end_time': end_time,
                            'location': location
                        })
                
                # Peak coverage: Additional FOH and Baristas
                if random.random() < 0.7:  # 70% chance of additional peak coverage
                    foh_available = get_available_employees('Front of House', location, date, location_shifts, all_shifts)
                    barista_available = get_available_employees('Barista', location, date, location_shifts, all_shifts)
                    
                    if foh_available:
                        emp_id = random.choice(foh_available)
                        start_time, end_time = generate_mid_shift(date, location)
                        location_shifts.append({
                            'employee_id': emp_id,
                            'start_time': start_time,
                            'end_time': end_time,
                            'location': location
                        })
                    
                    if barista_available:
                        emp_id = random.choice(barista_available)
                        start_time, end_time = generate_mid_shift(date, location)
                        location_shifts.append({
                            'employee_id': emp_id,
                            'start_time': start_time,
                            'end_time': end_time,
                            'location': location
                        })
                
                # Kitchen staff (morning only, 6:30 AM - 2 PM)
                kitchen_available = get_available_employees('Kitchen', location, date, location_shifts, all_shifts)
                if kitchen_available:
                    emp_id = kitchen_available[0]  # Only one kitchen staff per location
                    start_time = datetime(date.year, date.month, date.day, 6, 30)
                    end_time = datetime(date.year, date.month, date.day, 14, 0)  # 2 PM
                    location_shifts.append({
                        'employee_id': emp_id,
                        'start_time': start_time,
                        'end_time': end_time,
                        'location': location
                    })
                
                # Closing: Additional FOH and Barista
                foh_available = get_available_employees('Front of House', location, date, location_shifts, all_shifts)
                barista_available = get_available_employees('Barista', location, date, location_shifts, all_shifts)
                
                if foh_available and len([s for s in location_shifts if EMPLOYEES[s['employee_id']]['role'] == 'Front of House']) < 2:
                    emp_id = random.choice(foh_available)
                    start_time, end_time = generate_mid_shift(date, location)
                    location_shifts.append({
                        'employee_id': emp_id,
                        'start_time': start_time,
                        'end_time': end_time,
                        'location': location
                    })
                
                if barista_available and len([s for s in location_shifts if EMPLOYEES[s['employee_id']]['role'] == 'Barista']) < 3:
                    emp_id = random.choice(barista_available)
                    start_time, end_time = generate_mid_shift(date, location)
                    location_shifts.append({
                        'employee_id': emp_id,
                        'start_time': start_time,
                        'end_time': end_time,
                        'location': location
                    })
            
            else:  # LOC-002, LOC-003, LOC-004
                # Opening: 1 FOH + 1 Barista
                foh_available = get_available_employees('Front of House', location, date, location_shifts, all_shifts)
                barista_available = get_available_employees('Barista', location, date, location_shifts, all_shifts)
                
                # Opening FOH
                if foh_available:
                    emp_id = random.choice(foh_available)
                    start_time, end_time = generate_opening_shift(date, location)
                    location_shifts.append({
                        'employee_id': emp_id,
                        'start_time': start_time,
                        'end_time': end_time,
                        'location': location
                    })
                
                # Opening Barista
                if barista_available:
                    emp_id = random.choice(barista_available)
                    start_time, end_time = generate_opening_shift(date, location)
                    location_shifts.append({
                        'employee_id': emp_id,
                        'start_time': start_time,
                        'end_time': end_time,
                        'location': location
                    })
                
                # Kitchen staff (morning only)
                kitchen_available = get_available_employees('Kitchen', location, date, location_shifts, all_shifts)
                if kitchen_available:
                    emp_id = kitchen_available[0]
                    start_time = datetime(date.year, date.month, date.day, 6, 30)
                    end_time = datetime(date.year, date.month, date.day, 14, 0)  # 2 PM
                    location_shifts.append({
                        'employee_id': emp_id,
                        'start_time': start_time,
                        'end_time': end_time,
                        'location': location
                    })
                
                # Peak coverage: Additional staff (30% chance)
                if random.random() < 0.3:
                    foh_available = get_available_employees('Front of House', location, date, location_shifts, all_shifts)
                    if foh_available:
                        emp_id = random.choice(foh_available)
                        start_time, end_time = generate_part_time_shift(date, location)
                        location_shifts.append({
                            'employee_id': emp_id,
                            'start_time': start_time,
                            'end_time': end_time,
                            'location': location
                        })
            
            # Add all location shifts to main list
            all_shifts.extend(location_shifts)
    
    # Convert to roster format
    roster_data = []
    for shift in all_shifts:
        emp_id = shift['employee_id']
        emp_info = employee_master[emp_id]
        
        start_time = shift['start_time']
        end_time = shift['end_time']
        break_duration = calculate_break_duration(start_time, end_time)
        notes = generate_shift_notes()
        published = 'Yes' if random.random() < 0.95 else 'No'
        
        roster_data.append({
            'employee_id': emp_id,
            'role': emp_info['role'],
            'start_time': start_time.strftime('%Y-%m-%d %H:%M'),
            'end_time': end_time.strftime('%Y-%m-%d %H:%M'),
            'area_department': shift['location'],
            'pay_rate': emp_info['pay_rate'],
            'notes': notes,
            'published': published,
            'break_duration': break_duration
        })
    
    return roster_data


def main():
    """Main function to generate and save roster data."""
    print("Generating roster data...")
    print(f"Date range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
    print(f"Operating days: {OPERATING_DAYS} (Monday-Friday only)")
    print(f"Locations: {len(LOCATIONS)}")
    print(f"Total employees: {len(EMPLOYEES)}\n")
    
    # Generate roster
    roster_data = generate_roster()
    
    # Create DataFrame
    df_roster = pd.DataFrame(roster_data)
    
    # Sort by start_time, then location
    df_roster['start_time_dt'] = pd.to_datetime(df_roster['start_time'])
    df_roster = df_roster.sort_values(['start_time_dt', 'area_department']).reset_index(drop=True)
    df_roster = df_roster.drop('start_time_dt', axis=1)
    
    # Reorder columns
    column_order = ['employee_id', 'role', 'start_time', 'end_time', 
                   'area_department', 'pay_rate', 'notes', 'published', 'break_duration']
    df_roster = df_roster[column_order]
    
    # Save roster CSV
    import os
    roster_dir = '../data/roster'
    employee_dir = '../data/employee'
    os.makedirs(roster_dir, exist_ok=True)
    os.makedirs(employee_dir, exist_ok=True)
    
    output_file = os.path.join(roster_dir, 'roster_0.csv')
    df_roster.to_csv(output_file, index=False)
    print(f"Roster data saved to {output_file}")
    
    # Create employee master CSV
    employee_master_list = []
    for emp_id, emp_info in employee_master.items():
        employee_master_list.append(emp_info)
    
    df_employees = pd.DataFrame(employee_master_list)
    employee_file = os.path.join(employee_dir, 'employee_0.csv')
    df_employees.to_csv(employee_file, index=False)
    print(f"Employee master data saved to {employee_file}")
    
    # Print summary statistics
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    
    # Total shifts
    print(f"\nTotal Shifts Generated: {len(df_roster):,}")
    
    # Shifts per role
    print("\nShifts by Role:")
    role_counts = df_roster['role'].value_counts()
    for role, count in role_counts.items():
        pct = (count / len(df_roster)) * 100
        print(f"  {role}: {count:,} ({pct:.1f}%)")
    
    # Average shifts per employee
    shifts_per_emp = df_roster['employee_id'].value_counts()
    print(f"\nAverage Shifts per Employee: {shifts_per_emp.mean():.1f}")
    print(f"Min Shifts: {shifts_per_emp.min()}")
    print(f"Max Shifts: {shifts_per_emp.max()}")
    
    # Shifts per location
    print("\nShifts by Location:")
    location_counts = df_roster['area_department'].value_counts()
    for location in LOCATIONS:
        count = location_counts.get(location, 0)
        pct = (count / len(df_roster)) * 100
        print(f"  {location}: {count:,} ({pct:.1f}%)")
    
    # Calculate labor cost
    df_roster['start_time_dt'] = pd.to_datetime(df_roster['start_time'])
    df_roster['end_time_dt'] = pd.to_datetime(df_roster['end_time'])
    df_roster['hours_worked'] = (df_roster['end_time_dt'] - df_roster['start_time_dt']).dt.total_seconds() / 3600
    df_roster['break_hours'] = df_roster['break_duration'] / 60
    df_roster['paid_hours'] = df_roster['hours_worked'] - df_roster['break_hours']
    df_roster['shift_cost'] = df_roster['paid_hours'] * df_roster['pay_rate']
    
    total_labor_cost = df_roster['shift_cost'].sum()
    print(f"\nTotal Labor Cost: ${total_labor_cost:,.2f} AUD")
    
    # Average daily staffing cost by location
    print("\nAverage Daily Staffing Cost by Location:")
    df_roster['date'] = df_roster['start_time_dt'].dt.date
    daily_costs = df_roster.groupby(['area_department', 'date'])['shift_cost'].sum().reset_index()
    avg_daily_costs = daily_costs.groupby('area_department')['shift_cost'].mean()
    for location in LOCATIONS:
        cost = avg_daily_costs.get(location, 0)
        print(f"  {location}: ${cost:,.2f}")
    
    # Published status
    print("\nPublished Status:")
    published_counts = df_roster['published'].value_counts()
    for status, count in published_counts.items():
        pct = (count / len(df_roster)) * 100
        print(f"  {status}: {count:,} ({pct:.1f}%)")
    
    print("\n" + "="*60)
    print("Generation complete!")


if __name__ == '__main__':
    main()

