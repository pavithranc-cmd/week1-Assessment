"""
Week 1 Assessment - Task 1: Python Core, OOP and Errors

Sections:
    1. bonus() function with default, *args and **kwargs parameters
    2. Employee class and Manager subclass (inheritance)
    3. Custom exception InvalidSalaryError with try / except / finally
    4. Reading a CSV file + list comprehension, map/lambda, filter
    5. for loop with continue and break

Only Python standard-library modules are used.
"""

import csv                 # built-in module for reading CSV files
from pathlib import Path   # built-in module for working with file paths

# The CSV file is in the data/ folder next to this script.
# Using __file__ means the program works no matter which folder you run it from.
CSV_FILE = Path(__file__).parent / "data" / "employees.csv"


# ---------------------------------------------------------------------------
# 1. FUNCTION WITH DEFAULT, *args AND **kwargs PARAMETERS
# ---------------------------------------------------------------------------
def bonus(salary, rate=0.1, *extras, **options):
    """
    Calculate a bonus.

    salary   : the base salary (required)
    rate     : bonus percentage as a decimal, default 0.1 (10%)
    *extras  : any number of extra amounts, collected into a TUPLE
    **options: any keyword arguments, collected into a DICTIONARY
               - 'cap' (optional): the bonus can never be more than this
    """
    result = salary * rate + sum(extras)   # base bonus + all extra amounts

    cap = options.get("cap")               # .get() returns None if 'cap' is missing
    if cap is not None and result > cap:
        result = cap                       # limit the bonus to the cap

    return result


# ---------------------------------------------------------------------------
# 3. CUSTOM EXCEPTION (defined before the class that uses it)
# ---------------------------------------------------------------------------
class InvalidSalaryError(Exception):
    """Raised when an employee is given a negative salary."""
    pass


# ---------------------------------------------------------------------------
# 2. CLASSES AND INHERITANCE
# ---------------------------------------------------------------------------
class Employee:
    """A normal employee with a name and a monthly salary."""

    def __init__(self, name, salary):
        # Validate BEFORE storing: a negative salary is not allowed.
        if salary < 0:
            raise InvalidSalaryError(f"Invalid salary: {salary}")
        self.name = name        # instance attribute
        self.salary = salary    # instance attribute

    def annual_salary(self):
        """Monthly salary x 12 months."""
        return self.salary * 12

    def get_details(self):
        return f"Employee: {self.name}, Salary: {self.salary}"


class Manager(Employee):
    """A Manager IS an Employee, plus a team size."""

    def __init__(self, name, salary, team_size):
        # super().__init__() runs the parent's __init__,
        # so name, salary AND the salary check are reused (no copy-paste).
        super().__init__(name, salary)
        self.team_size = team_size

    def get_details(self):
        # Method overriding: same method name as the parent, new behaviour.
        return (f"Manager: {self.name}, Salary: {self.salary}, "
                f"Team size: {self.team_size}")


# ---------------------------------------------------------------------------
# 4. READ THE CSV FILE
# ---------------------------------------------------------------------------
def load_employees(path=CSV_FILE):
    """
    Read the CSV and return a list of dictionaries, one per row.
    csv.DictReader uses the header row as the dictionary keys.
    Every value is read as TEXT, so salary is converted to int.
    """
    employees = []
    with open(path, newline="", encoding="utf-8") as file:   # 'with' closes the file automatically
        reader = csv.DictReader(file)
        for row in reader:
            row["salary"] = int(row["salary"])
            employees.append(row)
    return employees


def names_above(employees, limit=50000):
    """List comprehension: names of employees earning more than `limit`."""
    return [e["name"] for e in employees if e["salary"] > limit]


def salaries_with_raise(employees, percent=10):
    """map + lambda: new salary after a raise, as (name, new_salary) pairs."""
    # round() gives a whole number and avoids float noise like 33000.000000000004
    return list(map(lambda e: (e["name"], round(e["salary"] * (1 + percent / 100))),
                    employees))


def chennai_employees(employees):
    """filter + lambda: keep only employees whose city is Chennai."""
    return list(filter(lambda e: e["city"] == "Chennai", employees))


# ---------------------------------------------------------------------------
# 5. LOOP WITH continue AND break
# ---------------------------------------------------------------------------
def process_salaries(salaries, stop_above=85000):
    """
    Go through salaries one by one:
      - continue: skip a salary of 0 and move to the next one
      - break   : stop the loop completely after the first salary above `stop_above`
    Returns the list of salaries that were processed.
    """
    processed = []
    for salary in salaries:
        if salary == 0:
            print("  Skipping salary 0 (continue)")
            continue                      # jump to the next loop iteration
        print(f"  Processing salary: {salary}")
        processed.append(salary)
        if salary > stop_above:
            print(f"  Found salary above {stop_above}: {salary} -> stopping (break)")
            break                         # exit the loop immediately
    return processed


# ---------------------------------------------------------------------------
# MAIN PROGRAM - runs only when you execute "python task1.py"
# (not when the tests import this file)
# ---------------------------------------------------------------------------
def main():
    print("=== 1. Bonus function ===")
    print("Basic bonus (50000, default 10%):", bonus(50000))
    print("Bonus with rate 0.2 and extras 1000, 500:", bonus(50000, 0.2, 1000, 500))
    print("Capped bonus (90000, 0.1, extra 2000, cap=8000):",
          bonus(90000, 0.1, 2000, cap=8000))

    print("\n=== 2. Employee and Manager classes ===")
    emp = Employee("Arun", 30000)
    mgr = Manager("Karthik", 90000, 5)
    print(emp.get_details())
    print("Annual salary:", emp.annual_salary())
    print(mgr.get_details())
    print("Annual salary:", mgr.annual_salary())   # inherited from Employee
    print("Is Manager an Employee?", isinstance(mgr, Employee))

    print("\n=== 3. Custom exception with try / except / finally ===")
    try:
        bad = Employee("Test", -500)               # this line raises the error
        print("This line is never reached:", bad.get_details())
    except InvalidSalaryError as error:
        print(f"Error: {error}")
    finally:
        print("Transaction finished")              # ALWAYS runs

    print("\n=== 4. CSV processing ===")
    employees = load_employees()
    print("Total employees read:", len(employees))
    print("Above 50000:", names_above(employees))
    print("10% raise:")
    for name, new_salary in salaries_with_raise(employees):
        print(f"  {name}: {new_salary}")
    print("Chennai:", [e["name"] for e in chennai_employees(employees)])

    print("\n=== 5. Loop with continue and break ===")
    # The CSV has no salary of 0, so one demo value 0 is added at the start
    # to show that 'continue' really skips it.
    salaries = [0] + [e["salary"] for e in employees]
    print("Salaries to check:", salaries)
    processed = process_salaries(salaries)
    print("Processed salaries:", processed)


if __name__ == "__main__":
    main()
