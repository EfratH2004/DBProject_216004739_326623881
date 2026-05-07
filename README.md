# DBProject – Phase 1

## Team Members
Meitav Bin Nun  
Efrat Hourvitz  

---

## Introduction

The general topic of the project is an **online store system**.  
Each team was required to focus on a specific department within the store.

Our team chose to focus on the **Customer Service department**.  
Therefore, the system we designed manages the information required for customer support operations, including customers, service requests, employees, products, and transactions related to customer inquiries.

---

# System Description

The goal of the system is to help customer service employees track customer activity, handle service requests, and view purchase information in order to provide better support.

The system manages the following main entities:

- **Customers** – store customer contact information.
- **Products** – represent products available in the online store.
- **Transactions** – represent purchases completed by customers on the website.
- **Requests** – represent customer service requests opened through the website.
- **Employees** – represent customer service employees that handle requests and assist customers.

### System functionality

Customers can perform purchases on the website, which are stored as **transactions** in the system.  
Customers can also open **service requests** when they encounter issues or need assistance.

Customer service **employees** handle these requests and may also assist customers regarding previous transactions.

The system allows tracking:

- customer purchases  
- customer service requests  
- employee handling of requests  
- relationships between customers, products, and transactions  

This information enables the customer service team to provide efficient support.

---

# ERD Diagram

![ERD Diagram](phase1/images/ERD.png)

---

# DSD Diagram

![DSD Diagram](phase1/images/DSD.png)

---

# DSD Diagram of pgAdmin

![DSD Diagram](phase1/images/ERD_pgAdmin.png)

---

# Data Population Documentation

### Data Generation – Customers
![Customers Data](phase1/images/customers_mockaroo.png)

### Data Generation – Employees
![Employees Data](phase1/images/employees_mockaroo.png)

### Data Generation – Products
![Products Data](phase1/images/products_mockaroo.png)

---

# Data Insertion Process

The data was inserted into the database in multiple stages:

1. Creation of tables using SQL scripts  
2. Generation of mock data using Mockaroo  
3. Importing CSV files into PostgreSQL  
4. Ensuring referential integrity using foreign keys  
5. Running validation queries to verify correctness  

---

# System Screens

### Login Screen
![Login](phase1/images/login.png)

---

### Dashboard
![Dashboard](phase1/images/dashboard.png)

---

### Customers Screen
![Customers](phase1/images/customers.png)

---

### Products Screen
![Products](phase1/images/products.png)

---

### Employees Screen
![Employees](phase1/images/employees.png)

---

### Requests Screen
![Requests](phase1/images/requests.png)

---

### Transactions Screen
![Transactions](phase1/images/transactions.png)

---

# Backup

A full backup of the database was created.

The backup includes:

- Database structure (tables, relationships, constraints)  
- All inserted data  

Backup file:
[Download backup](./phase1/customer_service_backup.backup)

# Phase 2

## Introduction

In this phase of the project, advanced SQL queries, transactions, constraints, and indexes were implemented in order to improve the functionality and performance of the database system.

The main goals of this phase were:

- Writing complex SELECT queries
- Comparing different implementations of the same query
- Performing UPDATE and DELETE operations
- Using transactions with COMMIT and ROLLBACK
- Adding constraints using ALTER TABLE
- Improving query efficiency using indexes
- Measuring query performance before and after indexing

The queries were designed according to the GUI screens of the system such as Requests, Employees, Products, Customers, Transactions, and Dashboard.

---

# SELECT Queries

## Query 1 – Open Requests Older Than 30 Days

### Version A – Using INTERVAL

This query displays all open customer requests that have been open for more than 30 days.

![openMoreThan30Days1.1](phase2/images/openMoreThan30Days1.1.jpeg)

---

### Version B – Using Date Difference Calculation

This query also displays open requests older than 30 days by directly calculating the number of days.

![openMoreThan30Days1.2](phase2/images/openMoreThan30Days1.2.jpeg)

---

### Efficiency Comparison

