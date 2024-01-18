import csv
from datetime import datetime

# Defining column indices globally
POSITION_ID_INDEX = None
EMPLOYEE_NAME_INDEX = None
TIME_INDEX = None
TIME_OUT_INDEX = None


def analyze_file(file_path):
    try:
        with open(file_path, "r") as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)  # Skip the header row

            # Set global column indices
            set_column_indices(header)

            employees = list(reader)

            # Filter out rows with empty or improperly formatted date/time values
            employees = [
                row for row in employees if row[TIME_INDEX] and row[TIME_OUT_INDEX]
            ]

            # a) Check for 7 consecutive days
            consecutive_days_employees = check_consecutive_days(employees)

            # b) Check for less than 10 hours between shifts but greater than 1 hour
            less_than_10_hours_employees = check_hours_between_shifts(employees)

            # c) Check for more than 14 hours in a single shift
            more_than_14_hours_employees = check_single_shift_duration(employees)

            # Print results to console
            print_results(
                consecutive_days_employees,
                less_than_10_hours_employees,
                more_than_14_hours_employees,
            )

    except Exception as e:
        print(f"Error processing the file: {e}")


def set_column_indices(header):
    global POSITION_ID_INDEX, EMPLOYEE_NAME_INDEX, TIME_INDEX, TIME_OUT_INDEX
    POSITION_ID_INDEX = header.index("Position ID")
    EMPLOYEE_NAME_INDEX = header.index("Employee Name")
    TIME_INDEX = header.index("Time")
    TIME_OUT_INDEX = header.index("Time Out")


def check_consecutive_days(employees):
    consecutive_days_employees = set()
    employees.sort(
        key=lambda x: (
            x[EMPLOYEE_NAME_INDEX],
            datetime.strptime(x[TIME_INDEX], "%m/%d/%Y %I:%M %p"),
        )
    )

    for i in range(1, len(employees)):
        current_employee = employees[i]
        previous_employee = employees[i - 1]

        current_date = datetime.strptime(
            current_employee[TIME_INDEX], "%m/%d/%Y %I:%M %p"
        )
        previous_date = datetime.strptime(
            previous_employee[TIME_INDEX], "%m/%d/%Y %I:%M %p"
        )

        # Check if the current and previous dates are consecutive
        if (
            current_employee[EMPLOYEE_NAME_INDEX]
            == previous_employee[EMPLOYEE_NAME_INDEX]
            and (current_date - previous_date).days == 1
        ):
            consecutive_days_employees.add(current_employee[EMPLOYEE_NAME_INDEX])

    return consecutive_days_employees


def check_hours_between_shifts(employees):
    less_than_10_hours_employees = set()

    for i in range(1, len(employees)):
        current_employee = employees[i]
        previous_employee = employees[i - 1]

        current_time = datetime.strptime(
            current_employee[TIME_INDEX], "%m/%d/%Y %I:%M %p"
        )
        previous_time_out = datetime.strptime(
            previous_employee[TIME_OUT_INDEX], "%m/%d/%Y %I:%M %p"
        )

        # Check if the hours between shifts are less than 10 but greater than 1
        hours_between_shifts = (current_time - previous_time_out).seconds / 3600
        if 1 < hours_between_shifts < 10:
            less_than_10_hours_employees.add(current_employee[EMPLOYEE_NAME_INDEX])

    return less_than_10_hours_employees


def check_single_shift_duration(employees):
    more_than_14_hours_employees = set()

    for employee in employees:
        time_in = datetime.strptime(employee[TIME_INDEX], "%m/%d/%Y %I:%M %p")
        time_out = datetime.strptime(employee[TIME_OUT_INDEX], "%m/%d/%Y %I:%M %p")

        # Check if the duration of the shift is more than 14 hours
        shift_duration = (time_out - time_in).seconds / 3600
        if shift_duration > 14:
            more_than_14_hours_employees.add(employee[EMPLOYEE_NAME_INDEX])

    return more_than_14_hours_employees


def print_results(
    consecutive_days_employees,
    less_than_10_hours_employees,
    more_than_14_hours_employees,
):
    print("Employees who worked for 7 consecutive days:")
    print(consecutive_days_employees)

    print("\nEmployees with less than 10 hours between shifts but greater than 1 hour:")
    print(less_than_10_hours_employees)

    print("\nEmployees who worked for more than 14 hours in a single shift:")
    print(more_than_14_hours_employees)


if __name__ == "__main__":
    file_path = "./Assignment_Timecard.csv"  # Replace with the actual file path
    analyze_file(file_path)