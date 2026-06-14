# Service Hub - Stage E

## What this app contains

Python + Tkinter GUI connected to PostgreSQL.

The system includes:

- Login screen
- Manager dashboard
- Employee dashboard
- Customers screen
- Requests screen
- Transactions screen
- Products screen
- Manager queries
- Workload balance process
- Supply and demand process
- Product discount screen
- Popups for CRUD and process results

## First run

### 1. Install Python package

```bash
pip install psycopg2-binary
```

### 2. Run setup SQL

Run this file in pgAdmin:

```text
setup_stage_e.sql
```

It adds:

- password column to employee
- role column to employee
- manager role for employee with eid = 1
- is_active column to products

Default password for all employees:

```text
1234
```

Employee with eid = 1 is manager.

### 3. Update database connection

Open:

```text
config.py
```

Change:

```python
"database": "PUT_YOUR_DATABASE_NAME_HERE",
"password": "PUT_YOUR_POSTGRES_PASSWORD_HERE",
```

### 4. Run app

```bash
python app.py
```

## Login

Use:

```text
Employee ID: 1
Password: 1234
```

This logs in as manager.

Other employees can log in with their employee id and password 1234.

## Notes

- Products are not physically deleted. The app performs logical delete using `is_active = false`.
- Status, priority, customers and employees are shown by names using joins and combo boxes.
- Employees see only their own requests and transactions.
- Manager can enter employee screens and also see manager actions.