Version A is generally more efficient because PostgreSQL can optimize INTERVAL comparisons better than repeated arithmetic calculations on dates.

---

## Query 2 – High Priority Requests

### Version A – Using JOIN

This query displays all requests marked as high priority.

![highPriority1](phase2/images/highPriority1.jpeg)

---

### Version B – Using Subquery

This query retrieves high priority requests using a nested subquery.

![highPriority2](phase2/images/highPriority2.jpeg)

---

### Efficiency Comparison

The JOIN version is usually more efficient because PostgreSQL can optimize joins directly without recalculating subqueries.

---

## Query 3 – Products That Were Never Sold

### Version A – Using LEFT JOIN

This query displays products that do not appear in any transaction.

![unsoldProducts1](phase2/images/unsoldProducts1.jpeg)

---

### Version B – Using NOT EXISTS

This query also finds products that were never sold using NOT EXISTS.

![unsoldProducts2](phase2/images/unsoldProducts2.jpeg)

---

### Efficiency Comparison

NOT EXISTS is generally more efficient because it works better with indexes and avoids large join operations.

---

## Query 4 – Employees With No Requests

### Version A – Using NOT IN

This query displays employees who never handled any request.

![noRequestsEmployees1](phase2/images/noRequestsEmployees1.jpeg)

---

### Version B – Using NOT EXISTS

This query also finds employees who did not handle requests.

![noRequestsEmployees2](phase2/images/noRequestsEmployees2.jpeg)

---

### Efficiency Comparison

NOT EXISTS is usually safer and more efficient because it handles NULL values correctly and optimizes better with indexes.

---

## Query 5 – Employee With Most Closed Requests

### Version A – Using ALL

This query displays the employee who handled the highest number of closed requests.

![mostRequestsOfEmployee1](phase2/images/mostRequestsOfEmployee1.jpeg)

---

### Version B – Using MAX

This query also finds the employee with the highest number of closed requests.

![mostRequestsOfEmployee2](phase2/images/mostRequestsOfEmployee2.jpeg)

---

### Efficiency Comparison

The MAX version is usually clearer and more stable for optimization, while the ALL version demonstrates advanced SQL capabilities.

---

# Additional SELECT Queries

## Query 6 – Total Revenue Per Customer

This query calculates the total amount spent by each customer.

![totalPerClient](phase2/images/totalPerClient.jpeg)

---

## Query 7 – Products With Highest Revenue

This query displays the products that generated the highest revenue.

![mostMoneyProducts](phase2/images/mostMoneyProducts.jpeg)

---

## Query 8 – Open Requests Per Employee

This query displays the number of open requests assigned to each employee.

![openRequestsPerEmloyee](phase2/images/openRequestsPerEmloyee.jpeg)

---

## Query 9 – Employees With More Than 10 Years Experience

This query displays employees with more than 10 years of experience.

![10YearsExperience](phase2/images/10YearsExperience.jpeg)

---

## Query 10 – Total Revenue Per Customer

This query displays the total revenue generated from each customer.

![totalPerCostumer](phase2/images/totalPerCostumer.jpeg)

---

## Query 11 – Closed Requests This Year

This query displays all requests that were closed during the current year.

![closedRequestThisYear](phase2/images/closedRequestThisYear.jpeg)

---

## Query 12 – Most Sold Products

This query displays the products with the highest number of sales.

![mostSoldProducts](phase2/images/mostSoldProducts.jpeg)

---

# UPDATE Queries

## UPDATE Query 1 – Transaction With COMMIT and ROLLBACK

The following transaction demonstrates the use of BEGIN, UPDATE, ROLLBACK, and COMMIT.

### Before Update

The database before the update operation.

![beforeUpdate](phase2/images/beforeUpdate.jpeg)

---

### Update Operation

The UPDATE query execution.

![update](phase2/images/update.png)

---

### After Update

The database after the update operation.

![afterUpdate](phase2/images/afterUpdate.jpeg)

---

### ROLLBACK

The transaction was rolled back and the database returned to its previous state.

