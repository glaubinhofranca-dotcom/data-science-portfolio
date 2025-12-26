import sqlite3
import random
from datetime import datetime, timedelta

# Database Connection
conn = sqlite3.connect('company_data.db')
c = conn.cursor()

# 1. Create Tables
c.execute('''
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER,
    role TEXT,
    salary INTEGER,
    hire_date DATE,
    FOREIGN KEY (department_id) REFERENCES departments (id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    amount INTEGER,
    sale_date DATE,
    region TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees (id)
)
''')

# 2. Insert Data
departments = ['Sales', 'Engineering', 'HR', 'Marketing', 'Finance']
for i, dept in enumerate(departments):
    c.execute('INSERT OR IGNORE INTO departments (id, name) VALUES (?, ?)', (i+1, dept))

roles = ['Associate', 'Manager', 'Director', 'Analyst']
regions = ['North', 'South', 'East', 'West']

# Generate 50 Employees
print("Creating Employees...")
for i in range(1, 51):
    name = f"Employee_{i}"
    dept_id = random.randint(1, 5)
    role = random.choice(roles)
    salary = random.randint(50000, 150000)
    hire_date = datetime.now() - timedelta(days=random.randint(0, 3650))
    c.execute('INSERT OR IGNORE INTO employees (id, name, department_id, role, salary, hire_date) VALUES (?, ?, ?, ?, ?, ?)', 
              (i, name, dept_id, role, salary, hire_date.strftime('%Y-%m-%d')))

# Generate 200 Sales
print("Creating Sales Records...")
for i in range(1, 201):
    emp_id = random.randint(1, 50)
    # Only sales dept (id 1) makes sales usually, but let's randomize for chaos
    amount = random.randint(1000, 50000)
    date = datetime.now() - timedelta(days=random.randint(0, 365))
    region = random.choice(regions)
    c.execute('INSERT OR IGNORE INTO sales (id, employee_id, amount, sale_date, region) VALUES (?, ?, ?, ?, ?)', 
              (i, emp_id, amount, date.strftime('%Y-%m-%d'), region))

conn.commit()
conn.close()
print("✅ Database 'company_data.db' created successfully!")