from datetime import datetime, timedelta
import csv
from prettytable import PrettyTable

def parse_datetime(datetime_str):
    """Parse datetime string into a datetime object."""
    return datetime.strptime(datetime_str, "%m/%d/%Y %I:%M %p") if datetime_str else None

def analyze_employee_data(file_path):
    """Analyze employee data based on specified criteria."""
    # Dictionary to store employee information
    employees = {}

    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            position_id = row['Position ID']
            employee_name = row['Employee Name']
            start_time = parse_datetime(row['Time'])
            end_time = parse_datetime(row['Time Out'])

            if position_id not in employees:
                employees[position_id] = {'name': employee_name, 'shifts': []}

            employees[position_id]['shifts'].append((start_time, end_time))

    # Prepare PrettyTable for tabular output
    table = PrettyTable()
    table.field_names = ["Employee Name", "Position ID", "Message"]

    # Analyze and print information based on criteria
    for position_id, employee_data in employees.items():
        employee_name = employee_data['name']
        shifts = employee_data['shifts']

        for i in range(len(shifts) - 1):
            # Check for 7 consecutive days
            if shifts[i][1] and shifts[i+1][0] and (shifts[i+1][0] - shifts[i][1]).days == 1 and \
                    (shifts[i+1][0] - shifts[i][1]).seconds == 0:
                table.add_row([employee_name, position_id, "Worked for 7 consecutive days"])

            # Check for less than 10 hours between shifts but greater than 1 hour
            if shifts[i][1] and shifts[i+1][0] and 1 * 3600 < (shifts[i+1][0] - shifts[i][1]).seconds < 10 * 3600:
                table.add_row([employee_name, position_id, "Less than 10 hours but greater than 1 hour between shifts"])

        # Check for more than 14 hours in a single shift
        for shift in shifts:
            if shift[0] and shift[1] and (shift[1] - shift[0]).seconds > 14 * 3600:
                table.add_row([employee_name, position_id, "Worked for more than 14 hours in a single shift"])

    # Print the table
    print(table)

if __name__ == "__main__":
    file_path = "/content/sample_data/Sheet1.csv"  # Replace with the actual file path
    analyze_employee_data(file_path)
