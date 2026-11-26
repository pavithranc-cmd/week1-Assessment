# Week 1 Assessment - Python & Data Engineering

## Project structure
```text
week1-assessment/
├── data/            employees.csv (original), departments.csv, generated JSON/CSV, backup/
├── notebooks/       analysis.ipynb and its nbconvert export analysis.py
├── reports/charts/  4 PNG charts (bar, histogram, scatter, line)
├── src/             task1.py, task2.py, task3.py
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

## Installation (Windows PowerShell)
```powershell
cd "E:\GEN AI PYTHON\GenAi_Training\week1-assessment"
python -m venv .venv
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned   # only once, if activation is blocked
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env     # then put your own API_KEY in .env
```

## Run the scripts (from the project root, with .venv active)
```powershell
python src/task1.py   # Python core, OOP, custom error, loops
python src/task2.py   # CSV -> JSON/CSV, .env, API calls (needs internet)
python src/task3.py   # NumPy, Pandas, cleaning, merges, 4 charts -> reports/charts/
```
Outputs: `data/employees.json`, `data/high_earners.csv`, `data/users.json`,
`data/departments.csv` and the four PNG files in `reports/charts/`.

## Notebook
Open `notebooks/analysis.ipynb` in VS Code, choose the `.venv` kernel and click **Run All**.
To run it and export it from the terminal:
```powershell
cd notebooks
python -m nbconvert --to notebook --execute --inplace analysis.ipynb
python -m nbconvert --to script analysis.ipynb     # creates analysis.py
cd ..
```

## Terminal commands (Git Bash)
```bash
mkdir -p data/backup reports/charts                            # make folders
cp data/employees.csv data/backup/employees.csv                # copy a file
mv data/backup/employees.csv data/backup/employees_backup.csv  # rename (move) it
mv reports/*.png reports/charts/                               # move charts into charts/
grep -n "Chennai" data/employees.csv                           # 4 rows: Arun, Priya, Divya, Suresh
```
PowerShell equivalents: `New-Item -ItemType Directory`, `Copy-Item`, `Move-Item`, `Select-String`.

## Git workflow
```powershell
git checkout -b feature/analysis         # work on a feature branch
git add <files>
git commit -m "Short, meaningful message"
git push -u origin feature/analysis      # then open a PR into main on GitHub
git log --oneline --graph --all          # view the history
```

## Decisions
- Paths are built from `__file__`, so the scripts work from any folder.
- `employees.csv` is never changed. Cleaning is done on a copy made in code with 2 blank salaries, 1 duplicate row and messy text.
- Text is standardised with `strip()` and title case, except `HR` and `IT`, which stay in capitals.
- Duplicates are dropped before the median is calculated, so the repeated row does not affect the fill value.
- The analysis uses the original data, because the filled salaries are only estimates.
- `.env` holds the secret and is in `.gitignore`. Only `.env.example` with a placeholder is committed.

## Findings
1. Headcount: Sales 2 | HR 2 | IT 3 | Finance 1, and Marketing has no employees.
2. Finance has the highest average salary (90000) and Sales the lowest (41000).
3. 5 of 8 employees earn above 50000, and the most common salary range is 42000-54000.
4. Mumbai has the highest average salary by city (69000).
5. Chitra has the best average mark (86.67) and Dinesh the lowest (61.00).