![rollback](phase2/images/rollback.jpeg)

---

### COMMIT

The transaction was committed and the changes were saved permanently.

![commit](phase2/images/commit.jpeg)

---

## UPDATE Query 2 – Assign Requests Without Employee

This query assigns requests without an employee to a specific employee.

### Before Update

![update11](phase2/images/update11.jpeg)

---

### Update Query

![update12](phase2/images/update12.jpeg)

---

### After Update

![update13](phase2/images/update13.jpeg)

---

## UPDATE Query 3 – Change Request Status

This query changes the status of a request.

### Before Update

![update21](phase2/images/update21.jpeg)

---

### Update Query

![update22](phase2/images/update22.jpeg)

---

### After Update

![update23](phase2/images/update23.png)

---

# DELETE Queries

## DELETE Query 1 – Delete Old Requests

This query deletes very old requests from the database.

### Before Delete

![DELETE1_1](phase2/images/DELETE1_1.png)

---

### After Delete

![DELETE1_2](phase2/images/DELETE1_2.png)

---

## DELETE Query 2 – Delete Customers Without Activity

This query deletes customers that have no requests and no transactions.

### Before Delete

![DELETE2_1](phase2/images/DELETE2_1.png)

---

### After Delete

![DELETE2_2](phase2/images/DELETE2_2.png)

---

## DELETE Query 3 – Delete Unsold Products

This query deletes products that were never sold.

### Before Delete

![DELETE3_1](phase2/images/DELETE3_1.png)

---

### After Delete

![DELETE3_2](phase2/images/DELETE3_2.png)

---

# Constraints

## Constraint 1 – UNIQUE Constraint

This constraint ensures that duplicate requests from the same customer and employee on the same date cannot exist.

### Constraint Creation

![UNIQUE_CONSTRAIN1](phase2/images/UNIQUE_CONSTRAIN1.png)

---

### Constraint Validation

![UNIQUE_CONSTRAIN2](phase2/images/UNIQUE_CONSTRAIN2.png)

---

## Constraint 2 – CHECK Constraint

This constraint ensures that product prices must always be positive.

### Constraint Creation

![CHECK_CONSTRAIN1](phase2/images/CHECK_CONSTRAIN1.png)

---

### Constraint Validation

![CHECK_CONSTRAIN2](phase2/images/CHECK_CONSTRAIN2.png)

---

## Constraint 3 – FOREIGN KEY Constraint

This constraint ensures that every request belongs to an existing customer.

### Constraint Creation

![FOREIGN_KEY_CONSTRAIN1](phase2/images/FOREIGN_KEY_CONSTRAIN1.png)

---

### Constraint Validation

![FOREIGN_KEY_CONSTRAIN2](phase2/images/FOREIGN_KEY_CONSTRAIN2.png)

---

# Indexes

## Created Indexes

The following indexes were created in order to improve query performance.

![INDEXES](phase2/images/INDEXES.png)

---

## Index 1 – Requests Date Index

### Before Index

![INDEX1_1](phase2/images/INDEX1_1.png)

---

### After Index

![INDEX1_2](phase2/images/INDEX1_2.png)

---

### Explanation

The index improved filtering operations on request dates by reducing the number of scanned rows.

---

## Index 2 – Transactions Customer and Date Index

### Before Index

![INDEX2_1](phase2/images/INDEX2_1.png)

---

### After Index

![INDEX2_2](phase2/images/INDEX2_2.png)

---

### Explanation

The index improved searches involving customer transactions and transaction dates.

---

## Index 3 – Requests Employee and Status Index

### Before Index

![INDEX3_1](phase2/images/INDEX3_1.png)

---

### After Index

![INDEX3_2](phase2/images/INDEX3_2.png)

---

### Explanation

The index improved queries that filter requests by employee and request status.

---

# Backup

A full updated backup of the database was created after completing Phase 2.

The backup includes:

- Database structure
- Constraints
- Indexes
- All updated data
- Transactions and relationships

Backup file:

[Download backup](./phase2/backup2.backup)