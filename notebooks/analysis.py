#!/usr/bin/env python
# coding: utf-8

# # Week 1 Assessment - Employee Analysis
# 
# NumPy, Pandas and Matplotlib analysis of `data/employees.csv`.
# Run this notebook from the `notebooks/` folder.

# ## 1. Imports

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA = '../data/'


# ## 2. NumPy - student marks (4 students x 3 subjects)

# In[2]:


marks = np.array([[78, 85, 90],
                  [65, 70, 72],
                  [88, 92, 80],
                  [55, 60, 68]])
print('Shape:', marks.shape)
print('Student averages:', marks.mean(axis=1).round(2))   # per row
print('Subject averages:', marks.mean(axis=0).round(2))   # per column
print('After 5 grace marks:')
print(marks + 5)   # broadcasting
weights = np.array([0.4, 0.35, 0.25])
print('Weighted scores:', np.dot(marks, weights).round(2))


# ### Timing with %timeit
# How fast NumPy computes the student averages.

# In[3]:


get_ipython().run_line_magic('timeit', 'marks.mean(axis=1)')


# ## 3. Pandas - load and explore

# In[4]:


df = pd.read_csv(DATA + 'employees.csv')
df.info()


# In[5]:


df.describe()


# In[6]:


# loc = by label, iloc = by position, then a filter
print(df.loc[df['city'] == 'Chennai', ['name', 'salary']])
print(df.iloc[0:3, 0:3])
df[df['salary'] > 50000]


# ## 4. Cleaning example
# `employees_raw.csv` is a copy of `employees.csv` with 2 blank salaries (Priya, Meena) and Rahul's row repeated.
# The original file is not changed. After cleaning, the copy has the same 8 employees, so the headcount does not change.

# In[7]:


raw = pd.read_csv(DATA + 'employees_raw.csv')
print('Missing:', raw['salary'].isna().sum(), '| Duplicates:', raw.duplicated().sum())
clean = raw.drop_duplicates().copy()
clean['salary'] = clean['salary'].fillna(clean['salary'].median()).astype(int)
print('Clean rows:', len(clean))
clean.dtypes


# ## 5. Group by department and merge

# In[8]:


summary = (df.groupby('department')
             .agg(headcount=('id', 'count'),
                  avg_salary=('salary', 'mean'),
                  max_salary=('salary', 'max'))
             .reindex(['Sales', 'HR', 'IT', 'Finance']))
print('Headcount: ' + ' | '.join(f'{d} {n}' for d, n in summary['headcount'].items()))
summary


# In[9]:


departments = pd.read_csv(DATA + 'departments.csv')
inner = pd.merge(df, departments, on='department', how='inner')
left = pd.merge(departments, df, on='department', how='left')
outer = pd.merge(df, departments, on='department', how='outer')
print('Inner:', len(inner), '| Left:', len(left), '| Outer:', len(outer))
print('No employees:', outer.loc[outer['id'].isna(), 'department'].tolist())
outer


# ## 6. Charts
# The same four charts as `src/task3.py`, which saves them to `reports/`.

# In[10]:


fig, axes = plt.subplots(2, 2, figsize=(11, 7))

axes[0, 0].bar(summary.index, summary['avg_salary'], label='Average salary')
axes[0, 0].set(title='Average Salary by Department', xlabel='Department', ylabel='Salary (INR)')
axes[0, 0].legend()

axes[0, 1].hist(df['salary'], bins=5, edgecolor='black', label='Employees')
axes[0, 1].set(title='Salary Distribution', xlabel='Salary (INR)', ylabel='Number of employees')
axes[0, 1].legend()

for city, g in df.groupby('city'):
    axes[1, 0].scatter(g['id'], g['salary'], label=city, s=60)
axes[1, 0].set(title='Employee Salary by City', xlabel='Employee ID', ylabel='Salary (INR)')
axes[1, 0].legend(title='City')

for name, row in zip(['Asha', 'Bala', 'Chitra', 'Dinesh'], marks):
    axes[1, 1].plot(['Maths', 'Science', 'English'], row, marker='o', label=name)
axes[1, 1].set(title='Student Marks by Subject', xlabel='Subject', ylabel='Marks')
axes[1, 1].legend(title='Student')

fig.tight_layout()
plt.show()


# ## 7. Insights
# - **Bar:** Finance has the highest average salary (90000) and Sales the lowest (41000).
# - **Histogram:** The most common salary range is 42000-54000, with 3 of 8 employees.
# - **Scatter:** Mumbai has the highest average salary by city (69000).
# - **Line:** Chitra has the best average mark (86.67) and Dinesh the lowest (61.00).
