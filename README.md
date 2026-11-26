# Week 1 Assessment - Python & Data Engineering

## Project structure
```text
week1-assessment/
├── data/        employees.csv (original), departments.csv, employees_raw.csv (cleaning demo), outputs
├── notebooks/   analysis.ipynb and its nbconvert export analysis.py
├── reports/     4 PNG charts (bar, histogram, scatter, line)
├── src/         task1.py, task2.py, task3.py
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

## Setup (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install ipykernel nbconvert   # only needed to run/export the notebook
copy .env.example .env            # then put your real API_KEY in .env
```

## Run
```powershell
python src/task1.py         # Python core, OOP, errors
python src/task2.py         # files, API, .env  (needs internet)
python src/task3.py         # NumPy, Pandas, 4 charts -> reports/
```
Notebook: open `notebooks/analysis.ipynb` and run all cells, or run it from the terminal:
```powershell
cd notebooks
python -m nbconvert --to notebook --execute --inplace analysis.ipynb
python -m nbconvert --to script analysis.ipynb    # creates analysis.py
```

Terminal commands (Git Bash):
```bash
mkdir -p data/backup
cp data/employees.csv data/backup/employees.csv
mv data/backup/employees.csv data/backup/employees_backup.csv
grep -n "Chennai" data/employees.csv      # 4 matching rows: Arun, Priya, Divya, Suresh
```

## Decisions
- Paths are built from `__file__`, so the scripts work from any folder.
- `employees.csv` is never changed. The cleaning demo uses `employees_raw.csv`, a copy with 2 blank salaries (Priya, Meena) and 1 duplicate row (Rahul).
- Duplicates are dropped before the median is calculated, so the duplicate does not affect the fill value.
- After cleaning, the copy has the same 8 employees, so the headcount is unchanged. The analysis uses the original file because the filled salaries are only estimates.
- `.env` holds the secret and is in `.gitignore`. Only `.env.example` with a placeholder is committed.

## Findings
1. Headcount: Sales 2 | HR 2 | IT 3 | Finance 1. Marketing has no employees (shown by the outer join).
2. Finance has the highest average salary (90000) and Sales the lowest (41000).
3. 5 of 8 employees earn above 50000, and the most common salary range is 42000-54000.
4. Mumbai has the highest average salary by city (69000).
5. Chitra has the best average mark (86.67) and Dinesh the lowest (61.00).
