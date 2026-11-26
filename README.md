# Week 1 Assessment - Python & Data Engineering

Week 1 assessment by pavithranc-cmd.

## Project structure
Each task has its own folder with its own script, data and outputs.
```text
week1-assessment/
├── task1_python_oop/        Task 1 - Python core, OOP and errors
│   ├── data/employees.csv
│   └── task1.py
├── task2_files_api/         Task 2 - files, API and environment
│   ├── data/                employees.csv + outputs: employees.json, high_earners.csv, users.json
│   └── task2.py
├── task3_numpy_pandas/      Task 3 - NumPy, Pandas and Matplotlib
│   ├── data/                employees.csv, departments.csv
│   ├── reports/charts/      4 PNG charts (bar, histogram, scatter, line)
│   └── task3.py
├── task4_notebook_git/      Task 4 - notebook, terminal and Git
│   ├── analysis.ipynb       reads ../task3_numpy_pandas/data/
│   ├── analysis.py          nbconvert export
│   └── backup/              made with mkdir, cp and mv
├── requirements.txt
├── .gitignore
├── .env.example             copy to .env (shared by all tasks, never committed)
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

## Run the tasks (from the project root, with .venv active)
```powershell
python task1_python_oop/task1.py     # Python core, OOP, custom error, loops
python task2_files_api/task2.py      # CSV -> JSON/CSV, .env, API calls (needs internet)
python task3_numpy_pandas/task3.py   # NumPy, Pandas, cleaning, merges, 4 charts
```
Paths are built from each script's own folder, so `cd task1_python_oop` then `python task1.py` also works.

## Task 4 - Notebook
Open `task4_notebook_git/analysis.ipynb` in VS Code, choose the `.venv` kernel and click **Run All**.
To run it and export it from the terminal:
```powershell
cd task4_notebook_git
python -m nbconvert --to notebook --execute --inplace analysis.ipynb
python -m nbconvert --to script analysis.ipynb     # creates analysis.py
cd ..
```

## Task 4 - Terminal commands (Git Bash)
```bash
mkdir -p task4_notebook_git/backup                                      # make a folder
cp task1_python_oop/data/employees.csv task4_notebook_git/backup/employees.csv            # copy a file
mv task4_notebook_git/backup/employees.csv task4_notebook_git/backup/employees_backup.csv # rename (move) it
grep -n "Chennai" task1_python_oop/data/employees.csv                   # 4 rows: Arun, Priya, Divya, Suresh
```
PowerShell equivalents: `New-Item -ItemType Directory`, `Copy-Item`, `Move-Item`, `Select-String`.

## Task 4 - Git workflow
```powershell
git checkout -b feature/analysis         # work on a feature branch
git add <files>
git commit -m "Short, meaningful message"
git push -u origin feature/analysis      # then open a PR into main on GitHub
git log --oneline --graph --all          # view the history
```

## Decisions
- Each task has its own folder, data and outputs, so it can be shown on its own.
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
