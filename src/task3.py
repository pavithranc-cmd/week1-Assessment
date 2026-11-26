"""
Week 1 Assessment - Task 3: NumPy, Pandas and Matplotlib

Part A - NumPy marks array (4 students x 3 subjects)
Part B - Pandas basics on data/employees.csv
Part C - Create data/departments.csv (includes one department with no employees)
Part D - Cleaning data/employees_raw.csv (2 missing salaries, 1 duplicate row)
Part E - groupby().agg() and pd.merge (inner, left, outer)
Part F - 4 charts saved as PNG in reports/, one insight each

How the cleaning data relates to the original:
    employees_raw.csv is a COPY of employees.csv that I made dirty on purpose:
    Priya's and Meena's salaries are blank, and Rahul's row appears twice.
    employees.csv itself is never changed.
    After cleaning, the copy has the same 8 employees again, so the headcount
    (Sales 2 | HR 2 | IT 3 | Finance 1) is the same as in the original.
    The analysis uses the ORIGINAL file, because the two filled-in salaries
    are only estimates (the median), not the real values.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")                     # save charts to files without opening a window
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd

ROOT = Path(__file__).parent.parent       # the week1-assessment folder
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

STUDENTS = ["Asha", "Bala", "Chitra", "Dinesh"]
SUBJECTS = ["Maths", "Science", "English"]
DEPT_ORDER = ["Sales", "HR", "IT", "Finance"]


# ---------------------------------------------------------------------------
# PART A - NUMPY
# ---------------------------------------------------------------------------
def numpy_part():
    print("=== A. NumPy ===")
    # rows = students, columns = subjects
    marks = np.array([
        [78, 85, 90],
        [65, 70, 72],
        [88, 92, 80],
        [55, 60, 68],
    ])
    print("Shape:", marks.shape)                                  # (4, 3)
    print("Student averages:", marks.mean(axis=1).round(2))       # across each row
    print("Subject averages:", marks.mean(axis=0).round(2))       # down each column

    # Broadcasting: the single number 5 is "stretched" to every cell.
    graced = marks + 5
    print("After 5 grace marks:\n", graced)

    # np.dot: each student's marks x subject weights, summed -> one score per student
    weights = np.array([0.4, 0.35, 0.25])                         # weights add up to 1
    weighted = np.dot(marks, weights)
    print("Weighted scores:", weighted.round(2))
    return marks


# ---------------------------------------------------------------------------
# PART B - PANDAS BASICS
# ---------------------------------------------------------------------------
def pandas_basics():
    print("\n=== B. Pandas basics ===")
    df = pd.read_csv(DATA_DIR / "employees.csv")
    df.info()                                                     # columns, types, non-null counts
    print(df.describe())                                          # count, mean, min, max ...
    print("\nloc  (label-based) - name and salary of Chennai staff:")
    print(df.loc[df["city"] == "Chennai", ["name", "salary"]])
    print("\niloc (position-based) - first 3 rows, first 3 columns:")
    print(df.iloc[0:3, 0:3])
    print("\nFilter - IT employees earning above 60000:")
    print(df[(df["department"] == "IT") & (df["salary"] > 60000)])
    return df


# ---------------------------------------------------------------------------
# PART C - CREATE departments.csv
# ---------------------------------------------------------------------------
def create_departments():
    print("\n=== C. Create departments.csv ===")
    departments = pd.DataFrame({
        "department": ["Sales", "HR", "IT", "Finance", "Marketing"],  # Marketing has no employees
        "head": ["Ramesh", "Lakshmi", "Vijay", "Deepa", "Sanjay"],
        "budget": [500000, 300000, 900000, 600000, 400000],
    })
    departments.to_csv(DATA_DIR / "departments.csv", index=False)
    print(departments)
    return departments


# ---------------------------------------------------------------------------
# PART D - CLEANING
# ---------------------------------------------------------------------------
def clean_employees(original):
    print("\n=== D. Cleaning employees_raw.csv ===")
    raw = pd.read_csv(DATA_DIR / "employees_raw.csv")
    print(f"Raw rows: {len(raw)} | Missing salaries: {raw['salary'].isna().sum()} "
          f"| Duplicate rows: {raw.duplicated().sum()}")

    # 1. Drop duplicates FIRST, so the duplicate row does not affect the median.
    clean = raw.drop_duplicates().copy()

    # 2. Fill missing salaries with the median (less affected by extreme values than mean).
    median_salary = clean["salary"].median()
    clean["salary"] = clean["salary"].fillna(median_salary)

    # 3. Correct types: salary became float because of the NaN values; make it int again.
    clean["salary"] = clean["salary"].astype(int)
    clean["department"] = clean["department"].astype("category")

    print(f"Median used: {median_salary:.0f}")
    print(f"Clean rows: {len(clean)} | Missing salaries: {clean['salary'].isna().sum()}")
    print(clean.dtypes)

    # Check: the cleaned copy holds exactly the same employees as the original file.
    same = sorted(clean["id"]) == sorted(original["id"])
    print("Same 8 employees as employees.csv:", same)
    return clean


# ---------------------------------------------------------------------------
# PART E - GROUPBY AND MERGE
# ---------------------------------------------------------------------------
def group_and_merge(df, departments):
    print("\n=== E. groupby and merge ===")
    summary = (
        df.groupby("department")
        .agg(headcount=("id", "count"),
             avg_salary=("salary", "mean"),
             max_salary=("salary", "max"))
        .reindex(DEPT_ORDER)
    )
    print(summary.round(0))
    print("Headcount: " + " | ".join(f"{d} {n}" for d, n in summary["headcount"].items()))

    inner = pd.merge(df, departments, on="department", how="inner")
    left = pd.merge(departments, df, on="department", how="left")
    outer = pd.merge(df, departments, on="department", how="outer")
    print(f"\nInner join rows: {len(inner)} (only departments that have employees)")
    print(f"Left join rows:  {len(left)} (all departments, even with no employees)")
    print(f"Outer join rows: {len(outer)} (everything from both sides)")
    print(outer[["department", "name", "salary", "head", "budget"]])

    empty = outer.loc[outer["id"].isna(), "department"].tolist()
    print("Department with no employees:", empty)
    return summary


# ---------------------------------------------------------------------------
# PART F - CHARTS (each one prints a one-sentence insight)
# ---------------------------------------------------------------------------
def make_charts(df, summary, marks):
    print("\n=== F. Charts ===")

    # 1. Bar - average salary per department
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(summary.index, summary["avg_salary"], label="Average salary")
    ax.set_title("Average Salary by Department")
    ax.set_xlabel("Department")
    ax.set_ylabel("Salary (INR)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "bar_avg_salary.png")
    plt.close(fig)
    top = summary["avg_salary"].idxmax()
    low = summary["avg_salary"].idxmin()
    print(f"Bar: {top} has the highest average salary "
          f"({summary.loc[top, 'avg_salary']:.0f}) and {low} the lowest "
          f"({summary.loc[low, 'avg_salary']:.0f}).")

    # 2. Histogram - salary distribution
    fig, ax = plt.subplots(figsize=(7, 4))
    counts, edges, _ = ax.hist(df["salary"], bins=5, edgecolor="black", label="Employees")
    ax.set_title("Salary Distribution")
    ax.set_xlabel("Salary (INR)")
    ax.set_ylabel("Number of employees")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))   # whole numbers only
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "hist_salary.png")
    plt.close(fig)
    i = counts.argmax()
    print(f"Histogram: the most common salary range is {edges[i]:.0f}-{edges[i + 1]:.0f} "
          f"with {int(counts[i])} of {len(df)} employees.")

    # 3. Scatter - salary of each employee, one colour per city
    fig, ax = plt.subplots(figsize=(7, 4))
    for city, group in df.groupby("city"):
        ax.scatter(group["id"], group["salary"], label=city, s=60)
    ax.set_title("Employee Salary by City")
    ax.set_xlabel("Employee ID")
    ax.set_ylabel("Salary (INR)")
    ax.legend(title="City")
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "scatter_salary_city.png")
    plt.close(fig)
    city_avg = df.groupby("city")["salary"].mean()
    print(f"Scatter: {city_avg.idxmax()} has the highest average salary by city "
          f"({city_avg.max():.0f}).")

    # 4. Line - each student's marks across subjects
    fig, ax = plt.subplots(figsize=(7, 4))
    for name, row in zip(STUDENTS, marks):
        ax.plot(SUBJECTS, row, marker="o", label=name)
    ax.set_title("Student Marks by Subject")
    ax.set_xlabel("Subject")
    ax.set_ylabel("Marks")
    ax.legend(title="Student", loc="upper left", bbox_to_anchor=(1.01, 1))   # outside the plot
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "line_student_marks.png")
    plt.close(fig)
    avgs = marks.mean(axis=1)
    print(f"Line: {STUDENTS[avgs.argmax()]} has the best average ({avgs.max():.2f}) "
          f"and {STUDENTS[avgs.argmin()]} the lowest ({avgs.min():.2f}).")

    print("Saved 4 charts to reports/")


def main():
    marks = numpy_part()
    employees = pandas_basics()
    departments = create_departments()
    clean_employees(employees)
    summary = group_and_merge(employees, departments)   # analysis uses the original data
    make_charts(employees, summary, marks)


if __name__ == "__main__":
    main()
